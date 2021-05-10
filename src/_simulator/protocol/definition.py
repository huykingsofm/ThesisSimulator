import csbuilder

from csbuilder.standard import Protocols, Roles, States


@csbuilder.protocols
class ThesisProtocols(Protocols):
    AUTHENTICATION = 0
    CHECK = 1
    SEARCH = 2
    MATCH = 3
    REGISTER = 4


@csbuilder.roles(protocol=ThesisProtocols.AUTHENTICATION)
@csbuilder.roles(protocol=ThesisProtocols.CHECK)
@csbuilder.roles(protocol=ThesisProtocols.SEARCH)
@csbuilder.roles(protocol=ThesisProtocols.MATCH)
@csbuilder.roles(protocol=ThesisProtocols.REGISTER)
class ThesisRoles(Roles):
    SERVER = 0
    CLIENT = 1


@csbuilder.states(ThesisProtocols.AUTHENTICATION, ThesisRoles.SERVER)
class AuthenticationServerStates(States):
    IGNORE = 0
    SUCCESS = 1
    FAILURE = 2


@csbuilder.states(ThesisProtocols.AUTHENTICATION, ThesisRoles.CLIENT)
class AuthenticationClientStates(States):
    IGNORE = 0
    REQUEST = 1


@csbuilder.states(ThesisProtocols.SEARCH, ThesisRoles.SERVER)
class SearchServerStates(States):
    IGNORE = 0
    SUCCESS = 1
    FAILURE = 2


@csbuilder.states(ThesisProtocols.SEARCH, ThesisRoles.CLIENT)
class SearchClientStates(States):
    IGNORE = 0
    REQUEST = 1


@csbuilder.states(ThesisProtocols.CHECK, ThesisRoles.SERVER)
class CheckServerStates(States):
    IGNORE = 0
    SUCCESS = 1
    FAILURE = 2


@csbuilder.states(ThesisProtocols.CHECK, ThesisRoles.CLIENT)
class CheckClientStates(States):
    IGNORE = 0
    QUERY = 1


@csbuilder.states(ThesisProtocols.MATCH, ThesisRoles.SERVER)
class MatchServerStates(States):
    IGNORE = 0
    SUCCESS = 1
    FAILURE = 2


@csbuilder.states(ThesisProtocols.MATCH, ThesisRoles.CLIENT)
class MatchClientStates(States):
    IGNORE = 0
    QUERY = 1
