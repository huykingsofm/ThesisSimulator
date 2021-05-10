import argparse

from hks_pylib.done import Done

from _simulator.protocol.definition import ThesisProtocols

from simulator.utils import error
from simulator.configuration.client import ClientSimulator


def authenticate(simulator: ClientSimulator, username, password):
    client = simulator.connect()
    try:
        client.activate(
                ThesisProtocols.AUTHENTICATION,
                username=username,
                password=password
            )
        result = client.wait_result(ThesisProtocols.AUTHENTICATION, timeout=5)

        if result is None:
            result = Done(False, error="Timeout")

    except Exception as e:
        result = Done(False, error=str(e))
    finally:
        client.close()

    if result:
        return Done(True, token=result.token)

    return error(result)

class Authenticate:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument("username")
        self.parser.add_argument("password")

    def run(self, args):
        simulator = ClientSimulator(args.client, args.channel)
        result = authenticate(simulator, args.username, args.password)
        if result:
            print("Please keep the token carefully. "
            "Your token is:\n{}".format(result.token))
        else:
            print(result.error)
