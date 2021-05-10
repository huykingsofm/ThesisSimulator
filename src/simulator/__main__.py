import argparse
from simulator.file import File

from simulator.pdp import PDP
from simulator.server import Server
from simulator.client import Client
from simulator.encrypt import Encrypt
from simulator.evaluate import Evaluate


class Simulator:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        engine = self.parser.add_subparsers(title="engine")

        server_parser = engine.add_parser("server")
        server_parser.set_defaults(engine="server")
        self.server = Server(server_parser)

        client_parser = engine.add_parser("client")
        client_parser.set_defaults(engine="client")
        self.client = Client(client_parser)

        encrypt_parser = engine.add_parser("encrypt")
        encrypt_parser.set_defaults(engine="encrypt")
        self.encrypt = Encrypt(encrypt_parser)

        pdp_parser = engine.add_parser("pdp")
        pdp_parser.set_defaults(engine="pdp")
        self.pdp = PDP(pdp_parser)

        evaluate_parser = engine.add_parser("evaluate")
        evaluate_parser.set_defaults(engine="evaluate")
        self.evaluate = Evaluate(evaluate_parser)

        file_parser = engine.add_parser("file")
        file_parser.set_defaults(engine="file")
        self.file = File(file_parser)

    def run(self, args):
        if not hasattr(args, "engine"):
            parser.print_help()
            return

        try:
            if args.engine == "server":
                self.server.run(args)

            if args.engine == "client":
                self.client.run(args)

            if args.engine == "encrypt":
                self.encrypt.run(args)

            if args.engine == "pdp":
                self.pdp.run(args)

            if args.engine == "evaluate":
                self.evaluate.run(args)

            if args.engine == "file":
                self.file.run(args)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    simulator = Simulator(parser)

    args = parser.parse_args()

    simulator.run(args)
