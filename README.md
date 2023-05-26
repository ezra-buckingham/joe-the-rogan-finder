# Joe the Rogan Finder

A simple python script that will check for tickets becoming available on Joe Rogan's website and notify a Discord server of tickets becoming available.

## Getting Started

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Usage is simple, even a dummy Willy Joe can use it!

```
Usage: main.py [OPTIONS]

Options:
  -d, --date TEXT  Date to check for on the website (ex. "Monday, Oct 23")
                   [required]
  -u, --url TEXT   Discord URL to notify when found  [required]
  --help           Show this message and exit.
```