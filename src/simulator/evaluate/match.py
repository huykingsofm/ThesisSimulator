import time
import argparse

from numpy import std, mean

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

        self.parser.add_argument(
                "--round",
                "-r",
                help="The number of rounds which you want to perform "
                "the evaluation. By default, round is 10.",
                type=int,
                default=10
            )
    def run(self, args):
        if not args.bmp:
            generator_cls = BytesGenerator
        else:
            generator_cls = BMPImageGenerator

        generator1 = generator_cls(args.input1)
        generator2 = generator_cls(args.input2)

        spm = SecurePatternMatching(generator1, generator2)
        
        elapsed_time = []

        prev_result = None
        for _ in range(args.round):

            start = time.time()
            result = spm.match()
            end = time.time()

            if prev_result is not None and result != prev_result:
                raise Exception("Secure pattern matching is incorrect")

            prev_result = result

            elapsed_time.append(end - start)

        print("The result of SPM is {:.2f}%".format(result * 100))
        print("The average cost is {:.3f}s.".format(mean(elapsed_time)))
        print("The standard deviation is {:.5f}s.".format(std(elapsed_time)))
