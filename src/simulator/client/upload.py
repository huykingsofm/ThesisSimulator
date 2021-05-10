import os
import argparse

from hks_pylib.done import Done

from simulator.utils import error
from simulator.client.tokenize import Tokenize
from simulator.configuration.client import ClientSimulator


def upload(simulator: ClientSimulator, utoken, path):
    result = simulator.sftsend(utoken, path)

    if result:
        return Done(True)

    return error(result)

class Upload:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument("path")
        self.tokenize = Tokenize(self.parser)


    def run(self, args):
        if os.path.isfile(args.path) is False:
            raise FileNotFoundError("File {} doesn't found.".format(args.path))

        simulator = ClientSimulator(args.client, args.channel)
        utoken = self.tokenize.run(simulator, args)
        result = upload(simulator, utoken, args.path)

        if result:
            print("Uploading successfully.")
        else:
            print(result.error)
