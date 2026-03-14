import argparse
from pathlib import Path
import sys

from cleany.cleany import Cleany

def parse_args():
    parser = argparse.ArgumentParser(description="Clean up your comments")
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Path to the directory containing Python files (default: current directory)",
    )
    parser.add_argument(
        "--ignore-dir",
        action="append",
        default=[],
        help="ignore matching directories"
    )
    parser.add_argument(
        "--ignore-file",
        action="append",
        default=[],
        help="ignore matching files"
    )
    parser.add_argument(
        "--nuke",
        action="store_true",
        help="Removes ALL comments",
    )
    parser.add_argument(
        "--emoji", 
        action="store_true", 
        help="Removes emojis"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="surpress output"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if len(sys.argv) == 1:
        return print("cleany -h for help")
    
    ignore_dir = ["venv"]
    for ignored in args.ignore_dir:
        ignore_dir.append(ignored)

    ignore_file = []
    for ignored in args.ignore_file:
        ignore_file.append(ignored)
    
    cleany = Cleany(
        path=args.path,
        ignore_dir=ignore_dir,
        ignore_file=ignore_file,
        nuke=args.nuke,
        emoji=args.emoji,
        quiet=args.quiet
        )
    cleany.main_loop()