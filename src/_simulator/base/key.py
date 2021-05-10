from hks_pylib.cryptography.hashes import SHA1, MD5
from hks_pylib.cryptography.ciphers.symmetrics import AES_CTR


class MasterKey(object):
    def __init__(self, key: bytes) -> None:
        self._key = key

        self._encryptor = AES_CTR(self._key)

        # Length of MD5(data) == 128 bit == block size of AES
        self._encryptor.set_param(0, MD5().finalize(key))

        self._material = self._encryptor.encrypt(key)

    def derive(self, index: int):
        self._encryptor.reset(auto_renew_params=False)

        iv = index.to_bytes(16, "big")
        self._encryptor.set_param(0, iv)

        return self._encryptor.encrypt(self._material)

    def __getitem__(self, index: int):
        return self.derive(index)

