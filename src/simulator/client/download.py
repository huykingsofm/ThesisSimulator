import argparse

from hks_pylib.done import Done

from simulator.utils import error
from simulator.configuration.client import ClientSimulator


def download(simulator: ClientSimulator, ftoken):
    result = simulator.sftrecv(ftoken)

    if result:
        return Done(True)

    return error(result)


class Download:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser
        
        self.parser.add_argument(
                "token",
                help="The file token of file which you want to download."
            )

    def run(self, args):
        simulator = ClientSimulator(args.client, args.channel)

        result = download(simulator, args.token)

        if result:
            print("Your file is downloaded successully")
        else:
            print(result.error)
