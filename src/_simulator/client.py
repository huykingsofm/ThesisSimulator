from hks_pylib.logger.standard import StdUsers
from hks_pylib.cryptography.ciphers.hkscipher import HKSCipher
from hks_pylib.cryptography.ciphers.symmetrics import NoCipher
from hks_pylib.logger import LoggerGenerator, InvisibleLoggerGenerator, Display

from csbuilder.client import ClientResponser

from _simulator.protocol.check.client import CheckClientScheme
from _simulator.protocol.match.client import MatchClientScheme
from _simulator.protocol.search.client import SearchClientScheme
from _simulator.protocol.authentication.client import AuthenticationClientScheme


class ThesisClient(ClientResponser):
    def __init__(self,
            address: tuple,
            cipher: HKSCipher = NoCipher(),
            logger_generator: LoggerGenerator = InvisibleLoggerGenerator(),
            display: dict = {StdUsers.DEV: Display.ALL}
        ) -> None:
        super().__init__(
                address,
                cipher=cipher,
                name="Client",
                logger_generator=logger_generator,
                display=display
            )

        self.session_manager().create_session(CheckClientScheme(self._forwarder.name))
        self.session_manager().create_session(MatchClientScheme(self._forwarder.name))
        self.session_manager().create_session(SearchClientScheme(self._forwarder.name))
        self.session_manager().create_session(AuthenticationClientScheme(self._forwarder.name))
