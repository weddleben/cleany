from cleany import remove_emojis, nuke_comments

from pathlib import Path
def test_remove_emojis_1(tmp_path):
    pre = Path("tests/fixtures/pre-clean-emojis.py")
    post = Path("tests/fixtures/post-clean-emojis.py")

    temp: Path = tmp_path / "emoji.py"
    temp.write_text(pre.read_text())

    remove_emojis(temp)

    assert temp.read_text() == post.read_text()

def test_nuke_1(tmp_path):
    pre = Path("tests/fixtures/pre-clean-nuke.py")
    post = Path("tests/fixtures/post-clean-nuke.py")

    temp: Path = tmp_path / "nuke.py"
    temp.write_text(pre.read_text())

    nuke_comments(temp)

    assert temp.read_text() == post.read_text()