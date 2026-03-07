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