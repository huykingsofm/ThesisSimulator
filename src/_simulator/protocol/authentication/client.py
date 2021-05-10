import csbuilder

from hks_pylib.done import Done

from csbuilder.scheme import Scheme
from csbuilder.cspacket import CSPacket
from csbuilder.scheme.result import SchemeResult

from _simulator.protocol.definition import AuthenticationServerStates
from _simulator.protocol.definition import AuthenticationClientStates
from _simulator.protocol.definition import ThesisProtocols, ThesisRoles

@csbuilder.scheme(ThesisProtocols.AUTHENTICATION, ThesisRoles.CLIENT)
class AuthenticationClientScheme(Scheme):
    def __init__(self, forwarder_name: str) -> None:
        super().__init__()
        self._forwarder_name = forwarder_name

    @csbuilder.active_activation
    def activation(self, username: str, password: str):
        if self.is_running():
            return None, None

        packet = self.generate_packet(AuthenticationClientStates.REQUEST)
        packet.payload("{} {}".format(username, password).encode())
        return self._forwarder_name, packet

    @csbuilder.response(AuthenticationServerStates.IGNORE)
    def resp_ignore(self, source: str, packet: CSPacket):
        return SchemeResult(
                None,
                None,
                False,
                Done(False, reason="Ignore", message=packet.payload())
            )

    @csbuilder.response(AuthenticationServerStates.SUCCESS)
    def resp_success(self, source: str, packet: CSPacket):
        if self.is_running():
            token = packet.payload().decode()
            return SchemeResult(None, None, False, Done(True, token=token))
        else:
            return self.ignore(source, reason="Invalid step")

    @csbuilder.response(AuthenticationServerStates.FAILURE)
    def resp_faulure(self, source: str, packet: CSPacket):
        if self.is_running():
            return SchemeResult(
                    None,
                    None,
                    False,
                    Done(False, reason="Failure", message=packet.payload())
                )
        else:
            return self.ignore(source, reason="Invalid step")
