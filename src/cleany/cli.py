import argparse
from pathlib import Path
import sys

from cleany.cleany import remove_emojis, nuke_comments

def parse_args():
    parser = argparse.ArgumentParser(description="Clean up your comments")
    parser.add_argument(
        "--nuke",
        action="store_true",
        help="Removes ALL comments",
    )
    parser.add_argument("--emoji", action="store_true", help="Removes emojis")
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Path to the directory containing Python files (default: current directory)",
    )
    parser.add_argument(
        "--ignore-dir",
        type=str,
        required=False,
        help="ignore matching directories"
    )

    parser.add_argument(
        "--ignore-file",
        type=str,
        required=False,
        help="ignore matching files"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if len(sys.argv) == 1:
        return print("cleany -h for help")

    if args.path:
        path = args.path
    else:
        path = "."

    ignore_dir = ["venv", "tests"]
    if args.ignore_dir:
        ignore_dir.append(args.ignore_dir)

    ignore_file = []
    if args.ignore_file:
        ignore_file.append(args.ignore_file)

    list_of_files = []

    for file in Path(path).rglob("*.py"):
        if any(part in ignore_dir for part in file.parent.parts):
            continue
        if any(str(file).endswith(to_ignore) for to_ignore in ignore_file):
            continue
        else:
            list_of_files.append(file)

    if args.emoji:
        for file in list_of_files:
            remove_emojis(file)
    if args.nuke:
        for file in list_of_files:
            nuke_comments(file)
