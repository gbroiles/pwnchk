#! /usr/bin/env python3
# pylint: disable=invalid-name,missing-module-docstring,missing-function-docstring
import argparse
import os
import sys
import pprint
import requests
from time import sleep
from rich.progress import track

table = False
found = []
notfound = []


def create_parse():
    parser = argparse.ArgumentParser(
        description="Have I Been Pwned bulk addess checker"
    )
    parser.add_argument("--table", help="output result as tables", action="store_true")
    parser.add_argument(
        "filename", help="file(s) with email addresses to scan", nargs="+"
    )
    return parser


def checkit(filename, apikey):
    global table
    global found
    global notfound
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
    headers = {"hibp-api-key": apikey, "user-agent": "HIBP bulk checker / 0.1"}

    with open(filename, "r") as f:
        addrs = f.read().splitlines()

    for addr in track(addrs, description="Processing.."):
        target = url + addr
        if not table:
            print(addr, end=" ")
        response = requests.get(target, headers=headers)
        if response.status_code == 200:
            found.append(addr)
            if not table:
                print("breach(es) found")
        elif response.status_code == 404:
            notfound.append(addr)
            if not table:
                print("no breaches found")
        else:
            if not table:
                pprint.pprint(response.json())
        sleep(1.6)


def start():
    global table
    parser = create_parse()
    args = parser.parse_args()
    try:
        apikey = os.environ["HIBPAPI"]
    except KeyError:
        print("Must set HIBPAPI key enviroment variable.")
        print("See https://haveibeenpwned.com/API/Key to purchase a key.")
        sys.exit(1)

    table = args.table

    for item in args.filename:
        checkit(item, apikey)

    if table:
        print("Found ", len(found), " ----------------------------------------")
        for i in found:
            print(i)
        print("Missing ", len(notfound), " ----------------------------------------")
        for i in notfound:
            print(i)


if __name__ == "__main__":
    start()
