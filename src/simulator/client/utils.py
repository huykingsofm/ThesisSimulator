from hks_pylib.done import Done

from _simulator.manager.token import PREFIX
from _simulator.protocol.definition import ThesisProtocols

from simulator.utils import error
from simulator.configuration.client import ClientSimulator


def search(simulator: ClientSimulator, utoken, filename):
    client = simulator.connect()
    try:
        client.activate(
                ThesisProtocols.SEARCH,
                filename=filename,
                token=utoken
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


def get_token(token):
    if token[: len(PREFIX)] == PREFIX:
        return token

    else:
        try:
            with open(token, "rt") as f:
                token = f.read()
        except FileNotFoundError:
            raise Exception("Invalid token")

        if token[: len(PREFIX)] != PREFIX:
            raise Exception("Invalid token")

        return token

