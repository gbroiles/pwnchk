#! /usr/bin/env python3
# pylint: disable=invalid-name,missing-module-docstring,missing-function-docstring
import argparse
import pwnedpasswords
from rich.progress import track

found = []
notfound = []
table = False
entries = []


def create_parse():
    parser = argparse.ArgumentParser(
        description="Have I Been Pwned bulk password checker"
    )
    parser.add_argument("--table", help="output result as tables", action="store_true")
    parser.add_argument("filename", help="file(s) with passwords to scan", nargs="+")
    return parser


def load_list(entries, filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
    for line in lines:
        entries.append(line)


def checkit(pws):
    global table
    for pw in track(pws, description="Processing.."):
        if not table:
            print(pw, end=" ")
        r = pwnedpasswords.check(pw)
        if r > 0:
            found.append(pw)
            if not table:
                print("found")
        else:
            notfound.append(pw)
            if not table:
                print("missing")


def start():
    global table
    global entries
    parser = create_parse()
    args = parser.parse_args()

    table = args.table

    for item in args.filename:
        load_list(entries, item)

    entries = list(set(entries))
    entries.sort()

    checkit(entries)

    if table:
        print("Found ", len(found), " ----------------------------------------")
        for i in found:
            print(i)
        print("Missing ", len(notfound), " ----------------------------------------")
        for i in notfound:
            print(i)


if __name__ == "__main__":
    start()
