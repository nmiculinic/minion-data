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


class MinionDataCfg(NamedTuple):
    input: str
    out: str
    aligner: str
    reference: str
    workdir: str


class ProcessDataPointCfg(NamedTuple):
    fast5: str
    cfg: MinionDataCfg
    completed: mp.Queue


def main(cfg: MinionDataCfg):
    os.makedirs(cfg.input, exist_ok=True)
    all = glob(cfg.input + "/*.fast5")

    for file in tqdm(all, desc="preparing dataset"):
        with h5py.File(file, "r") as f:
            fastq = f['/Analyses/Basecall_1D_000/BaseCalled_template/Fastq'][()].decode().split('\n')
        print(fastq)

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
    ))


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--input", "-i", help="input folder with fast5s", required=True)
    parser.add_argument("--out", "-o", help="output folder", required=True)
    parser.add_argument("--reference", "-r", help="reference file", required=True)
    parser.add_argument("--aligner", "-a", help="aligner to use", choices=["graphmap"], default="graphmap")
    parser.add_argument("--workdir", "-w", help="Workdir", default=".")
    parser.set_defaults(func=run)

