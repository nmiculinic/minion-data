import argparse
import logging
import gzip
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


class MinionDataCfg(NamedTuple):
    input: str
    out: str

class ProcessDataPointCfg(NamedTuple):
    fname_no_ext: str
    cfg: MinionDataCfg
    completed: mp.Queue


def processDataPoint(cfgDp: ProcessDataPointCfg):
    try:
        cfg = cfgDp.cfg
        sol = dataset_pb2.DataPoint()
        with open(cfgDp.fname_no_ext + ".signal", "r") as f:
            signal = np.array(f.readlines()[0].split(), dtype=np.float)
            sol.MergeFrom(dataset_pb2.DataPoint(signal=signal))

        with open(cfgDp.fname_no_ext + ".label", "r") as f:
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
                cigar=[dataset_pb2.MATCH] * len(bcall),
                aligned_ref=bcall,
                aligned_ref_squiggle=bcall,
                basecalled_squiggle=bcall,
            )
        )
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
    all = glob(cfg.input + "/*.signal")
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
    )
    main(cfg)
    return 0


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--input", "-i", help="input folder with .signal and .label files", required=True)
    parser.add_argument("--out", "-o", help="output folder", required=True)
    parser.set_defaults(func=run)
