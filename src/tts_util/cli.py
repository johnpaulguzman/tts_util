import argparse
import logging
from typing import Optional, Sequence
from .macro_util import start


def _configure_logging(level_str: str = "INFO") -> None:
    level_str = level_str.upper()
    level_map = logging.getLevelNamesMapping()
    if level_str not in level_map:
        raise ValueError(f"Unsupported log level: {level_str}")
    level = level_map[level_str]
    format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    logging.basicConfig(level=level, format=format)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ttsu")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"),
        help="Set logging verbosity.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="up",
        choices=("up", "start"),
        help="Start the global-hotkey TTS service (blocks until exit).",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Start the floating GUI trigger controller instead of hotkeys.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    _configure_logging(args.log_level)

    if args.command in ("up", "start"):
        start(use_gui=args.gui)
        return 0

    parser.print_help()
    return 2
