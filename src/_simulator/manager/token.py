import time
import base64

from hks_pylib import as_object
from hks_pylib.cryptography.ciphers.keygenerator import KeyGenerator
from hks_pylib.cryptography.ciphers.symmetrics import AES_CBC


DEFAULT_TOKEN_SIZE = 128
DEFAULT_SECRET = KeyGenerator(DEFAULT_TOKEN_SIZE)\
    .pwd2key("default")\
    .replace(b"\x00", b"\xff")

PREFIX = "thesis-"


@as_object
class Token(object):
    def __init__(self) -> None:
        self.__encryptor = None
        self.__size = DEFAULT_TOKEN_SIZE
        self.__secret = DEFAULT_SECRET

    def config(self, **kwargs):
        key = kwargs.pop("key", None)
        secret = kwargs.pop("secret", None)
        size = kwargs.pop("size", None)

        if kwargs:
            raise Exception("Unexpected parameters {}".format(set(kwargs.keys())))

        if size is not None:
            if not isinstance(size, int):
                raise Exception("Parameter size expected an int object")

            if size < 32:
                raise Exception("Not enough size {}, "
                "at least 32 bytes.".format(size))

            self.__size = size
            self.__secret = bytes(range(1, size + 1))

        if secret is not None:
            if len(secret) < self.__size:
                raise Exception("The length of super secret "
                "must at least equal to token size ({})".format(self.__size))

            self.__secret = secret

        if key is not None:
            self.__encryptor = AES_CBC(key)
            self.__encryptor.set_param(0, b"0" * 16)

    def generate(self, *args: str, timeout=300):
        encoded_args = []
        for arg in args:
            if not isinstance(arg, str):
                raise Exception("Required str object")

            encoded_args.append(arg.encode())

        token = b"\x00".join(encoded_args)

        start = str(int(time.time())).encode()
        timeout = str(timeout).encode()

        token = b"\x00".join([token, start, timeout])

        secret_padding = self.__secret[:self.__size - len(token)]

        token = b"\x00".join([token, secret_padding])

        self.__encryptor.reset(False)
        token = self.__encryptor.encrypt(token)

        return PREFIX + base64.b32encode(token).decode()

    def degenerate(self, token: str):
        if not isinstance(token, str):
            raise Exception("Parameter token expected a bytes object")

        if token[:len(PREFIX)] != PREFIX:
            raise Exception("Invalid token")

        token = base64.b32decode(token[len(PREFIX):])

        self.__encryptor.reset(False)
        token = self.__encryptor.decrypt(token)

        args = token.split(b"\x00")

        secret_padding = args[-1]
        timeout = int(args[-2].decode())
        start = int(args[-3].decode())

        if secret_padding != self.__secret[:len(secret_padding)]:
            raise Exception("Invalid token.")

        if time.time() - start > timeout:
            raise TimeoutError("Expired token.")

        decoded_args = []
        for arg in args[:-3]:
            decoded_args.append(arg.decode())

        if len(decoded_args) == 1:
            return decoded_args[0]

        if len(decoded_args) == 0:
            return None

        return decoded_args
