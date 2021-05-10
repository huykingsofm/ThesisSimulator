import os
import json
import base64

from typing import Iterator

from hks_pylib.cryptography.hashes import HKSHash, SHA256

from _simulator.base.rand import Rand
from _simulator.base.key import MasterKey


DEFAULT_R = 460
DEFAULT_D = 10000
DEFAULT_HASH = SHA256


class PDP(object):
    def __init__(self,
                filename: str,
                hash_algorithm: HKSHash = None,
                r: int = None,
                d: int = None
            ) -> None:
        """
        Parameters:\n
        + `r` (`int`): The number of blocks to be proved.\n
        + `d` (`int`): The total number of blocks.
        """

        if not os.path.isfile(filename):
            raise Exception("File not found.")

        if hash_algorithm is not None and not isinstance(hash_algorithm, HKSHash):
            raise Exception("Parameter hash_algorithm expected a HKSHash object.")

        if r is not None and not isinstance(r, int):
            raise Exception("Parameter r expected an int object.")

        if d is not None and not isinstance(d, int):
            raise Exception("Parameter d expected an int object.")

        if r and d and r > d:
            raise Exception("The number of blocks to be proved "
            "r must be less than or equal to the total number "
            "of block d.")

        self._filename = filename

        self._hash_algorithm = hash_algorithm
        if hash_algorithm is None:
            self._hash_algorithm = DEFAULT_HASH()

        self._r = r
        if r is None:
            self._r = DEFAULT_R

        self._d = d
        if d is None:
            self._d = DEFAULT_D

        self._d = min(self._d, os.path.getsize(filename))
        self._r = min(self._d, self._r)

        self._blocksize = os.path.getsize(filename) // self._d

    def generate_a_proof(self, key):
        nonce = Rand.randbytes(key, 32)
        indices = Rand.randperm(key, 0, self._d-1)[:self._r]

        self._hash_algorithm.reset()

        self._hash_algorithm.update(nonce)

        with open(self._filename, "rb") as f:
            for index in indices:
                offset = index * self._blocksize
                f.seek(offset)
                block = f.read(self._blocksize)

                self._hash_algorithm.update(block)

        return self._hash_algorithm.finalize()


class ClientPDP(PDP):
    def save(   self,
                output: str,
                master_key: MasterKey,
                key_indices: Iterator[int]
            ):
        metadata = {
                "r": self._r,
                "d": self._d,
                "digests": {}
                }

        for key_index in key_indices:
            session_key = master_key.derive(key_index)
            digest = self.generate_a_proof(session_key)
            metadata["digests"][key_index] = base64.b64encode(digest).decode()

        metadata_file = open(output, "wt")        
        json.dump(metadata, metadata_file)
        metadata_file.close()

    @staticmethod
    def pick(input: str, key_index: int):
        metadata_file = open(input, "rt")
        metadata = json.load(metadata_file)
        metadata_file.close()

        key_index = str(key_index)
        return {
                "r": metadata["r"],
                "d": metadata["d"],
                "digest": base64.b64decode(metadata["digests"][key_index])
            }

    @staticmethod
    def remove(input: str, key_index: int):
        metadata_file = open(input, "rt")
        metadata = json.load(metadata_file)
        metadata_file.close()

        key_index = str(key_index)
        metadata["digests"].pop(key_index, None)

        metadata_file = open(input, "wt")
        json.dump(metadata, metadata_file)
        metadata_file.close()
