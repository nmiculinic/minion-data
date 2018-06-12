import os
from os import path
import gzip
import argparse
import logging
from tqdm import tqdm
import threading
import multiprocessing as mp
from glob import glob
from minion_data.preparation import bioinf_utils
from pprint import pprint
import numpy as np
import h5py
from typing import *
from minion_data import dataset_pb2


def find_ref(fast5_path):
    dirname = os.path.dirname(fast5_path)
    basename = os.path.basename(fast5_path)
    name, ext = os.path.splitext(basename)
    ref_path = os.path.join(dirname, name + '.ref')

    if not os.path.exists(ref_path):
        raise ValueError(
            "{}-> search query:{}.ref in following directory {}".format(basename, name, dirname))
    return ref_path


def get_basecalled_data(h5, target_read, sampling_rate):
    basecalled_events = h5['/Analyses/Basecall_1D_000/BaseCalled_template/Events']
    basecalled_events = np.array(basecalled_events.value[['start', 'length', 'model_state', 'move']])

    raw_start_time = h5['Raw/Reads/' + target_read].attrs['start_time']
    events = h5['/Analyses/EventDetection_000/Reads/' + target_read]
    event_start_time = events.attrs['start_time']

    basecalled_events['start'] -= events['Events'][0]['start'] / sampling_rate
    basecalled_events['start'] += (event_start_time - raw_start_time) / sampling_rate
    return (
        basecalled_events,
        h5['/Analyses/Basecall_1D_000/BaseCalled_template/Fastq'][()].decode().split('\n')
    )


def read_fast5(fast5_path):
    with h5py.File(fast5_path, 'r') as h5:
        reads = h5['Raw/Reads']
        target_read = list(reads.keys())[0]
        sampling_rate = h5['UniqueGlobalKey/channel_id'].attrs['sampling_rate']
        basecalled, fastq = get_basecalled_data(h5, target_read, sampling_rate)

        signal = h5['Raw/Reads/' + target_read]['Signal']
        start_time = basecalled[0]['start']
        start_pad = int(sampling_rate * basecalled[0]['start'])
        signal_len = int(sampling_rate * (basecalled[-1]['start'] + basecalled[-1]['length'] - basecalled[0]['start']))

        # np.testing.assert_allclose(len(signal), start_pad + signal_len, rtol=1e-2)  # Within 1% relative tolerance, TODO check for HMM and RNN discrepancy

        basecalled['start'] -= start_time
        signal = signal[start_pad:start_pad + signal_len]

        return {
            'signal': signal,
            'basecalled': basecalled,
            'sampling_rate': sampling_rate,
            'fastq': fastq,
            'start_pad': start_pad,
            'signal_len': signal_len
        }


