# Cleany

![tests](https://github.com/weddleben/cleany/actions/workflows/cleany.yml/badge.svg)
![GitHub issues](https://img.shields.io/github/issues/weddleben/cleany.png)
![last-commit](https://img.shields.io/github/last-commit/weddleben/cleany)
![Supported Versions](https://img.shields.io/pypi/pyversions/cleany.svg)

A CLI tool to clean up your comments

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

### Remove all comments
````bash
$ cleany --nuke
````

### Remove emojis only:
````bash
$ cleany --emoji
````

### Change the path.
Cleany will search for `.py` files starting in your current directory and moving recursively down. If you would like to specify a directory, use `--path`:
````bash
$ cleany --nuke --path some-directory
````

### Ignore directory
If you want Cleany to skip a directory, use `--ignore-dir`:
````bash
$ cleany --emoji --ignore-dir some-directory
````
You can ignore multiple directories:
````bash
$ cleany --emoji --ignore-dir some-directory --ignore-dir another-directory
````

### Ignore file
If you want Cleany to skip a file, use `--ignore-file`:
````bash
$ cleany --nuke --ignore-file some_file.py
````
You do not need to include the full path to the file; just use the file name. Cleany will find and skip any file with that name.

### Surpress Cleany's output
By default Cleany will provide output about the files it's cleaning up. 
````bash
$ cleany --nuke
> ----- scanning comments in /src/main.py -----
> removing comment from line 85 of /src/main.py
> removing comment from like 115 of /src/main.py
> removed 2 comments from /src/main.py
````
If you want to surpress that output, use `--quiet`:
````bash
$ cleany --nuke --quiet
$ 
````