import csbuilder

from hks_pylib.done import Done

from csbuilder.scheme.scheme import Scheme
from csbuilder.scheme.result import SchemeResult
from csbuilder.cspacket.cspacket import CSPacket

from _simulator.manager.token import Token
from _simulator.manager.storage import Storage
from _simulator.protocol.definition import ThesisRoles, ThesisProtocols
from _simulator.protocol.definition import SearchClientStates, SearchServerStates


class FailureError(Exception):
    ...


@csbuilder.scheme(
    ThesisProtocols.SEARCH,
    ThesisRoles.SERVER,
    SearchClientStates.REQUEST
)
class SearchServerScheme(Scheme):
    def __init__(self) -> None:
        super().__init__()

    @csbuilder.response(SearchClientStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload())
            )

    @csbuilder.response(SearchClientStates.REQUEST)
    def resp_request(self, source: str, packet: CSPacket):
        if self.is_running():
            return self.ignore(source)

        payload = packet.payload()

        failure_reason = None
        failure_packet = self.generate_packet(SearchServerStates.FAILURE)

        try:
            token, filename = payload.decode().split(" ")

            try:
                username = Token.degenerate(token)
            except TimeoutError:
                raise FailureError("Expired token")
            except Exception:
                raise FailureError("Invalid token")

            path = Storage.get_path(username, filename)
            if path is None:
                raise FailureError("File doesn't found")

        except ValueError:
            raise FailureError("Invalid payload")

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

        token = Token.generate(path, timeout=900)

        success_packet = self.generate_packet(SearchServerStates.SUCCESS)
        success_packet.payload(token.encode())

        return SchemeResult(
                source,
                success_packet,
                False,
                Done(True, token=token)
            )
