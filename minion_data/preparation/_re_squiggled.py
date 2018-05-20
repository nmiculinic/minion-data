import argparse
import logging
import gzip
import h5py
from os import path
import typing
import os
from tqdm import tqdm
from typing import NamedTuple
from .. import dataset_pb2
import numpy as np
import multiprocessing as mp
import threading
from glob import glob
from .common import fillDataPoint
from minion_data.inspect import debug_output


class MinionDataCfg(NamedTuple):
    input: str
    out: str
    basecall_group: str
    basecall_subgroup: str

class ProcessDataPointCfg(NamedTuple):
    fname_no_ext: str
    cfg: MinionDataCfg
    completed: mp.Queue


def processDataPoint(cfgDp: ProcessDataPointCfg):
    try:
        cfg = cfgDp.cfg
        sol = dataset_pb2.DataPoint()
        with h5py.File(cfgDp.fname_no_ext + ".fast5", 'r') as fast5_data:
            # Get raw data
            try:
                raw_dat = list(fast5_data['/Raw/Reads/'].values())[0]
                # raw_attrs = raw_dat.attrs
                raw_dat = raw_dat['Signal'].value
                sol.MergeFrom(dataset_pb2.DataPoint(signal=raw_dat))
            except:
                raise RuntimeError(
                    'Raw data is not stored in Raw/Reads/Read_[read#] so ' +
                    'new segments cannot be identified.')

            # Read corrected data
            try:
                corr_data = fast5_data[
                    '/Analyses/RawGenomeCorrected_000/' + cfg.basecall_subgroup + '/Events']
                corr_attrs = dict(list(corr_data.attrs.items()))
                corr_data = corr_data.value
            except:
                raise RuntimeError((
                    'Corrected data not found.'))

            # Maybe
            basecalled = fast5_data[f"/Analyses/{cfg.basecall_group}/BaseCalled_template/Fastq"].value.strip().split()[2].decode("ASCII")

            # fast5_info = fast5_data['UniqueGlobalKey/channel_id'].attrs
            # sampling_rate = fast5_info['sampling_rate'].astype('int_')

            # Reading extra information
            corr_start_rel_to_raw = corr_attrs['read_start_rel_to_raw']
            if any(len(vals) <= 1 for vals in (
                    corr_data, raw_dat)):
                raise NotImplementedError((
                    'One or no segments or signal present in read.'))

            event_starts = corr_data['start'] + corr_start_rel_to_raw
            event_lengths = corr_data['length']
            event_bases = corr_data['base']

            label_data = np.array(
                list(zip(event_starts, event_lengths, event_bases)),
                dtype=[('start', '<u4'), ('length', '<u4'), ('base', 'S1')])

            labels = []
            for index, start in enumerate(event_starts):
                labels.append(dataset_pb2.DataPoint.BPConfidenceInterval(
                    lower=start,
                    upper=start + event_lengths[index],
                    pair=typing.cast(
                        dataset_pb2.BasePair,
                        dataset_pb2.BasePair.Value(label_data['base'][index].decode("ASCII").upper())),
                    ),
                )

            sol.MergeFrom(dataset_pb2.DataPoint(
                basecalled=[typing.cast(dataset_pb2.BasePair, dataset_pb2.BasePair.Value(x)) for x in basecalled],
                aligned_ref=[x.pair for x in labels],
                labels=labels,
            ))
            fillDataPoint(sol)

        fname_out = path.join(cfg.out, cfgDp.fname_no_ext.split(os.sep)[-1] + ".datapoint")
        with gzip.open(fname_out, "w") as f:
            sol_pb_str = sol.SerializeToString()
            f.write(sol_pb_str)
        cfgDp.completed.put(sol_pb_str)
    except Exception as ex:
        logging.getLogger(__name__).error(f"Cannot process {cfgDp.fname_no_ext} {type(ex).__name__}\n{ex}", exc_info=True)
        cfgDp.completed.put(ex)


def main(cfg: MinionDataCfg):
    os.makedirs(cfg.out, exist_ok=True)
    all = glob(cfg.input + "/*.fast5")
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
                    fname_no_ext=os.path.splitext(x)[0],
                    cfg=cfg,
                    completed=q,
                ) for x in all]
            )


def run(args):
    logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    cfg = MinionDataCfg(
        input=path.abspath(args.input),
        out=path.abspath(args.out),
        basecall_group=args.basecall_group,
        basecall_subgroup=args.basecall_subgroup,
    )
    main(cfg)
    return 0


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--input", "-i", help="input folder with re-sqiggled fast5s", required=True)
    parser.add_argument("--out", "-o", help="output folder", required=True)
    parser.add_argument('--basecall_group', default='Basecall_1D_000',
                        help='Basecall group Nanoraw resquiggle into. Default is Basecall_1D_000')
    parser.add_argument('--basecall_subgroup', default='BaseCalled_template',
                        help='Basecall subgroup Nanoraw resquiggled into. Default is BaseCalled_template')
    parser.set_defaults(func=run)
