import os
import time
import argparse

from hks_pylib.files.generator import BytesGenerator, BMPImageGenerator

from _simulator.base.cryptor import Cryptor


class Encrypt:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument(
                "input",
                help="The file path is passed to the encryption or decryption"
            )

        self.parser.add_argument(
                "output",
                help="The file path is used to contain the encrypted or decrypted input."
            )

        self.parser.add_argument(
                "--password",
                "-p",
                help="The password is used to encrypt or decrypt the file."
            )

        self.parser.add_argument(
                "--decrypt",
                "-d",
                help="Decrypting the file instead of encrypting",
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
        
        if args.decrypt:
            cryptor.decrypt(args.output, args.password)
            print("Decrypt file {} to {} successfully.".format(args.input, args.output))
        else:
            cryptor.encrypt(args.output, args.password)
            print("Encrypt file {} to {} successfully.".format(args.input, args.output))

