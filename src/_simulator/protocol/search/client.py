import csbuilder

from hks_pylib.done import Done

from csbuilder.scheme import Scheme
from csbuilder.cspacket import CSPacket
from csbuilder.scheme.result import SchemeResult

from _simulator.protocol.definition import ThesisProtocols, ThesisRoles
from _simulator.protocol.definition import SearchClientStates, SearchServerStates


@csbuilder.scheme(ThesisProtocols.SEARCH, ThesisRoles.CLIENT)
class SearchClientScheme(Scheme):
    def __init__(self, forwarder_name: str) -> None:
        super().__init__()
        self._forwarder_name = forwarder_name

    @csbuilder.active_activation
    def activation(self, token: str, filename: str):
        if self.is_running():
            return None, None

        packet = self.generate_packet(SearchClientStates.REQUEST)
        packet.payload("{} {}".format(token, filename).encode())
        return self._forwarder_name, packet

    @csbuilder.response(SearchServerStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload())
            )

    @csbuilder.response(SearchServerStates.SUCCESS)
    def resp_success(self, source: str, packet: CSPacket):
        if self.is_running():
            token = packet.payload().decode()
            return SchemeResult(None, None, False, Done(True, token=token))
        else:
            return self.ignore(source)

    @csbuilder.response(SearchServerStates.FAILURE)
    def resp_failure(self, source: str, packet: CSPacket):
        if self.is_running():
            return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Failure", message=packet.payload())
            )
        else:
            return self.ignore(source)
