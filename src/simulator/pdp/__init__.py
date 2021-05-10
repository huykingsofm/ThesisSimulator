import os
import re
import argparse

from hks_pylib.cryptography.ciphers.keygenerator import KeyGenerator

from _simulator.base.pdp import ClientPDP
from _simulator.base.key import MasterKey


class PDP:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument(
                "input",
                help="The file path is passed to proof generator by PDP."
            )

        self.parser.add_argument(
                "output",
                help="The file path is used to contain all generated proofs."
            )

        parser.add_argument(
                "--password",
                "-p",
                help="The password is used to generate the proofs.",
                default=None
            )

        self.parser.add_argument(
                "-d",
                help="The total number of blocks which "
                "you want to divide the file.",
                type=int,
                default=None
            )

        self.parser.add_argument(
                "-r",
                help="The number of blocks which you "
                "want to generate the digest (expected r < d).",
                type=int,
                default=None
            )

        self.parser.add_argument(
                "--indices",
                "-i",
                help="The range of index is used to "
                "generate the digest. The format is "
                "[start-end]. It is expected that "
                "start and end are the non-negative "
                "numbers. Note that the range is include "
                "both end points. Example: [0-5], is "
                "equipvalent to indices 0, 1, 2, 3, 4, and 5. "
                "By default, indices is [0-99].",
                default="[0-99]"
            )


    def run(self, args):
        if os.path.isfile(args.input) is False:
            raise FileNotFoundError("File {} isn't found.".format(args.input))

        if args.password is None:
            raise Exception("Password is required")

        pattern = r"^\[(\d+)-(\d+)\]$"
        match = re.match(pattern, args.indices)

        if match is None:
            raise Exception("Invalid indices")

        low = int(match.groups()[0])
        high = int(match.groups()[1])

        if low > high:
            raise Exception("Invalid indices")

        key = KeyGenerator(32).pwd2key(args.password)
        master_key = MasterKey(key)

        pdp = ClientPDP(args.input, r=args.r, d=args.d)
        pdp.save(args.output, master_key, range(low, high+1))

        print("Proof is saved at {}.".format(args.output))
