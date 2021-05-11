import os
import time
import argparse
from hks_pylib.files.generator import BMPImageGenerator, BytesGenerator

from _simulator.base.cryptor import Cryptor


class Encrypt:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument("input", help="The file path of sample.")

        self.parser.add_argument(
                "--decrypt",
                "-d",
                help="Evaluate the decryption instead of the encryption",
                action="store_true"
            )

        self.parser.add_argument(
                "--bmp",
                help="Treat the file as a BMP image.",
                action="store_true"
            )


    def run(self, args):
        if os.path.isfile(args.input) is False:
            raise FileNotFoundError("File {} isn't found.".format(args.input))

        if args.bmp:
            generator = BMPImageGenerator(args.input)
        else:
            generator = BytesGenerator(args.input)

        cryptor = Cryptor(generator)

        start = time.time()
        if args.decrypt:
            cryptor.decrypt("evaluation.temp", "default password")
        else:
            cryptor.encrypt("evaluation.temp", "default password")
        end = time.time()

        os.remove("evaluation.temp")

        return end - start
