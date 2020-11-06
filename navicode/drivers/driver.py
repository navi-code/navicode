import argparse

from navicode.drivers.cli.cli import *

def navigate():
    parser = argparse.ArgumentParser(description="NaviCode command line tool")
    parser.add_argument("init",  nargs="?", default="noinit", type=str, help="Initialize navicode in your repository")
    args = parser.parse_args()

    if args.init == "init":
        navicode_init()

