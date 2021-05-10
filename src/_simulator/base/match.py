from hks_pylib.math import bxor
from hks_pylib.files.generator import BytesGenerator


DEFAULT_BUFFER_SIZE = 10**6  # 1MB


class SecurePatternMatching:
    def __init__(self,
                generator1: BytesGenerator,
                generator2: BytesGenerator,
                buffer_size: int = None
            ) -> None:
        self._generator1 = generator1
        self._generator2 = generator2

        if buffer_size is not None and not isinstance(buffer_size, int):
            raise Exception("Parameter buffer_size expected an int")

        self._buffer_size = buffer_size
        if buffer_size is None:
            self._buffer_size = DEFAULT_BUFFER_SIZE

    def match(self):
        self._generator1.reset()
        self._generator2.reset()

        pair = zip(
                self._generator1.iter(self._buffer_size),
                self._generator2.iter(self._buffer_size)
            )

        nzero = 0
        ntotal = 0

        for block1, block2 in pair:
            block = bxor(block1, block2)
            nzero += block.count(0)
            ntotal += len(block)

        return nzero/ntotal
