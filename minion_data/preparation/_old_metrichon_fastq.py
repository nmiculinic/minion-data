import os
import edlib
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
from minion_data import butil
from collections import defaultdict
import pysam
import subprocess
from minion_data.preparation._old_metrichon_ref import read_fast5_raw_ref


logger = logging.getLogger(__name__)

class MinionDataCfg(NamedTuple):
    input: str
    out: str
    aligner: str
    reference: str
    workdir: str
    circular: bool


class ProcessDataPointCfg(NamedTuple):
    fast5: str
    target: str
    cigar: str
    cfg: MinionDataCfg
    completed: mp.Queue


def processDataPoint(cfgDp: ProcessDataPointCfg):
    try:
        fname_out = path.join(cfgDp.cfg.out, path.splitext(cfgDp.fast5)[0].split(os.sep)[-1] + ".datapoint")
        sol = read_fast5_raw_ref(cfgDp.fast5, ref_cigar=cfgDp.cigar, ref_seq=cfgDp.target)
        with gzip.open(fname_out, "w") as f:
            sol_pb_str = sol.SerializeToString()
            f.write(sol_pb_str)
        cfgDp.completed.put(sol_pb_str)
    except Exception as ex:
        logging.getLogger(__name__).error(f"Cannot process {cfgDp.fast5} {type(ex).__name__}\n{ex}", exc_info=True)
        cfgDp.completed.put(ex)


def main(cfg: MinionDataCfg):
    os.makedirs(cfg.out, exist_ok=True)
    os.makedirs(cfg.workdir, exist_ok=True)
    all_files = glob(cfg.input + "/*.fast5")

    fastq_fn = os.path.join(cfg.workdir, "all.fastq")
    sam_fn = os.path.join(cfg.workdir, "all.sam")

    id2fast5 = {}
    logger.info(f"Reading fastq from {cfg.input}, {len(all_files)} elements")
    with open(fastq_fn, "w") as f:
        for file in tqdm(all_files, desc="reading fastqs"):
            with h5py.File(file, "r") as h5:
                fastq = h5['/Analyses/Basecall_1D_000/BaseCalled_template/Fastq'][()].decode()
                id2fast5[fastq.split("\n")[0].split(" ")[0].replace("@","")] = file
                print(fastq, file=f)

    args = [
       "graphmap",
        "align",
        "-r",
        cfg.reference,
        "-d",
        fastq_fn,
        "-o",
        sam_fn,
        "--extcigar",
        "-t",
        str(os.cpu_count() or 8),
    ]
    if cfg.circular:
        args.append("-C")

    arg_line = " ".join(args)
    logger.info(f"Aligning with {cfg.aligner}\n{arg_line}")
    subprocess.run(args)

    cnt = defaultdict(int)
    result_dict = {}

    with pysam.AlignmentFile(sam_fn, "r") as samfile:
        for x in tqdm(samfile.fetch(), desc='Building ref'):
            x: pysam.AlignedSegment = x
            name = x.query_name
            cnt['total'] += 1

            if x.is_unmapped:
                cnt['unmapped'] += 1
                #logging.warning("%s unmapped" % name)
                continue
            try:
                # hack to bypass segfault
                full_cigar = butil.decompress_cigar_pairs(x.cigartuples)
                r_len = butil.get_read_len_from_cigar(full_cigar)
                ref_len = butil.get_ref_len_from_cigar(full_cigar)

                if r_len != x.query_length or ref_len != x.reference_length:
                    logging.error(
                        "%s cigar operations do not match alignment info in md",
                        name
                    )
                    cnt['invalid_md_cigar'] += 1
                    continue

                target = x.get_reference_sequence()
            except (ValueError, AssertionError) as e:
                cnt['missign_ref'] += 1
                logging.error(
                    "%s Mapped but reference len equals 0, md tag: %s", name,
                    x.has_tag('MD')
                )
                continue

            ref_name = x.reference_name
            length = x.reference_length
            start_pos = x.reference_start
            cigar_pairs = x.cigartuples

            if x.is_reverse:
                target = butil.reverse_complement(target)
                cigar_pairs = list(reversed(cigar_pairs))

            cigar_str = butil.decompress_cigar_pairs(cigar_pairs, mode='ints')

            if name in result_dict:
                prev_target, _, prev_start_pos, _, prev_cigar_str = result_dict[
                    name
                ]
                merged = _merge_circular_aligment(
                    prev_target, prev_start_pos, prev_cigar_str, target,
                    start_pos, cigar_str, x.is_reverse, x.query_name
                )
                if not merged:
                    continue

                target, start_pos, cigar_str = merged
            result_dict[name] = [target.upper(), cigar_str]

    with tqdm(total=len(result_dict), desc="preparing dataset") as pbar:
        with mp.Pool() as p:
            m = mp.Manager()
            q = m.Queue()

            def f():
                for _ in range(len(result_dict)):
                    q.get()
                    pbar.update()

            threading.Thread(target=f, daemon=True).start()
            for k, v in result_dict.items():
                p.map(
                    processDataPoint,
                    [ProcessDataPointCfg(
                        fast5=id2fast5[k],
                        target=v[0],
                        cigar=v[1],
                        cfg=cfg,
                        completed=q,
                    ) for k, v in result_dict.items()]
                )


def _merge_circular_aligment(
        target_1, start_pos_1, cigar_str_1, target_2, start_pos_2, cigar_str_2,
        is_reversed, qname
):

    if is_reversed:
        # reverse back both
        cigar_str_1 = ''.join(reversed(cigar_str_1))
        target_1 = butil.reverse_complement(target_1)

        cigar_str_2 = ''.join(reversed(cigar_str_2))
        target_2 = butil.reverse_complement(target_2)

    if start_pos_1 == 0:
        start = start_pos_2
        cigar = butil.rtrim_cigar(cigar_str_2) + butil.ltrim_cigar(cigar_str_1)
        target = target_2 + target_1

    elif start_pos_2 == 0:
        start = start_pos_1
        cigar = butil.rtrim_cigar(cigar_str_1) + butil.ltrim_cigar(cigar_str_2)
        target = target_1 + target_2

    else:
        # not circular, duplicate
        logging.error("Duplicate read with name %s", qname)
        return None

    if is_reversed:
        cigar = ''.join(reversed(cigar))
        target = butil.reverse_complement(target)

    return [target, start, cigar]


def run(args):
    logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    main(MinionDataCfg(
        input=args.input,
        out=args.out,
        aligner=args.aligner,
        reference=args.reference,
        workdir=args.workdir,
        circular=args.circular,
    ))


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--input", "-i", help="input folder with fast5s", required=True)
    parser.add_argument("--out", "-o", help="output folder", required=True)
    parser.add_argument("--reference", "-r", help="reference file", required=True)
    parser.add_argument("--aligner", "-a", help="aligner to use", choices=["graphmap"], default="graphmap")
    parser.add_argument("--workdir", "-w", help="Workdir", default=".")
    parser.add_argument("--circular", "-C", help="circular genome", action="store_true")
    parser.set_defaults(func=run)

