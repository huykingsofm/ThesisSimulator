import os
import csbuilder

from hks_pylib.done import Done

from csbuilder.scheme.scheme import Scheme
from csbuilder.scheme.result import SchemeResult
from csbuilder.cspacket.cspacket import CSPacket

from _simulator.base.pdp import PDP
from _simulator.manager.token import Token
from _simulator.protocol.definition import ThesisRoles, ThesisProtocols
from _simulator.protocol.definition import CheckClientStates, CheckServerStates


class FailureError(Exception):
    ...


@csbuilder.scheme(
    ThesisProtocols.CHECK,
    ThesisRoles.SERVER,
    CheckClientStates.QUERY
)
class CheckServerScheme(Scheme):
    def __init__(self) -> None:
        super().__init__()

    @csbuilder.response(CheckClientStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload()))

    @csbuilder.response(CheckClientStates.QUERY)
    def resp_query(self, source: str, packet: CSPacket):
        if self.is_running():
            return self.ignore(source, reason="Invalid step")

        failure_reason = None
        failure_packet = self.generate_packet(CheckServerStates.FAILURE)

        try:
            r, d, token = packet.option().decode().split(" ")
            r = int(r)
            d = int(d)

            key = packet.payload()

            try:
                path = Token.degenerate(token)
            except TimeoutError:
                raise FailureError("Expired token")
            except Exception as e:
                raise FailureError("Invalid token")

            if not os.path.isfile(path):
                raise FailureError("Not existed file")

            proof_generator = PDP(path, r=r, d=d)
            digest = proof_generator.generate_a_proof(key)

        except ValueError:
            raise FailureError("Invalid payload")
        except FailureError as e:
            failure_reason = str(e)
            failure_packet.payload(failure_reason.encode())
        except Exception as e:
            failure_reason = "Unknown error ({})".format(str(e))
            failure_packet.payload(b"Unknown error")

        if failure_reason:
            return SchemeResult(
                    source,
                    failure_packet,
                    False,
                    Done(False, reason=failure_reason)
                )

        success_packet = self.generate_packet(CheckServerStates.SUCCESS)
        success_packet.payload(digest)

        return SchemeResult(
                source,
                success_packet,
                False,
                Done(True)
            )
