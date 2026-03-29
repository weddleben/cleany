from pathlib import Path
import subprocess

def test_init_1():
    '''if nothing passed in, should return default help message'''
    output = subprocess.run("cleany", capture_output=True)
    assert "help" in str(output.stdout)

def test_init_2():
    '''runs...'''
    subprocess.run(["cleany", "--nuke"])

def test_invalid_arg_1():
    '''no value passed to --ignore-dir'''
    output = subprocess.run(["cleany", "--ignore-dir"], capture_output=True)
    assert output.returncode != 0

def test_invalid_arg_2():
    '''no value passed to --ignore-file'''
    output = subprocess.run(["cleany", "--ignore-file"], capture_output=True)
    assert output.returncode != 0

def test_invalid_arg_3():
    '''--nuke does not accept a value. It's a boolean'''
    output = subprocess.run(["cleany", "--nuke", "hahah"])
    assert output.returncode != 0

def test_invalid_arg_4():
    '''--emoji does not accept a value. It's a boolean'''
    output = subprocess.run(["cleany", "--emoji", "hahah"])
    assert output.returncode != 0

def test_no_mod_commands_1():
    '''if no modification commands passed (emoji, nuke, etc)'''
    output = subprocess.run(["cleany", "--path", "some_dir"], capture_output=True)
    assert "no modification commands" in str(output.stdout)

def test_no_mod_commands_2():
    '''if no modification commands passed (emoji, nuke, etc)'''
    output = subprocess.run(["cleany", "--ignore-dir", "some_dir"], capture_output=True)
    assert "no modification commands" in str(output.stdout)

def test_dir_not_exist():
    '''passing in non-existent directory'''
    output = subprocess.run(["cleany", "--path", "doesnt_exist", "--nuke"], capture_output=True)
    assert "cannot find matching directory" in str(output.stdout)

def test_emoty_dir_1(tmp_path):
    '''specifying directory with no matching files'''
    output = subprocess.run(["cleany", "--path", tmp_path, "--nuke"], capture_output=True)
    assert "no files found in" in str(output.stdout)

def test_empty_dir_2(tmp_path):
    '''specifying directory with no matching files'''
    output = subprocess.run(["cleany", "--path", tmp_path, "--emoji"], capture_output=True)
    assert "no files found in" in str(output.stdout)


def test_dir_without_python_files_1(tmp_path):
    '''specifying directory with files but no python files. should scan and find files, 
    but report that there are no python files when used with --nuke'''
    sample_text = "some sample text here"
    temp: Path = tmp_path / "del.txt"
    temp.write_text(sample_text)
    output = subprocess.run(["cleany", "--nuke", "--path", tmp_path], capture_output=True)
    assert "found 0 Python files" in str(output.stdout)

def test_expected_output_1():
    '''correct feedback is in the terminal output'''
    output = subprocess.run(["cleany", "--emoji"], capture_output=True)
    expected: list = ["removed", "emojis", "from", "files"]
    for segment in expected:
        assert segment in str(output.stdout)

def test_expected_output_2():
    '''correct feedback is in the terminal output'''
    output = subprocess.run(["cleany", "--nuke"], capture_output=True)
    expected: list = ["removed", "comments", "from", "files"]
    for segment in expected:
        assert segment in str(output.stdout)

def test_quiet_1():
    '''should be nothing in the terminal output if --quiet is passed'''
    output = subprocess.run(["cleany", "--nuke", "--quiet"], capture_output=True)
    output = str(output.stdout).strip("b''")
    assert len(str(output)) == 0

def test_quiet_2():
    '''should be nothing in the terminal output if --quiet is passed'''
    output = subprocess.run(["cleany", "--emoji", "--quiet"], capture_output=True)
    output = str(output.stdout).strip("b''")
    assert len(str(output)) == 0

def test_remove_emojis_1(tmp_path):
    pre = Path(".tests/fixtures/pre-clean-emojis.py")
    post = Path(".tests/fixtures/post-clean-emojis.py")

    temp: Path = tmp_path / "emoji.py"
    temp.write_text(pre.read_text())

    subprocess.run(["cleany", "--emoji", "--path", tmp_path])

    assert temp.read_text() == post.read_text()

def test_remove_emojis_no_ruff_1(tmp_path):
    pre = Path(".tests/fixtures/pre-clean-emojis.py")
    post = Path(".tests/fixtures/post-clean-emojis-no-ruff.py")

    temp: Path = tmp_path / "emoji_no_ruff.py"
    temp.write_text(pre.read_text())

    subprocess.run(["cleany", "--emoji", "--no-ruff", "--path", tmp_path])

    assert temp.read_text() == post.read_text()

def test_nuke_1(tmp_path):
    pre = Path(".tests/fixtures/pre-clean-nuke.py")
    post = Path(".tests/fixtures/post-clean-nuke.py")

    temp: Path = tmp_path / "nuke.py"
    temp.write_text(pre.read_text())

    subprocess.run(["cleany", "--nuke", "--path", tmp_path])

    assert temp.read_text() == post.read_text()

def test_nuke_no_ruff_1(tmp_path):
    pre = Path(".tests/fixtures/pre-clean-nuke.py")
    post = Path(".tests/fixtures/post-clean-nuke-no-ruff.py")

    temp: Path = tmp_path / "nuke-no-ruff.py"
    temp.write_text(pre.read_text())
    
    subprocess.run(["cleany", "--nuke", "--no-ruff", "--path", tmp_path])

    assert temp.read_text() == post.read_text()