import json

from hks_pylib.cryptography.ciphers.keygenerator import KeyGenerator
from hks_pylib.cryptography.ciphers.symmetrics import AES_CBC, AES_CTR, NoCipher


from _simulator.manager.users import Users
from _simulator.manager.storage import Storage
from _simulator.manager.token import DEFAULT_TOKEN_SIZE, Token


def parse_server(path):

    # GET CONFIGURATED INFORMATION
    with open(path, "rt") as f:
        configuration: dict = json.load(f)

    storage_dir = configuration.get("storage", "Storage")
    users_path = configuration.get("users", "users.json")

    token_configuration = configuration.get("token", {})

    token_password = token_configuration.get("password", "default")
    token_secret = token_configuration.get("secret", "default")
    token_size = token_configuration.get("size", DEFAULT_TOKEN_SIZE)

    log_path = configuration.get("log", "logs/server.log")

    # CONFIG

    Storage.config(directory=storage_dir)
    Users.config(path=users_path)

    token_key = KeyGenerator(32).pwd2key(token_password)
    token_secret = KeyGenerator(token_size)\
        .pwd2key(token_secret)\
        .replace(b"\x00", b"\xff")

    Token.config(
            key=token_key,
            secret=token_secret,
            size=token_size
        )

    return {
        "log": log_path,
        "storage": storage_dir
        }

def parse_channel(path):
    with open(path, "rt") as f:
        configuration: dict = json.load(f)

    host = configuration.get("host")

    tport = configuration.get("tport", 1999)
    uport = configuration.get("uport", 1808)
    dport = configuration.get("dport", 2001)

    cipher = configuration.get("cipher", None)
    password = configuration.get("password", "default")
    key = KeyGenerator(32).pwd2key(password)

    ALL_CIPHERS = (None, "AES_CTR", "AES_CBC")
    if cipher not in ALL_CIPHERS:
        raise Exception("The parameter cipher only can be one of {}.".format(ALL_CIPHERS))

    if cipher is None:
        cipher = NoCipher()

    if cipher == "AES_CTR":
        cipher = AES_CTR(key)

    if cipher == "AES_CBC":
        cipher = AES_CBC(key)

    return {
            "host": host,
            "tport": tport,
            "uport": uport, 
            "dport": dport,
            "cipher": cipher
        }

def parse_client(path):
    with open(path, "rt") as f:
        configuration: dict = json.load(f)

    log_path = configuration.get("log", "logs/client.log")

    return {"log": log_path}
