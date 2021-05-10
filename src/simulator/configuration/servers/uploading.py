import socket
import threading

from csbuilder.server.responser import ServerResponser

from hks_pylib.logger.logger import Display
from hks_pylib.logger.standard import StdLevels, StdUsers
from hks_pylib.logger.logger_generator import StandardLoggerGenerator

from sft.listener import SFTListener
from sft.protocol.definition import SFTProtocols, SFTRoles

from _simulator.manager.token import Token
from _simulator.manager.storage import Storage

from simulator.utils import error
from simulator.configuration.parser import parse_server, parse_channel


def error_detoken(x):
    raise Exception("Invalid token ({})".format(x))


class UploadingServerSimulator:
    def __init__(self, server_path, channel_path) -> None:
        server_configuration = parse_server(server_path)
        channel_configuration = parse_channel(channel_path)

        logger_generator = StandardLoggerGenerator(server_configuration["log"])

        host = channel_configuration["host"]
        uport = channel_configuration["uport"]
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
                address=(host, uport),
                name="SFT Uploading Listener",
                logger_generator=logger_generator,
                display={StdUsers.USER: Display.ALL, StdUsers.DEV: Display.ALL}
            )

        self.__listener.get_scheme(
                SFTProtocols.SFT,
                SFTRoles.RECEIVER
            ).config(directory=server_configuration["storage"])

        self.__listener.get_scheme(
                SFTProtocols.SFT,
                SFTRoles.SENDER
            ).config(detoken=error_detoken)


    def _serve(self, responser: ServerResponser):
        try:
            responser.get_scheme(
                    SFTProtocols.SFT,
                    SFTRoles.RECEIVER
                ).config(detoken=Token.degenerate)

            responser.start(True)

            result = responser.wait_result(SFTProtocols.SFT, SFTRoles.RECEIVER, timeout=30)

            if result == None:
                raise Exception("Detected an abnormal connection.")

            if result:
                username = result.detoken_value
                src = result.path
                Storage.store(username, src)
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
                name="Uploading Server"
            ).start()
