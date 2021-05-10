import os

from hks_pylib.done import Done
from hks_pylib.logger.standard import StdLevels, StdUsers
from hks_pylib.logger.logger_generator import StandardLoggerGenerator

from sft.client import SFTClientResponser
from sft.protocol.definition import SFTProtocols, SFTRoles

from _simulator.client import ThesisClient

from simulator.configuration.parser import parse_channel, parse_client


def move_file(result: Done):
    src = result.path
    directory = os.path.split(src)[0]
    des = os.path.join(directory, result.filename)

    if os.path.isfile(des):
        os.remove(des)

    os.rename(src, des)

    return Done(True, path=des)


class ClientSimulator:
    def __init__(self, client_path, channel_path) -> None:
        client_configuration = parse_client(client_path)
        channel_configuration = parse_channel(channel_path)

        self._logger_generator = StandardLoggerGenerator(client_configuration["log"])

        self._host = channel_configuration["host"]

        self._tport = channel_configuration["tport"]
        self._uport = channel_configuration["uport"]
        self._dport = channel_configuration["dport"]

        self._cipher = channel_configuration["cipher"]

        print = self._logger_generator.generate("Console", {StdUsers.USER: [StdLevels.INFO]})

        self._print = lambda *args, **kwargs:\
            print(
                StdUsers.USER,
                StdLevels.INFO,
                *args,
                **kwargs
            )

    def sftsend(self, token, path):
        client = SFTClientResponser(
                cipher=self._cipher,
                address=(self._host, self._uport),
                logger_generator=self._logger_generator
            )
        
        client.connect()

        try:
            client.start(True)

            client.activate(SFTProtocols.SFT, SFTRoles.SENDER, path=path, token=token)

            result = client.wait_result(SFTProtocols.SFT, SFTRoles.SENDER, timeout=30)

            if result == None:
                result = Done(False, reason="Timeout")

        except Exception as e:
            result = Done(False, reason=str(e))
        finally:
            client.close()

        return result

    def sftrecv(self, token):
        client = SFTClientResponser(
                cipher=self._cipher,
                address=(self._host, self._dport),
                logger_generator=self._logger_generator
            )

        client.connect()

        try:
            client.start(True)

            client.activate(SFTProtocols.SFT, SFTRoles.RECEIVER, token=token)

            result = client.wait_result(SFTProtocols.SFT, SFTRoles.RECEIVER, timeout=30)

            if result == None:
                result = Done(False, reason="Timeout")
        except Exception as e:
            result = Done(False, reason=str(e))
        finally:
            client.close()

        if result:
            move_file(result)

        return result

    def connect(self):
        client = ThesisClient(
                address=(self._host, self._tport),
                cipher=self._cipher,
                logger_generator=self._logger_generator
            )

        client.connect()
        client.start(True)

        return client
