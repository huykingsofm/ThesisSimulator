import csbuilder

from hks_pylib.done import Done

from csbuilder.scheme.scheme import Scheme
from csbuilder.scheme.result import SchemeResult
from csbuilder.cspacket.cspacket import CSPacket

from _simulator.manager.users import Users
from _simulator.manager.token import Token

from _simulator.protocol.definition import AuthenticationServerStates
from _simulator.protocol.definition import AuthenticationClientStates
from _simulator.protocol.definition import ThesisRoles, ThesisProtocols


class FailureError(Exception):
    ...


@csbuilder.scheme(
    ThesisProtocols.AUTHENTICATION,
    ThesisRoles.SERVER,
    AuthenticationClientStates.REQUEST
)
class AuthenticationServerScheme(Scheme):
    def __init__(self) -> None:
        super().__init__()

    @csbuilder.response(AuthenticationClientStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload())
            )

    @csbuilder.response(AuthenticationClientStates.REQUEST)
    def resp_request(self, source: str, packet: CSPacket):
        if self.is_running():
            return self.ignore(source, reason="Busy")

        payload = packet.payload()

        failure_reason = None
        failure_packet = self.generate_packet(AuthenticationServerStates.FAILURE)

        try:
            username, password = payload.decode().split(" ")

            if Users.authenticate(username, password) is False:
                raise FailureError("Authentication failed")

        except ValueError:
            raise FailureError("Invalid format payload")
        except FailureError as e:
            failure_reason = str(e)
            failure_packet.payload(failure_reason.encode())
        except Exception as e:
            failure_reason = "Unknown error ({})".format(e)
            failure_packet.payload(b"Unknown error")

        if failure_reason:
            return SchemeResult(
                    source,
                    failure_packet,
                    False,
                    Done(False, reason=failure_reason)
                )

        token = Token.generate(username, timeout=900)

        success_packet = self.generate_packet(AuthenticationServerStates.SUCCESS)
        success_packet.payload(token.encode())

        return SchemeResult(
                source,
                success_packet,
                False,
                Done(True, token=token)
            )
