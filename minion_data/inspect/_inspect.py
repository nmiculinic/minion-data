import argparse
from collections import defaultdict
import os
import glob
import gzip
import numpy as np
from .. import dataset_pb2
import pandas as pd
import cytoolz as toolz
from multiprocessing import pool
from google.protobuf import json_format


def debug_output(pb: dataset_pb2.DataPoint, screen_width: int = 120):
    ttbl = {
        dataset_pb2.MATCH: "=",
        dataset_pb2.MISMATCH: "X",
        dataset_pb2.INSERTION: "I",
        dataset_pb2.DELETION: "D",
    }

    def ff(x):
        if x == dataset_pb2.BLANK:
            return "-"
        return dataset_pb2.BasePair.Name(x)

    for i in range(0, len(pb.cigar), screen_width):
        print(
            "CIGAR:", "".join([ttbl[x] for x in pb.cigar[i:i + screen_width]])
        )
        print(
            "BaseC:",
            "".join([ff(x) for x in pb.basecalled_squiggle[i:i + screen_width]])
        )
        print(
            "REF  :", "".join([
                ff(x) for x in pb.aligned_ref_squiggle[i:i + screen_width]
            ])
        )
        print("------", "-" * screen_width)


def count(x):
    sol = 0
    for _ in x:
        sol += 1
    return sol


def calc_stats(dp: dataset_pb2.DataPoint) -> pd.DataFrame:
    items = []
    signal = np.array(dp.signal)
    items.append(("Signal length", len(signal)))
    items.append(("Signal min value", np.min(signal)))
    items.append(("Signal median value", np.median(signal)))
    items.append(("Signal max value", np.max(signal)))
    items.append(("Signal value std", np.std(signal)))
    items.append(("Basecalled length", len(dp.basecalled)))
    items.append(("Reference length", len(dp.aligned_ref)))
    occ = toolz.frequencies(dp.cigar)
    items.append((
        "Match Rate",
        occ.get(dataset_pb2.MATCH, 0) / len(dp.aligned_ref),
    ))
    items.append((
        "Mismatch Rate",
        occ.get(dataset_pb2.MISMATCH, 0) / len(dp.aligned_ref),
    ))
    items.append((
        "Insertion Rate",
        occ.get(dataset_pb2.INSERTION, 0) / len(dp.aligned_ref),
    ))
    items.append((
        "Deletion Rate",
        occ.get(dataset_pb2.DELETION, 0) / len(dp.aligned_ref),
    ))
    items.append(("Signal sample/bases", len(signal) / len(dp.basecalled)))
    return pd.DataFrame(items, columns=("Attribute", "Value"))


def run(args):
    if os.path.isdir(args.file):
        stats = defaultdict(list)
        ordering = []
        for fname in glob.glob(args.file + "/*.datapoint"):
            with gzip.open(fname, "rb") as f:
                g = f.read()
                dp = dataset_pb2.DataPoint()
                dp.ParseFromString(g)
            if args.stat:
                df = calc_stats(dp)
                for _, row in df.iterrows():
                    stats[row["Attribute"]].append(row["Value"])
                if not ordering:
                    for _, row in df.iterrows():
                        ordering.append(row["Attribute"])

        if args.stat:
            items = []
            for x in ordering:
                arr = np.array(stats[x])
                items.append((
                    x,
                    np.min(arr),
                    np.median(arr),
                    np.mean(arr),
                    np.max(arr),
                    np.std(arr),
                ))
            print(
                pd.DataFrame(
                    items,
                    columns=(
                        "Attribute", "Min", "Median", "Mean", "Max", "stddev"
                    )
                )
            )

    elif os.path.isfile(args.file):
        with gzip.open(args.file, "rb") as f:
            g = f.read()
            dp = dataset_pb2.DataPoint()
            dp.ParseFromString(g)
        if args.cigar:
            debug_output(dp)
        if args.stat:
            print(calc_stats(dp))
    else:
        raise ValueError(f"Not sure what to do with {args.file}")


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("file", help="file name to inspect")
    parser.add_argument(
        "--stat", help="Basic file stats", action="store_true", default=True
    )
    parser.add_argument(
        "--cigar", help="Display CIGAR alignment", action="store_true"
    )
    parser.set_defaults(func=run)
