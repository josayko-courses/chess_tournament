# chess_tournament

> Python web developer course project 03:
> Manage a chess tournament with a Swiss-system for pairing the players

## Get Started

`python >= 3.6` and `venv` are needed.

### Virtual Environment

```bash
$ python -m venv env
$ source env/bin/activate
```

### Required packages

```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

### Generate flake8-html report

Generate the report file in `chess_tournament/flake_report/index.html`.

```bash
# from project root directory
$ cd chess_tournament/
$ python -m flake8 --format=html --htmldir=flake-report
```

## How to run the program

```bash
# from project root directory
$ cd chess_tournament/
$ python chess_tournament.py
```
