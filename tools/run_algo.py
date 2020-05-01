import argparse
import sys

from background_changer.config import get_cfg
from background_changer import process_data


def parse_args():
    """
    Parse the following arguments for the any change in params provided in config file.
    Args:
        cfg (str): path to the config file.
        opts (argument): provide addtional options from the command line, it
            overwrites the config loaded from file.
    """
    parser = argparse.ArgumentParser(
        description="Provide arguments for Background Change Pipeline."
    )

    parser.add_argument(
        "--cfg",
        dest="cfg_file",
        help="Path to the config file",
        default="configs/BIISC.yaml",
        type=str,
    )

    parser.add_argument(
        "opts",
        help="See background_changer/config/defaults.py for all options",
        default=None,
        nargs=argparse.REMAINDER,
    )
    if len(sys.argv) == 1:  # TODO: reconsider this
        parser.print_help()
    return parser.parse_args()


def load_config(args):
    """
    Given the arguments, load and initialize the configs.
    """
    cfg = get_cfg()

    if args.cfg_file is not None:
        cfg.merge_from_file(args.cfg_file)

    if args.opts is not None:
        cfg.merge_from_list(args.opts)

    if hasattr(args, "input_dir"):
        cfg.INPUT.DIR = args.input_dir
    if hasattr(args, "data_format"):
        cfg.DATA.FORMAT = args.data_format
    if hasattr(args, "output_dir"):
        cfg.OUTPUT.DIR = args.output_dir

    return cfg


def main():
    args = parse_args()
    cfg = load_config(args)

    process_data(cfg)


if __name__ == '__main__':
    main()
