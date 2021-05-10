import os
import argparse


class File:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument("output")
        self.parser.add_argument(
                "--size",
                "-s",
                help="The size of output in MB. By default, size is 100.",
                default=100,
                type=int
            )

        self.parser.add_argument(
                "--blocksize",
                "-b",
                help="The block size when generate the file. "
                "By default, the block size is 65535 bytes",
                default=65535,
                type=int
            )

    def run(self, args):
        size = args.size * 1024 ** 2
        n = int(size/args.blocksize)
        with open(args.output, "wb") as f:
            for _ in range(n):
                block = os.urandom(args.blocksize)
                f.write(block)
