import argparse


from simulator.client.utils import get_token
from simulator.client.authenticate import authenticate
from simulator.configuration.client import ClientSimulator

def is_same(a, b):
    if a is None and b is not None:
        return False

    if a is not None and b is None:
        return False

    return True

class Tokenize:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        account_auth_group = self.parser.add_argument_group("Account authentication")
        token_auth_group = self.parser.add_argument_group("Token authentication")

        account_auth_group.add_argument(
                "--username",
                "-u",
                help="The username in account authentication.",
                default=None
            )

        account_auth_group.add_argument(
                "--password",
                "-p",
                help="The password in account authentication",
                default=None
            )

        token_auth_group.add_argument(
                "--token",
                "-t",
                help="The token is received by authentication.",
                default=None
            )

    def run(self, simulator: ClientSimulator, args):
        method_counter = 0

        if args.username is not None and args.password is not None:
            method_counter += 1

        if args.token is not None:
            method_counter += 1

        if method_counter > 1:
            raise Exception("Only choose an authentication method")

        if not is_same(args.username, args.password):
            raise Exception("The username and password must "
            "be passed together in account authentication.")

        if method_counter == 0:
            raise Exception("Please choose an authentication method (account or token)")

        if args.username and args.password:
            result = authenticate(simulator, args.username, args.password)

            if result:
                return result.token

            raise Exception("Authentication failed")

        else:
            return get_token(args.token)
