import subprocess
import tokenize
import regex
from pathlib import Path

from pydantic import BaseModel, Field

class CleanyCLIArgs(BaseModel):
    path: Path
    ignore_dir: list = Field(default_factory=list)
    ignore_file: list = Field(default_factory=list)
    nuke: bool = False
    emoji: bool = False
    quiet: bool = False


class Cleany(BaseModel):
    args: CleanyCLIArgs
    list_of_files: list[Path] = Field(default_factory=list)
    total_emojis_removed: int = 0
    files_with_emojis_removed: int = 0
    total_comments_removed: int = 0
    files_with_comments_removed: int = 0

    def model_post_init(self, __context):
        self.list_of_files = self.create_list_of_files()

    def main_loop(self):
        if not any([self.args.nuke, self.args.emoji]):
            return print("no modification commands")
        if not self.args.path.exists():
            return print(f"cannot find matching directory: {self.args.path}")
        if len(self.list_of_files) == 0:
            return print(f"no files found in {self.args.path}")
        if self.args.nuke:
            self.nuke_comments()
            self.print_to_screen(
                statement=f"removed {self.total_comments_removed} comments from {self.files_with_comments_removed} files"
                )
        if self.args.emoji:
            self.remove_emojis()
            self.print_to_screen(
                f"removed {self.total_emojis_removed} emojis from {self.files_with_emojis_removed} files"
                )

    def file_is_skippable(self, file: Path):
        if not file.is_file():
            return True
        if any(part.startswith(".") for part in file.parent.parts):
            return True
        if str(file).endswith(".pyc"):
            return True
        if any(part in self.args.ignore_dir for part in file.parent.parts):
            return True
        if any(str(file).endswith(to_ignore) for to_ignore in self.args.ignore_file):
            return True
        if self.is_not_utf8(file=file):
            return True

    def is_not_utf8(self, file: Path):
        with file.open("rb") as f:
            chunk = f.read(4000)
        if b"\x00" in chunk:
            return True
        try:
            chunk.decode("utf-8")
            return False
        except UnicodeDecodeError:
            return True

    def create_list_of_files(self) -> list[Path]:
        self.print_to_screen(statement=f"----- Scanning files in {self.args.path.absolute()} -----")
        list_of_files: list = []
        for file in self.args.path.rglob("*"):
            if self.file_is_skippable(file):
                continue
            else:
                list_of_files.append(file)
        number_of_files: int = len(list_of_files)
        self.print_to_screen(statement=f"----- found {number_of_files} valid files in {self.args.path.absolute()} -----")
        return list_of_files

    def nuke_comments(self):
        paths: list[Path] = self.list_of_files
        self.print_to_screen(statement=f"----- --nuke is only valid for Python files -----")

        total_python_files: int = 0
        for path in paths:
            if path.suffix == ".py":
                total_python_files +=1
        self.print_to_screen(statement=f"----- found {total_python_files} Python files -----")

        for path in paths:
            if not path.suffix == ".py":
                continue
            self.print_to_screen(f"----- scanning comments in {path} -----")
            total_removed: int = 0
            with open(path, "rb") as f:
                tokens = list(tokenize.tokenize(f.readline))

            new_tokens = []

            for token in tokens:
                if token.type == tokenize.COMMENT:
                    self.print_to_screen(
                        f"removing comment from line {token.start[0]} of {path}"
                    )
                    total_removed += 1
                    self.total_comments_removed +=1
                    continue
                else:
                    new_tokens.append(token)

            if tokens == new_tokens:
                self.print_to_screen(f"----- no comments found in {path} -----")
                self.print_to_screen(statement="")
                continue
            
            self.files_with_comments_removed += 1
            self.print_to_screen(f"removed {total_removed} comments from {path}")
            new_source = tokenize.untokenize(new_tokens)
            path.write_bytes(new_source)
            self.run_ruff(path=path)

    def remove_emojis(self):
        self.print_to_screen(statement="")
        paths: list[Path] = self.list_of_files
        for path in paths:
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
                continue

            self.print_to_screen(statement="")
            self.files_with_emojis_removed += 1
            path.write_text("\n".join(new_tokens))
            if path.suffix == ".py":
                self.run_ruff(path=path)

    def replace_emojis_in_comment(self, path: Path, text: str, replacement: str = "") -> str:
        grapheme_pattern = regex.compile(r"\X", regex.UNICODE)
        emoji_pattern = regex.compile(r"\p{Extended_Pictographic}")
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
        if not self.args.quiet:
            print(statement)
