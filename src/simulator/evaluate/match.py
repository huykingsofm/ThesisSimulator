import time
import argparse

from hks_pylib.files.generator import BMPImageGenerator, BytesGenerator

from _simulator.base.match import SecurePatternMatching


class Match:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument("input1", help="The first file path")
        self.parser.add_argument("input2", help="The second file path")

        self.parser.add_argument(
                "--bmp",
                help="Treat the files as the BMP image files.",
                action="store_true"
            )

    def run(self, args):
        if not args.bmp:
            generator_cls = BytesGenerator
        else:
            generator_cls = BMPImageGenerator

        generator1 = generator_cls(args.input1)
        generator2 = generator_cls(args.input2)

        spm = SecurePatternMatching(generator1, generator2)

        start = time.time()
        spm.match()
        end = time.time()

        return end - start
