import argparse

from numpy import mean, std

from simulator.evaluate.pdp import PDP
from simulator.evaluate.match import Match
from simulator.evaluate.encrypt import Encrypt


class Evaluate:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument(
                "--round",
                help="The number of rounds which you want to perform "
                "the evaluation. By default, round is 10.",
                type=int,
                default=10
            )

        operation = self.parser.add_subparsers(title="operation")

        encrypt_parser = operation.add_parser("encrypt")
        encrypt_parser.set_defaults(operation="encrypt")
        self.encrypt = Encrypt(encrypt_parser)

        match_parser = operation.add_parser("match")
        match_parser.set_defaults(operation="match")
        self.match = Match(match_parser)

        pdp_parser = operation.add_parser("pdp")
        pdp_parser.set_defaults(operation="pdp")
        self.pdp = PDP(pdp_parser)

    def run(self, args):
        if not hasattr(args, "operation"):
            self.parser.print_help()
            return

        elapsed_time = []

        for i in range(args.round):
            if args.operation == "encrypt":
                cost = self.encrypt.run(args)

            if args.operation == "match":
                cost = self.match.run(args)

            if args.operation == "pdp":
                cost = self.pdp.run(args)

            elapsed_time.append(cost)
            print("Round {}: {:.3f}s".format(i + 1, cost))

        print("The avarage cost is {:.3f}s".format(mean(elapsed_time)))
        print("The standard deviation: {:.5f}s".format(std(elapsed_time)))