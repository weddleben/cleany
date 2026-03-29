# Cleany

![tests](https://github.com/weddleben/cleany/actions/workflows/cleany.yml/badge.svg)
![GitHub issues](https://img.shields.io/github/issues/weddleben/cleany.png)
![last-commit](https://img.shields.io/github/last-commit/weddleben/cleany)
![Supported Versions](https://img.shields.io/pypi/pyversions/cleany.svg)

Cleany is a CLI tool to clean up your source files.

## Install
Install via pip
````bash
$ pip install cleany
````

## Invoke
Cleany is a command line tool. Once installed, invoke it from the command line:
````bash
$ cleany
> cleany -h for help
````

### Remove emojis:
````bash
$ cleany --emoji
````
Cleany will attempt to remove all emojis from all valid UTF-8 text files it finds.

IF cleany removes at least one emoji from a `.py` file, it will attempt to refactor the file using [Ruff](https://pypi.org/project/ruff/). Since this can significantly change the shape of your source files, you can disable Ruff:
````bash
$ cleany --emoji --no-ruff
````
If cleany does not remove an emoji from a Python file, it will not run Ruff against it.

### Change the path.
Cleany will search for files starting in your current directory and moving recursively down. If you would like to specify a directory, use `--path`:
````bash
$ cleany --emoji --path some-directory
````

### Ignore directory
If you want Cleany to skip directory, use `--ignore-dir`:
````bash
$ cleany --emoji --ignore-dir some-directory
````
You can ignore multiple directories:
````bash
$ cleany --emoji --ignore-dir some-directory --ignore-dir another-directory
````
By default cleany will skip hidden directories (directory names which begin with `.`) It will also skip the following directories:
- venv
- add more here
### Ignore file
If you want Cleany to skip a file, use `--ignore-file`:
````bash
$ cleany --nuke --ignore-file banana.js
````
You can ignore multiple files:
````bash
$ cleany --emoji --ignore-file banana.js --ignore-file palace.js
````
Do not include the full path to the file; just use the file name. Cleany will find and skip any file with that name.

### Remove comments from Python files
If cleany finds `.py` files, it can remove all `#` comments from them. Does not remove docstrings.
````bash
$ cleany --nuke
````
IF cleany removes at least one comment from a `.py` file, it will attempt to refactor the file using [Ruff](https://pypi.org/project/ruff/). Since this can significantly change the shape of your source files, you can disable Ruff:
````bash
$ cleany --nuke --no-ruff
````

If cleany does not remove a comment from a Python file, it will not run Ruff against it.

### Surpress Cleany's output
By default Cleany will provide output about the files it's cleaning up. 
````bash
$ cleany --nuke
> ----- scanning comments in /src/main.py -----
> removing comment from line 85 of /src/main.py
> removing comment from line 115 of /src/main.py
> removed 2 comments from /src/main.py
````
If you want to surpress that output, use `--quiet`:
````bash
$ cleany --nuke --quiet
$ 
````