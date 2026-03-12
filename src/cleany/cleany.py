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
            return print(f"cannot find matching directory: {self.path}")
        if len(self.list_of_files) == 0:
            return print(f"no files found in {self.path}")
        for file in self.list_of_files:
            if self.nuke:
                self.nuke_comments(file)
            if self.emoji:
                self.remove_emojis(file)
                self.print_to_screen(f"removed {self.total_emojis_removed} emojis")
    def file_is_skippable(self, file: Path):
            if not file.is_file():
                return True
            if any(part.startswith(".") for part in file.parent.parts):
                return True
            if str(file).endswith(".pyc"):
                return True
            if any(part in self.ignore_dir for part in file.parent.parts):
                return True
            if any(str(file).endswith(to_ignore) for to_ignore in self.ignore_file):
                return True

    def create_list_of_files(self) -> list[Path]:
        list_of_files: list = []
        for file in self.path.rglob("*"):
            if self.file_is_skippable(file):
                continue
            else:
                list_of_files.append(file)
        return list_of_files

    def nuke_comments(self, path: Path):
        if not path.suffix == ".py":
            return
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
        tokens = path.read_text(encoding="utf-8", errors="ignore").splitlines()

        new_tokens = []

        for token in tokens:
            if token == "":
                new_tokens.append(token)
                continue
            new_string = self.replace_emojis_in_comment(text=token, path=path)
            new_tokens.append(new_string)

        if tokens == new_tokens:
            self.print_to_screen(f"----- no emojis found in {path} -----")
            self.print_to_screen(statement="")
            return

        path.write_text("\n".join(new_tokens))
        if path.suffix == ".py":
            self.run_ruff(path=path)

    def replace_emojis_in_comment(self, path: Path, text: str, replacement: str = "") -> str:
        graphemes = grapheme_pattern.findall(text)
        new_parts = []
        for g in graphemes:
            if emoji_pattern.search(g):
                new_parts.append(replacement)
                self.print_to_screen(f"removing {g} from {path}")
                self.total_emojis_removed += 1
            else:
                new_parts.append(g)
        return "".join(new_parts)
    
    def run_ruff(self, path: Path):
        subprocess.run(["ruff", "format", "--silent", str(path)], check=True)

    def print_to_screen(self, statement):
        if not self.quiet:
            print(statement)