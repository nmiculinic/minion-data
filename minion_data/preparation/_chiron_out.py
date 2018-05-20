import argparse
import logging
import gzip
from os import path
import typing
import os
from tqdm import tqdm
from typing import NamedTuple
from .align_utils import get_target_sequences
from .. import dataset_pb2
from . import bioinf_utils
from .common import fillDataPoint
import numpy as np
import sys
import multiprocessing as mp
import threading


class MinionDataCfg(NamedTuple):
    chiron_out: str
    sam_file: str
    out: str

class ProcessDataPointCfg(NamedTuple):
    pt: typing.Tuple[str, typing.Tuple]
    cfg: MinionDataCfg
    completed: mp.Queue


def processDataPoint(cfgDp: ProcessDataPointCfg):
    try:
        cfg = cfgDp.cfg
        name, v = cfgDp.pt
        ref, _, _, _, cigar_str = v  # target & cigar_str are important
        ref = [dataset_pb2.BasePair.Value(x) for x in ref.upper()]
        sol = dataset_pb2.DataPoint(aligned_ref=ref,)
        with open(path.join(cfg.chiron_out, "raw", name + ".signal"), "r") as f:
            signal = np.array(f.readlines()[0].split(), dtype=np.float)
            sol.MergeFrom(dataset_pb2.DataPoint(signal=signal))

        with open(path.join(cfg.chiron_out, "labels", name + ".label"), "r") as f:
            labels = []
            bcall: typing.List[dataset_pb2.BasePair] = []
            for l, u, b in [x.split() for x in f.readlines() if len(x)]:
                labels.append(
                    dataset_pb2.DataPoint.BPConfidenceInterval(
                        lower=l,
                        upper=u,
                        pair=typing.cast(dataset_pb2.BasePair, dataset_pb2.BasePair.Value(b.upper())),
                    )
                )
                bcall.append(dataset_pb2.BasePair.Value(b.upper()))

            sol.MergeFrom(
                dataset_pb2.DataPoint(
                    basecalled=bcall,
                    labels=labels,
                )
            )

        fillDataPoint(sol, cigar_str)
        with gzip.open(path.join(cfg.out, name + ".datapoint"), "w") as f:
            sol_pb_str = sol.SerializeToString()
            f.write(sol_pb_str)
        cfgDp.completed.put(sol_pb_str)
    except Exception as ex:
        logging.getLogger(__name__).error(f"Cannot process {cfgDp.fname_no_ext} {type(ex).__name__}\n{ex}", exc_info=True)
        cfgDp.completed.put(ex)


def main(cfg: MinionDataCfg):
    if not path.isfile(cfg.sam_file):
        raise ValueError(f"{cfg.sam_file} isn't a file")
    os.makedirs(cfg.out, exist_ok=True)
    all = get_target_sequences(cfg.sam_file).items()
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
                    pt=x,
                    cfg=cfg,
                    completed=q,
                ) for x in all]
            )


def run(args):
    if args.default_root is not None:
        args.chiron_out = args.chiron_out or path.join(
            args.default_root, "chiron_out"
        )
        args.sam_file = args.sam_file or path.join(
            args.default_root, "alignment.sam"
        )
        args.out = args.out or path.join(args.default_root, "dataset")
    if args.chiron_out is None or args.sam_file is None:
        print(
            "Both chiron_out and sam_file must be defined (( or default_root ))"
        )
        return 1

    cfg = MinionDataCfg(
        chiron_out=path.abspath(args.chiron_out),
        sam_file=path.abspath(args.sam_file),
        out=path.abspath(args.out),
    )
    main(cfg)
    return 0


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--default-root")
    parser.add_argument("--chiron-out")
    parser.add_argument("--sam_file")
    parser.add_argument("--out", "-o", help="output folder")
    parser.set_defaults(func=run)
