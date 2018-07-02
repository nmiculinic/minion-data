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
import subprocess


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
    cfg: MinionDataCfg
    completed: mp.Queue


def main(cfg: MinionDataCfg):
    os.makedirs(cfg.out, exist_ok=True)
    os.makedirs(cfg.workdir, exist_ok=True)
    all_files = glob(cfg.input + "/*.fast5")

    fastq_fn = os.path.join(cfg.workdir, "all.fastq")
    sam_fn = os.path.join(cfg.workdir, "all.sam")

    logger.info(f"Reading fastq from {cfg.input}, {len(all_files)} elements")
    with open(fastq_fn, "w") as f:
        for file in tqdm(all_files, desc="reading fastqs"):
            with h5py.File(file, "r") as h5:
                fastq = h5['/Analyses/Basecall_1D_000/BaseCalled_template/Fastq'][()].decode()
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

    # with tqdm(total=len(all), desc="preparing dataset") as pbar:
    #     with mp.Pool() as p:
    #         m = mp.Manager()
    #         q = m.Queue()
    #
    #         def f():
    #             for _ in range(len(all)):
    #                 q.get()
    #                 pbar.update()
    #
    #         threading.Thread(target=f, daemon=True).start()
    #         p.map(
    #             processDataPoint,
    #             [ProcessDataPointCfg(
    #                 fast5=x,
    #                 cfg=cfg,
    #                 completed=q,
    #             ) for x in all]
    #         )


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

