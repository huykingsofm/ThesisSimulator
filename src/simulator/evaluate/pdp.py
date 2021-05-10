import os
import time
import argparse

from numpy import std, mean

from hks_pylib.cryptography.ciphers.keygenerator import KeyGenerator

from _simulator.base.key import MasterKey
from _simulator.base.pdp import ClientPDP


class PDP:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument(
                "input",
                help="The file path is passed to proof generator by PDP."
            )

        self.parser.add_argument(
                "-d",
                help="The total number of blocks which "
                "you want to divide the file.",
                type=int,
                default=None
            )

        self.parser.add_argument(
                "-R",
                help="The number of blocks which you "
                "want to generate the digest (expected R < d).",
                type=int,
                default=None
            )

        self.parser.add_argument(
                "--nproof",
                "-n",
                help="The number of digest which you want to compute. By default, n is 100.",
                default=100,
                type=int
            )

        self.parser.add_argument(
                "--round",
                help="The number of rounds which you want to perform "
                "the evaluation. By default, round is 10.",
                type=int,
                default=10
            )

    def run(self, args):
        if os.path.isfile(args.input) is False:
            raise FileNotFoundError("File {} isn't found.".format(args.input))

        print("WARNING: -r is removed in this operation. "
        "-R is the number of blocks to be proved. "
        "--round is the number of rounds.")

        password = "default password"

        key = KeyGenerator(32).pwd2key(password)
        master_key = MasterKey(key)

        pdp = ClientPDP(args.input, r=args.R, d=args.d)
    
        elapsed_time = []

        for _ in range(args.round):
            start = time.time()
            pdp.save("evaluate.temp", master_key, range(args.nproof + 1))
            end = time.time()

            os.remove("evaluate.temp")
            elapsed_time.append(end - start)

        print("The average cost is {:.3f}s.".format(mean(elapsed_time)))
        print("The standard deviation is {:.5f}s.".format(std(elapsed_time)))
