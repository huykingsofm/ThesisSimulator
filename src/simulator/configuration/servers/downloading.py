import socket
import threading
from csbuilder.server.responser import ServerResponser

from hks_pylib.logger.logger import Display
from hks_pylib.logger.standard import StdLevels, StdUsers
from hks_pylib.logger.logger_generator import StandardLoggerGenerator

from sft.listener import SFTListener
from sft.protocol.definition import SFTProtocols, SFTRoles

from _simulator.manager.token import Token


from simulator.configuration.parser import parse_server, parse_channel
from simulator.utils import error


def error_detoken(x):
    raise Exception("Invalid Token ({})".format(x))


class DownloadingServerSimulator:
    def __init__(self, server_path, channel_path) -> None:
        server_configuration = parse_server(server_path)
        channel_configuration = parse_channel(channel_path)

        logger_generator = StandardLoggerGenerator(server_configuration["log"])

        host = channel_configuration["host"]
        dport = channel_configuration["dport"]
        cipher = channel_configuration["cipher"]

        print = logger_generator.generate("Console", {StdUsers.USER: [StdLevels.INFO]})

        self._print = lambda *args, **kwargs:\
            print(
                StdUsers.USER,
                StdLevels.INFO,
                *args,
                **kwargs
            )

        self.__listener = SFTListener(
                cipher=cipher,
                address=(host, dport),
                name="SFT Downloading Listener",
                logger_generator=logger_generator,
                display={StdUsers.USER: Display.ALL, StdUsers.DEV: Display.ALL}
            )

        self.__listener.get_scheme(
                SFTProtocols.SFT,
                SFTRoles.RECEIVER
            ).config(detoken=error_detoken)

    def _serve(self, responser: ServerResponser):
        try:
            responser.get_scheme(
                    SFTProtocols.SFT,
                    SFTRoles.SENDER
                ).config(detoken=Token.degenerate)

            responser.start(True)

            result = responser.wait_result(SFTProtocols.SFT, SFTRoles.SENDER, timeout=30)

            if result == None:
                raise Exception("Detected an abnormal connection.")

            if result:
                    self._print(result)
            else:
                self._print(error(result))

        except Exception as e:
            self._print(e)

    def _start(self):
        self.__listener.listen()

        while True:
            try:
                responser = self.__listener.accept(False)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break

            threading.Thread(target=self._serve, args=(responser, )).start()

        self.__listener.close()

    def start(self):
        threading.Thread(
                target=self._start,
                name="Downloading Server"
            ).start()
