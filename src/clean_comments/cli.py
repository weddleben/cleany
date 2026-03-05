import argparse
import subprocess
import sys
import tokenize
from tokenize import TokenInfo
import regex
from pathlib import Path

grapheme_pattern = regex.compile(r"\X", regex.UNICODE)
emoji_pattern = regex.compile(r"\p{Extended_Pictographic}")


def replace_emojis_in_comment(text: TokenInfo, replacement: str = "") -> str:
    graphemes = grapheme_pattern.findall(text.string)
    new_parts = []
    global total_removed
    for g in graphemes:
        if emoji_pattern.search(g):
            new_parts.append(replacement)
            print(f"removing {g} from line {text.start[0]}")
        else:
            new_parts.append(g)
    return "".join(new_parts)


def nuke_comments(path: Path):
    print(f"----- scanning comments in {path} -----")
    total_removed: int = 0
    with open(path, "rb") as f:
        tokens = list(tokenize.tokenize(f.readline))

    new_tokens = []

    for token in tokens:
        if token.type == tokenize.COMMENT:
            print(f"removing comment from line {token.start[0]} of {path}")
            total_removed += 1
            pass
        else:
            new_tokens.append(token)

    if tokens == new_tokens:
        print(f"----- no comments found in {path} -----")
        print()
        return

    print(f"removed {total_removed} comments from {path}")
    new_source = tokenize.untokenize(new_tokens)
    path.write_bytes(new_source)
    run_ruff(path=path)


def run_ruff(path: Path):
    subprocess.run(["ruff", "format", "--silent", str(path)], check=True)


def remove_emojis(path: Path):
    print(f"----- scanning comments in {path} -----")
    with open(path, "rb") as f:
        tokens = list(tokenize.tokenize(f.readline))

    new_tokens = []

    for token in tokens:
        if token.type == tokenize.COMMENT:
            new_comment = replace_emojis_in_comment(token)
            token = tokenize.TokenInfo(
                token.type,
                new_comment,
                token.start,
                token.end,
                token.line,
            )
        new_tokens.append(token)

    if tokens == new_tokens:
        print(f"----- no emojis found in {path} -----")
        print()
        return

    new_source = tokenize.untokenize(new_tokens)
    path.write_bytes(new_source)
    run_ruff(path=path)


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
        return print("clean -h for help")

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
