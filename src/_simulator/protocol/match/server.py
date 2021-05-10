import os
import imghdr
import csbuilder

from hks_pylib.done import Done
from hks_pylib.files.generator import BytesGenerator, BMPImageGenerator

from csbuilder.scheme.scheme import Scheme
from csbuilder.scheme.result import SchemeResult
from csbuilder.cspacket.cspacket import CSPacket

from _simulator.manager.token import Token
from _simulator.base.match import SecurePatternMatching
from _simulator.protocol.definition import ThesisRoles, ThesisProtocols
from _simulator.protocol.definition import MatchClientStates, MatchServerStates



class FailureError(Exception):
    ...


@csbuilder.scheme(
    ThesisProtocols.MATCH,
    ThesisRoles.SERVER,
    MatchClientStates.QUERY
)
class MatchServerScheme(Scheme):
    def __init__(self) -> None:
        super().__init__()

    @csbuilder.response(MatchClientStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload()))

    @csbuilder.response(MatchClientStates.QUERY)
    def resp_query(self, source: str, packet: CSPacket):
        if self.is_running():
            return self.ignore(source, reason="Invalid step")

        failure_reason = None
        failure_packet = self.generate_packet(MatchServerStates.FAILURE)

        try:
            ftoken1, ftoken2 = packet.payload().decode().split(" ")

            try:
                path1 = Token.degenerate(ftoken1)
                path2 = Token.degenerate(ftoken2)
            except TimeoutError:
                raise FailureError("Expired token")
            except Exception as e:
                raise FailureError("Invalid token")

            if not os.path.isfile(path1) or not os.path.isfile(path2):
                raise FailureError("Not existed file")

            if imghdr.what(path1) == "bmp":
                generator1 = BMPImageGenerator(path1)
            else:
                generator1 = BytesGenerator(path1)

            if imghdr.what(path2) == "bmp":
                generator2 = BMPImageGenerator(path2)
            else:
                generator2 = BytesGenerator(path2)

            spm = SecurePatternMatching(generator1, generator2)
            result = spm.match()

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

        success_packet = self.generate_packet(MatchServerStates.SUCCESS)
        success_packet.payload(str(result).encode())

        return SchemeResult(
                source,
                success_packet,
                False,
                Done(True)
            )
