import argparse

from hks_pylib.done import Done

from _simulator.protocol.definition import ThesisProtocols

from simulator.utils import error
from simulator.client.utils import get_token
from simulator.configuration.client import ClientSimulator


def match(simulator: ClientSimulator, ftoken1, ftoken2):
    client = simulator.connect()
    try:
        client.activate(
                ThesisProtocols.MATCH,
                token1=ftoken1,
                token2=ftoken2
            )

        result = client.wait_result(ThesisProtocols.MATCH, timeout=5)

        if result == None:
            result = Done(False, reason="Timeout")

    except Exception as e:
        result = Done(False, reason=str(e))
    finally:
        client.close()

    if result != True:
        return error(result)

    return Done(True, similarity=result.similarity)


class Match:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument("token1", help="The token or path of token of file 1")
        self.parser.add_argument("token2", help="The token or path of token of file 2")

    def run(self, args):
        token1 = get_token(args.token1)
        token2 = get_token(args.token2)

        simulator = ClientSimulator(args.client, args.channel)

        result = match(simulator, token1, token2)

        if result:
            print("The similarity score of "
            "two files is {:.2f}%".format(result.similarity * 100))
        else:
            print(result.error)
