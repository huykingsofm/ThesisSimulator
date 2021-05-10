import argparse

from hks_pylib.done import Done

from _simulator.protocol.definition import ThesisProtocols

from simulator.utils import error
from simulator.client.tokenize import Tokenize
from simulator.configuration.client import ClientSimulator


def search(simulator: ClientSimulator, utoken, filename):
    client = simulator.connect()
    try:
        client.activate(
                ThesisProtocols.SEARCH,
                token=utoken,
                filename=filename
            )

        result = client.wait_result(ThesisProtocols.SEARCH, timeout=5)

        if result == None:
            result = Done(False, reason="Timeout")

    except Exception as e:
        result = Done(False, reason=str(e))
    finally:
        client.close()

    if result != True:
        return error(result)

    return Done(True, token=result.token)


class Search:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument(
                "filename",
                help="The filename which you want to get the token."
            )

        self.tokenize = Tokenize(self.parser)

    def run(self, args):
        simulator = ClientSimulator(args.client, args.channel)

        utoken = self.tokenize.run(simulator, args)

        result = search(simulator, utoken, args.filename)

        if result:
            print("Please keep the file token carefully. "
            "Your file token is:\n{}".format(result.token))
        else:
            print(result.error)
