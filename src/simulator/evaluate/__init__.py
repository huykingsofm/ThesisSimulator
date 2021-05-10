import argparse

from simulator.evaluate.pdp import PDP
from simulator.evaluate.match import Match
from simulator.evaluate.encrypt import Encrypt


class Evaluate:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

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

        if args.operation == "encrypt":
            self.encrypt.run(args)

        if args.operation == "match":
            self.match.run(args)

        if args.operation == "pdp":
            self.pdp.run(args)
