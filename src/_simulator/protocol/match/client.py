import csbuilder

from hks_pylib.done import Done

from csbuilder.scheme import Scheme
from hks_pylib.hksenum import HKSEnum
from csbuilder.cspacket import CSPacket
from csbuilder.scheme.result import SchemeResult

from _simulator.protocol.definition import ThesisProtocols, ThesisRoles
from _simulator.protocol.definition import MatchClientStates, MatchServerStates


class MatchClientStep(HKSEnum):
    NONE = "none"
    QUERYING = "querying"


@csbuilder.scheme(ThesisProtocols.MATCH, ThesisRoles.CLIENT)
class MatchClientScheme(Scheme):
    def __init__(self, forwarder_name: str) -> None:
        super().__init__()
        self._forwarder_name = forwarder_name

        self._step = MatchClientStep.NONE

        self._digest = None

    def cancel(self, *args, **kwargs) -> None:
        self._step = MatchClientStep.NONE
        self._digest = None

        return super().cancel(*args, **kwargs)

    @csbuilder.active_activation
    def activation(self,
                token1: str,
                token2: str
            ):
        if self._step != MatchClientStep.NONE:
            return None, None

        self._step = MatchClientStep.QUERYING

        packet = self.generate_packet(MatchClientStates.QUERY)
        packet.payload("{} {}".format(token1, token2).encode())
        return self._forwarder_name, packet

    @csbuilder.response(MatchServerStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload())
            )

    @csbuilder.response(MatchServerStates.FAILURE)
    def resp_failure(self, source: str, packet: CSPacket):
        if self._step == MatchClientStep.QUERYING:
            return SchemeResult(
                    None,
                    None,
                    False,
                    Done(False, reason="Failure", message=packet.payload())
                )
        else:
            return self.ignore(source, reason="Invalid step")

    @csbuilder.response(MatchServerStates.SUCCESS)
    def resp_success(self, source: str, packet: CSPacket):
        if self._step == MatchClientStep.QUERYING:
            similarity = float(packet.payload().decode())
            return SchemeResult(None, None, False, Done(True, similarity=similarity))

        else:
            return self.ignore(source, reason="Invalid step")
