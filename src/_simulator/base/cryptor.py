from hks_pylib.files.generator import BytesGenerator
from hks_pylib.cryptography.ciphers.symmetrics import AES_CTR
from hks_pylib.cryptography.ciphers.keygenerator import KeyGenerator


class Cryptor(object):
    def __init__(self, generator: BytesGenerator) -> None:
        if not isinstance(generator, BytesGenerator):
            raise Exception("Parameter generator expected a BytesGenerator.")

        self._generator = generator

    def encrypt(self,
                output: str, 
                password: str,
                buffer_size: int = 65535
            ):
        if not isinstance(output, str):
            raise Exception("Parameter output expected an str object.")

        if not isinstance(password, str):
            raise Exception("Parameter password expected an str object.")

        if not isinstance(buffer_size, int) or buffer_size <= 0:
            raise Exception("Paramter buffer_size expected a positive integer.")

        self._generator.reset()

        key = KeyGenerator(32).pwd2key(password)
        iv = KeyGenerator(16).pwd2key(password)

        cipher = AES_CTR(key)
        cipher.set_param(0, iv)

        with open(output, "wb") as f:
            f.write(self._generator.head())

            for block in self._generator.iter(buffer_size):
                encrypted_block = cipher.encrypt(block, finalize=False)
                f.write(encrypted_block)

            final_block = cipher.finalize()
            f.write(final_block)

            f.write(self._generator.tail())

    def decrypt(self,
                output: str,
                password: str,
                buffer_size: int = 65535
            ):
        if not isinstance(output, str):
            raise Exception("Parameter output expected an str object.")

        if not isinstance(password, str):
            raise Exception("Parameter password expected an str object.")

        if not isinstance(buffer_size, int) or buffer_size <= 0:
            raise Exception("Paramter buffer_size expected a positive integer.")

        self._generator.reset()

        key = KeyGenerator(32).pwd2key(password)
        iv = KeyGenerator(16).pwd2key(password)

        cipher = AES_CTR(key)
        cipher.set_param(0, iv)

        with open(output, "wb") as f:
            f.write(self._generator.head())

            for encrypted_block in self._generator.iter(buffer_size):
                block = cipher.decrypt(encrypted_block, finalize=False)
                f.write(block)

            final_block = cipher.finalize()
            f.write(final_block)

            f.write(self._generator.tail())
