import threading

from hks_pylib.logger.logger import Display
from hks_pylib.logger.standard import StdLevels, StdUsers
from hks_pylib.logger.logger_generator import StandardLoggerGenerator

from _simulator.server import ThesisListener

from simulator.configuration.parser import parse_server, parse_channel


class ThesisServerSimulator(object):
    def __init__(self, server_path, channel_path):
        server_configuration = parse_server(server_path)
        channel_configuration = parse_channel(channel_path)

        logger_generator = StandardLoggerGenerator(server_configuration["log"])

        host = channel_configuration["host"]
        tport = channel_configuration["tport"]
        cipher = channel_configuration["cipher"]


        print = logger_generator.generate("Console", {StdUsers.USER: [StdLevels.INFO]})

        self._print = lambda *args, **kwargs:\
            print(
                StdUsers.USER,
                StdLevels.INFO,
                *args,
                **kwargs
            )

        self.__listener = ThesisListener(
                address=(host, tport),
                cipher=cipher,
                name="Thesis Listener",
                logger_generator=logger_generator,
                display={StdUsers.USER: Display.ALL, StdUsers.DEV: Display.ALL}
            )

    def start(self):
        threading.Thread(
                target=self.__listener.quickstart,
                name="Thesis Server"
            ).start()
