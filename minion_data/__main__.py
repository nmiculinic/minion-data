import argparse
from typing import NamedTuple
import sys
from minion_data import preparation, inspect
import logging
from tqdm import tqdm

class TqdmWrapper():
    def write(self, s):
        tqdm.write(s, end="")


class MinionDataCfg(NamedTuple):
    chiron_out: str
    sam_file: str
    out: str


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="minion_data")
    parser.add_argument("--debug", action="store_true")
    subparsers = parser.add_subparsers(
        title='sub command', help='sub command help'
    )
    preparation.add_args(
        subparsers.add_parser('prepare_dataset', description='Prepare dataset')
    )
    inspect.add_args(
        subparsers.add_parser(
            "inspect", description="Inspect specific datapoint"
        )
    )

    args = parser.parse_args()
    if hasattr(args, 'func'):
        root_logger = logging.getLogger()
        h = logging.StreamHandler(
            TqdmWrapper(),
        )
        h.setLevel(logging.DEBUG if args.debug else logging.INFO)
        h.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        root_logger.addHandler(h)
        sys.exit(args.func(args))
    else:
        parser.print_help()
        sys.exit(2)
