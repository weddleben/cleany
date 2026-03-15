import argparse
import sys

from cleany import Cleany, CleanyCLIArgs

def parse_args():
    parser = argparse.ArgumentParser(description="Cleany", allow_abbrev=False)
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Path to the directory you want cleany to inspect (default: current directory)",
    )
    parser.add_argument(
        "--ignore-dir",
        action="append",
        type=str,
        default=[],
        help="ignore matching directories"
    )
    parser.add_argument(
        "--ignore-file",
        action="append",
        type=str,
        default=[],
        help="ignore matching files"
    )
    parser.add_argument(
        "--nuke",
        action="store_true",
        help="Removes ALL comments from Python files",
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
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print the current version"
    )
    if len(sys.argv) == 1:
        print("cleany -h for help")
        sys.exit()
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.version:
        from importlib.metadata import version
        cleany_version = version("cleany")
        return print(f"Cleany v{cleany_version}")
    
    ignore_dir = ["venv"]
    for ignored in args.ignore_dir:
        ignore_dir.append(ignored)

    ignore_file = []
    for ignored in args.ignore_file:
        ignore_file.append(ignored)

    cleany_args = CleanyCLIArgs(
        path=args.path,
        ignore_dir=ignore_dir,
        ignore_file=ignore_file,
        nuke=args.nuke,
        emoji=args.emoji,
        quiet=args.quiet
    )
    
    cleany = Cleany(args=cleany_args)
    cleany.main_loop()