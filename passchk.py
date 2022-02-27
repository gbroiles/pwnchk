#! /usr/bin/env python3
# pylint: disable=invalid-name,missing-module-docstring,missing-function-docstring
import argparse
import pwnedpasswords

def create_parse():
    parser = argparse.ArgumentParser(description="Have I Been Pwned bulk password checker")
    parser.add_argument("filename", help="file(s) with passwords to scan", nargs="+")
    return parser

def checkit(filename):
    with open(filename,"r") as f:
        pws = f.read().splitlines()
    for pw in pws:
        print(pw, end=' ')
        r = pwnedpasswords.check(pw)
        if r > 0:
            print("breach(es) found")
        else:
            print("not found")

def start():
    parser = create_parse()
    args = parser.parse_args()

    for item in args.filename:
        checkit(item)

if __name__ == "__main__":
    start()
