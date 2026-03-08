import os
from pathlib import Path
import subprocess

import pytest

def test_init_1():
    '''if nothing passed in, should return default help message'''
    output = subprocess.run("cleany", capture_output=True)
    assert "help" in str(output.stdout)

def test_init_2():
    '''runs...'''
    subprocess.run(["cleany", "--nuke"])

def test_init_3():
    '''wrong type passed to path. should be str'''
    with pytest.raises(Exception):
        subprocess.run(["cleany", "--path", 2])

def test_init_4():
    '''if no modification commands passed (emoji, nuke, etc)'''
    output = subprocess.run(["cleany", "--path", "some_dir"], capture_output=True)
    assert "no modification commands" in str(output.stdout)

def test_init_5():
    '''if no modification commands passed (emoji, nuke, etc)'''
    output = subprocess.run(["cleany", "--ignore-dir", "some_dir"], capture_output=True)
    assert "no modification commands" in str(output.stdout)

def test_init_6():
    '''passing in non-existent directory'''
    output = subprocess.run(["cleany", "--path", "doesnt_exist", "--nuke"], capture_output=True)
    assert "cannot find matchign directory" in str(output.stdout)

def test_init_7(tmp_path):
    '''specifying directory with no matching python files'''
    output = subprocess.run(["cleany", "--path", tmp_path, "--nuke"], capture_output=True)
    print(tmp_path)
    assert "no files found in" in str(output.stdout)

def test_remove_emojis_1(tmp_path):
    pre = Path("tests/fixtures/pre-clean-emojis.py")
    post = Path("tests/fixtures/post-clean-emojis.py")

    temp: Path = tmp_path / "emoji.py"
    temp.write_text(pre.read_text())

    subprocess.run(["cleany", "--emoji", "--path", tmp_path])

    assert temp.read_text() == post.read_text()

def test_nuke_1(tmp_path):
    pre = Path("tests/fixtures/pre-clean-nuke.py")
    post = Path("tests/fixtures/post-clean-nuke.py")

    temp: Path = tmp_path / "nuke.py"
    temp.write_text(pre.read_text())

    subprocess.run(["cleany", "--nuke", "--path", tmp_path])

    assert temp.read_text() == post.read_text()