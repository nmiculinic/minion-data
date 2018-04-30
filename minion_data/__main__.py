import argparse
from typing import NamedTuple
import sys
from . import preparation, inspect


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
        sys.exit(args.func(args))
    else:
        parser.print_help()
        sys.exit(2)
