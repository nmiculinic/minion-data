import argparse
import logging
from os import path
from typing import NamedTuple
from .align_utils import get_target_sequences
import sys

class MinionDataCfg(NamedTuple):
    chiron_out: str
    sam_file: str

def main(cfg: MinionDataCfg):
    if not path.isfile(cfg.sam_file):
        raise ValueError(f"{cfg.sam_file} isn't a file")
    for name, v in get_target_sequences(cfg.sam_file).items():
        target, ref_name, start_pos, length, cigar_str = v  # target & cigar_str are important


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="minion_data")
    parser.add_argument("--default-root")
    parser.add_argument("--chiron-out")
    parser.add_argument("--sam_file")
    parser.add_argument("--debug", "-v", action="store_true")
    args = parser.parse_args()
    if args.default_root is not None:
        args.chiron_out = args.chiron_out or path.join(args.default_root, "chiron_out")
        args.sam_file = args.sam_file or path.join(args.default_root, "alignment.sam")
    if args.chiron_out is None or args.sam_file is None:
        print("Both chiron_out and sam_file must be defined (( or default_root ))")
        parser.print_help()
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)


    cfg = MinionDataCfg(
        chiron_out=path.abspath(args.chiron_out),
        sam_file=path.abspath(args.sam_file),
    )
    main(cfg)
