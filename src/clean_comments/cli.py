import argparse
import tokenize
from tokenize import TokenInfo
import regex
from pathlib import Path
import glob

total_removed:int = 0

grapheme_pattern = regex.compile(r'\X', regex.UNICODE)
emoji_pattern = regex.compile(r'\p{Extended_Pictographic}')

def replace_emojis_in_comment(text: TokenInfo, replacement: str = "") -> str:
    graphemes = grapheme_pattern.findall(text.string)
    new_parts = []
    global total_removed
    for g in graphemes:
        if emoji_pattern.search(g):
            new_parts.append(replacement)
            print(f"removing {g} from line {text.start[0]}")
            total_removed += 1
        else:
            new_parts.append(g)
    return "".join(new_parts)


def rewrite_file(path: Path):
    print(f"scanning comments in {path}")
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

    new_source = tokenize.untokenize(new_tokens)

    path.write_bytes(new_source)

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

    if args.path:
        path = args.path
    else:
        path = "."

    ignore_dir = ["venv", "something"]
    if args.ignore_dir:
        ignore_dir.append(args.ignore_dir)
    
    ignore_file = []
    if args.ignore_file:
        ignore_file.append(args.ignore_file)
     
    for file in Path(path).rglob("*.py"):
        if any(part in ignore_dir for part in file.parent.parts):
            continue
        if any(str(file).endswith(to_ignore) for to_ignore in ignore_file):
            continue
        else:
            rewrite_file(file)


    print(f"Removed {total_removed} emojis")