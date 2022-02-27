#! /usr/bin/env python3
# pylint: disable=invalid-name,missing-module-docstring,missing-function-docstring
import argparse
import os
import sys
import pprint
import requests
from time import sleep


def create_parse():
    parser = argparse.ArgumentParser(
        description="Have I Been Pwned bulk addess checker"
    )
    parser.add_argument(
        "filename", help="file(s) with email addresses to scan", nargs="+"
    )
    return parser


def checkit(filename, apikey):
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/"
    headers = {"hibp-api-key": apikey, "user-agent": "HIBP bulk checker / 0.1"}

    with open(filename, "r") as f:
        addrs = f.read().splitlines()

    for addr in addrs:
        target = url + addr  # + "?truncateResponse=false"
        print(addr, end=" ")
        response = requests.get(target, headers=headers)
        if response.status_code == 200:
            print("breach(es) found")
        elif response.status_code == 404:
            print("no breaches found")
        else:
            pprint.pprint(response.json())
        #        print()
        sleep(1.6)


def start():
    parser = create_parse()
    args = parser.parse_args()
    try:
        apikey = os.environ["HIBPAPI"]
    except KeyError:
        print("Must set HIBPAPI key enviroment variable.")
        print("See https://haveibeenpwned.com/API/Key to purchase a key.")
        sys.exit(1)

    for item in args.filename:
        checkit(item, apikey)


if __name__ == "__main__":
    start()
