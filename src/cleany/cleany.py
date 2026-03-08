import subprocess
import tokenize
from tokenize import TokenInfo
import regex
from pathlib import Path

from pydantic import BaseModel, Field

grapheme_pattern = regex.compile(r"\X", regex.UNICODE)
emoji_pattern = regex.compile(r"\p{Extended_Pictographic}")

class Cleany(BaseModel):

    path: Path
    ignore_dir: list = Field(default_factory=list)
    ignore_file: list = Field(default_factory=list)
    nuke: bool = False
    emoji: bool = False
    quiet: bool = False
    list_of_files: list[Path] = Field(default_factory=list)
    total_emojis_removed: int = 0

    def model_post_init(self, __context):
        self.list_of_files = self.create_list_of_files()

    def main_loop(self):
        if not any([self.nuke, self.emoji]):
            return print("no modification commands")
        if not self.path.exists():
            return print(f"cannot find matchign directory: {self.path}")
        if len(self.list_of_files) == 0:
            return print(f"no files found in {self.path}")
        for file in self.list_of_files:
            if self.nuke:
                self.nuke_comments(file)
            if self.emoji:
                self.remove_emojis(file)
                self.print_to_screen(f"removed {self.total_emojis_removed} emojis")

    def create_list_of_files(self) -> list[Path]:
        list_of_files: list = []
        for file in self.path.rglob("*.py"):
            if any(part in self.ignore_dir for part in file.parent.parts):
                continue
            if any(str(file).endswith(to_ignore) for to_ignore in self.ignore_file):
                continue
            else:
                list_of_files.append(file)
        return list_of_files

    def nuke_comments(self, path: Path):
        self.print_to_screen(f"----- scanning comments in {path} -----")
        total_removed: int = 0
        with open(path, "rb") as f:
            tokens = list(tokenize.tokenize(f.readline))

        new_tokens = []

        for token in tokens:
            if token.type == tokenize.COMMENT:
                self.print_to_screen(f"removing comment from line {token.start[0]} of {path}")
                total_removed += 1
                pass
            else:
                new_tokens.append(token)

        if tokens == new_tokens:
            self.print_to_screen(f"----- no comments found in {path} -----")
            self.print_to_screen(statement="")
            return

        self.print_to_screen(f"removed {total_removed} comments from {path}")
        new_source = tokenize.untokenize(new_tokens)
        path.write_bytes(new_source)
        self.run_ruff(path=path)

    def remove_emojis(self, path: Path):
        self.print_to_screen(f"----- scanning comments in {path} -----")
        with open(path, "rb") as f:
            tokens = list(tokenize.tokenize(f.readline))

        new_tokens = []

        for token in tokens:
            if token.type == tokenize.COMMENT:
                new_comment = self.replace_emojis_in_comment(token)
                token = tokenize.TokenInfo(
                    token.type,
                    new_comment,
                    token.start,
                    token.end,
                    token.line,
                )
            new_tokens.append(token)

        if tokens == new_tokens:
            self.print_to_screen(f"----- no emojis found in {path} -----")
            self.print_to_screen(statement="")
            return

        new_source = tokenize.untokenize(new_tokens)
        path.write_bytes(new_source)
        self.run_ruff(path=path)

    def replace_emojis_in_comment(self, text: TokenInfo, replacement: str = "") -> str:
        graphemes = grapheme_pattern.findall(text.string)
        new_parts = []
        for g in graphemes:
            if emoji_pattern.search(g):
                new_parts.append(replacement)
                self.print_to_screen(f"removing {g} from line {text.start[0]}")
                self.total_emojis_removed += 1
            else:
                new_parts.append(g)
        return "".join(new_parts)
    
    def run_ruff(self, path: Path):
        subprocess.run(["ruff", "format", "--silent", str(path)], check=True)

    def print_to_screen(self, statement):
        if not self.quiet:
            print(statement)