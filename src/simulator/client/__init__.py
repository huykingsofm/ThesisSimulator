import argparse


from simulator.client.check import Check
from simulator.client.match import Match
from simulator.client.search import Search
from simulator.client.upload import Upload
from simulator.client.download import Download
from simulator.client.authenticate import Authenticate


class Client:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser        

        self.parser.add_argument(
                "--client",
                help="The path of client configuration "
                "json file (by default, client.json).",
                default="client.json"
            )

        self.parser.add_argument(
                "--channel",
                help="The path of channel configuration "
                "json file (by default, channel.json).",
                default="channel.json"
            )

        action = self.parser.add_subparsers(title="action")

        authenticate_parser = action.add_parser("authenticate")
        authenticate_parser.set_defaults(action="authenticate")
        self.authenticate = Authenticate(authenticate_parser)

        upload_parser = action.add_parser("upload")
        upload_parser.set_defaults(action="upload")
        self.upload = Upload(upload_parser)

        download_parser = action.add_parser("download")
        download_parser.set_defaults(action="download")
        self.download = Download(download_parser)

        check_parser = action.add_parser("check")
        check_parser.set_defaults(action="check")
        self.check = Check(check_parser)

        match_parser = action.add_parser("match")
        match_parser.set_defaults(action="match")
        self.match = Match(match_parser)

        search_parser = action.add_parser("search")
        search_parser.set_defaults(action="search")
        self.search = Search(search_parser)

    def run(self, args):
        if not hasattr(args, "action"):
            self.parser.print_help()
            return

        if args.action == "authenticate":
            self.authenticate.run(args)

        if args.action == "upload":
            self.upload.run(args)

        if args.action == "download":
            self.download.run(args)

        if args.action == "check":
            self.check.run(args)

        if args.action == "match":
            self.match.run(args)

        if args.action == "search":
            self.search.run(args)
