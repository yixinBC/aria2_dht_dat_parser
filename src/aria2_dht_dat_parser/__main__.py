import argparse
import sys
import json
from .parser import parse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", help="input dht.dat file", required=True)
    arg_parser.add_argument(
        "-o", help="output file", type=argparse.FileType("w"), default=sys.stdout
    )
    args = arg_parser.parse_args()
    args.o.write(json.dumps(parse(args.i), indent=2))


if __name__ == "__main__":
    main()
