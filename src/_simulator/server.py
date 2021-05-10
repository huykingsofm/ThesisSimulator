from hks_pylib.logger.logger import Display
from hks_pylib.logger import LoggerGenerator
from hks_pylib.logger.standard import StdUsers
from hks_pylib.logger import InvisibleLoggerGenerator
from hks_pylib.cryptography.ciphers.hkscipher import HKSCipher
from hks_pylib.cryptography.ciphers.symmetrics import NoCipher

from csbuilder.server.listener import Listener

from _simulator.protocol.check.server import CheckServerScheme
from _simulator.protocol.match.server import MatchServerScheme
from _simulator.protocol.search.server import SearchServerScheme
from _simulator.protocol.authentication.server import AuthenticationServerScheme


class ThesisListener(Listener):
    def __init__(self,
                address: tuple,
                cipher: HKSCipher = NoCipher(),
                name: str = "Listener",
                logger_generator: LoggerGenerator = InvisibleLoggerGenerator(),
                display = {StdUsers.DEV: Display.ALL}
            ) -> None:
        super().__init__(
                address,
                cipher=cipher,
                name=name,
                logger_generator=logger_generator,
                display=display
            )

        self.session_manager().create_session(MatchServerScheme())
        self.session_manager().create_session(CheckServerScheme())
        self.session_manager().create_session(SearchServerScheme())
        self.session_manager().create_session(AuthenticationServerScheme())
