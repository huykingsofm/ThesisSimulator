import csbuilder

from hks_pylib.done import Done

from csbuilder.scheme import Scheme
from hks_pylib.hksenum import HKSEnum
from csbuilder.cspacket import CSPacket
from csbuilder.scheme.result import SchemeResult

from _simulator.protocol.definition import ThesisProtocols, ThesisRoles
from _simulator.protocol.definition import CheckClientStates, CheckServerStates


class CheckClientStep(HKSEnum):
    NONE = "none"
    QUERYING = "querying"


@csbuilder.scheme(ThesisProtocols.CHECK, ThesisRoles.CLIENT)
class CheckClientScheme(Scheme):
    def __init__(self, forwarder_name: str) -> None:
        super().__init__()
        self._forwarder_name = forwarder_name

        self._step = CheckClientStep.NONE

        self._digest = None

    def cancel(self, *args, **kwargs) -> None:
        self._step = CheckClientStep.NONE
        self._digest = None

        return super().cancel(*args, **kwargs)

    @csbuilder.active_activation
    def activation(self,
                token: str,
                key: bytes,
                digest: bytes,
                r: int = None,
                d: int = None
            ):
        if not isinstance(key, bytes):
            raise Exception("Parameter key expected a bytes object.")

        if not isinstance(digest, bytes):
            raise Exception("Paramter digest expected a bytes object.")

        if r is not None and not isinstance(r, int):
            raise Exception("Paramter r expected an int object.")

        if d is not None and not isinstance(d, int):
            raise Exception("Paramter d expected an int object.")

        if type(r) != type(d):
            raise Exception("Both of d and r must be passed.")

        if self._step != CheckClientStep.NONE:
            return None, None

        self._digest = digest

        self._step = CheckClientStep.QUERYING

        packet = self.generate_packet(CheckClientStates.QUERY)
        packet.option("{} {} {}".format(r, d, token).encode())
        packet.payload(key)
        return self._forwarder_name, packet

    @csbuilder.response(CheckServerStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload())
            )

    @csbuilder.response(CheckServerStates.FAILURE)
    def resp_failure(self, source: str, packet: CSPacket):
        if self._step == CheckClientStep.QUERYING:
            return SchemeResult(
                    None,
                    None,
                    False,
                    Done(False, reason="Failure", message=packet.payload())
                )
        else:
            return self.ignore(source, reason="Invalid step")

    @csbuilder.response(CheckServerStates.SUCCESS)
    def resp_success(self, source: str, packet: CSPacket):
        if self._step == CheckClientStep.QUERYING:
            digest = packet.payload()
            if digest == self._digest:
                return SchemeResult(None, None, False, Done(True))
            else:
                return SchemeResult(
                        None,
                        None,
                        False,
                        Done(False, reason="Differential digest")
                    )

        else:
            return self.ignore(source, reason="Invalid step")
