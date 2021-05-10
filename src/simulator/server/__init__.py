import argparse

from simulator.configuration.servers.thesis import ThesisServerSimulator
from simulator.configuration.servers.uploading import UploadingServerSimulator
from simulator.configuration.servers.downloading import DownloadingServerSimulator


class Server:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument(
                "--server",
                help="The path of server configuration "
                "json file (by default, server.json).",
                default="server.json"
            )

        self.parser.add_argument(
                "--channel",
                help="The path of channel configuration "
                "json file (by default, channel.json).",
                default="channel.json"
            )


    def run(self, args):
        server_path = args.server
        channel_path = args.channel

        tserver = ThesisServerSimulator(server_path, channel_path)
        userver = UploadingServerSimulator(server_path, channel_path)
        dserver = DownloadingServerSimulator(server_path, channel_path)

        tserver.start()
        userver.start()
        dserver.start()