def read_fast5_raw_ref(fast5_path, ref_path=None, verify_file=True, correct=True) -> dataset_pb2.DataPoint:
    fast5 = read_fast5(fast5_path)

    signal = fast5['signal']
    basecalled = fast5['basecalled']
    sampling_rate = fast5['sampling_rate']
    fastq = fast5['fastq']
    labels: List[dataset_pb2.DataPoint.BPConfidenceInterval] = []

    # Initial conditions
    # start, length, model_state, move
    for bp in basecalled[0]['model_state'].decode("ASCII"):  # TODO: Should this be reversed?
        labels.append(dataset_pb2.DataPoint.BPConfidenceInterval(
            lower=0,
            upper=1,
            pair=dataset_pb2.BasePair.Value(bp),
        ))
    for b in basecalled[1:]:
        if b['move'] != 0:
            for bp in b['model_state'][-b['move']:].decode("ASCII"):  # TODO: Should this be reversed???
                labels.append(dataset_pb2.DataPoint.BPConfidenceInterval(
                    lower=np.int64(sampling_rate * b['start']),
                    upper=np.int64(sampling_rate * (b['start'] + b['length'])),
                    pair=dataset_pb2.BasePair.Value(bp),
                ))

    dp = dataset_pb2.DataPoint(
        signal=signal,
    )
    if not correct:
        dp.MergeFrom(dataset_pb2.DataPoint(
            labels=labels
        ))
        return dp

    ref_path = ref_path or find_ref(fast5_path)
    with open(ref_path, 'r') as f:
        ref = f.readlines()
    _, ref_ext = os.path.splitext(ref_path)
    if ref_ext == ".ref":
        ref_seq = ref[3].strip()
    else:
        raise ValueError("extension not recognized %s" % ref_ext)
    ref_cigar = ref[2].strip()
    ref_seq = ref_seq.upper()

    corrected_labels = []
    label_idx = 0
    ref_seq_idx = 0

    for c in ref_cigar:
        elem = dataset_pb2.DataPoint.BPConfidenceInterval()
        if c in bioinf_utils.CIGAR_MATCH_MISSMATCH:
            elem.MergeFrom(labels[label_idx])
            elem.pair = dataset_pb2.BasePair.Value(ref_seq[ref_seq_idx])

            corrected_labels.append(elem)
            label_idx += 1
            ref_seq_idx += 1
        elif c in bioinf_utils.CIGAR_INSERTION:
            label_idx += 1
        elif c in bioinf_utils.CIGAR_DELETION:
            if len(corrected_labels) > 0:
                elem.MergeFrom(corrected_labels[-1])
            elem.pair = dataset_pb2.BasePair.Value(ref_seq[ref_seq_idx])
            corrected_labels.append(elem)
            ref_seq_idx +=1
        else:
            raise ValueError("Unknown cigar " + c)

    assert label_idx == len(labels)
    assert ref_seq_idx == len(ref_seq)
    assert len(corrected_labels) == len(ref_seq)

    dp.MergeFrom(dataset_pb2.DataPoint(
        labels=corrected_labels
    ))
    return dp


class MinionDataCfg(NamedTuple):
    input: str
    out: str


class ProcessDataPointCfg(NamedTuple):
    fast5: str
    cfg: MinionDataCfg
    completed: mp.Queue


def processDataPoint(cfgDp: ProcessDataPointCfg):
    try:
        fname_out = path.join(cfgDp.cfg.out, path.splitext(cfgDp.fast5)[0].split(os.sep)[-1] + ".datapoint")
        sol = read_fast5_raw_ref(cfgDp.fast5)
        with gzip.open(fname_out, "w") as f:
            sol_pb_str = sol.SerializeToString()
            f.write(sol_pb_str)
        cfgDp.completed.put(sol_pb_str)
    except Exception as ex:
        logging.getLogger(__name__).error(f"Cannot process {cfgDp.fast5} {type(ex).__name__}\n{ex}", exc_info=True)
        cfgDp.completed.put(ex)


def main(cfg: MinionDataCfg):
    os.makedirs(cfg.input, exist_ok=True)
    all = glob(cfg.out + "/*.fast5")
    with tqdm(total=len(all), desc="preparing dataset") as pbar:
        with mp.Pool() as p:
            m = mp.Manager()
            q = m.Queue()

            def f():
                for _ in range(len(all)):
                    q.get()
                    pbar.update()

            threading.Thread(target=f, daemon=True).start()
            p.map(
                processDataPoint,
                [ProcessDataPointCfg(
                    fast5=x,
                    cfg=cfg,
                    completed=q,
                ) for x in all]
            )


def run(args):
    logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    main(MinionDataCfg(
        input=args.input,
        out=args.out,
    ))


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--input", "-i", help="input folder with fast5s", required=True)
    parser.add_argument("--out", "-o", help="output folder", required=True)
    parser.set_defaults(func=run)


if __name__ == "__main__":
    pprint(read_fast5('/home/lpp/Desktop/test_fast5/odw_genlab4209_20161213_FN_MN16303_sequencing_run_sample_id_32395_ch169_read301_strand.fast5'))
    pprint(read_fast5_raw_ref('/home/lpp/Desktop/test_fast5/odw_genlab4209_20161213_FN_MN16303_sequencing_run_sample_id_32395_ch169_read301_strand.fast5'))


