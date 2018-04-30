import argparse
from . import _chiron_out
from . import _signal_label

def add_args(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(
        help='Various dataset preparation utilities'
    )

    _chiron_out.add_args(subparsers.add_parser(
        name='chiron_out', help='Chiron out folder ( one with meta, raw, lable, signal, etc. subfolders)'
    ))

    _signal_label.add_args(subparsers.add_parser(
        name='signal_label', help='Prepare from bunch of .signal .label files', description=
        """Each .signal file hold N signal datapoints. Each .label file fold N rows, each row space separated from, to signal position and BasePair
        """
    ))
