import os

from hks_pylib import as_object
from hks_pylib.logger import console_output


@as_object
class Storage(object):
    def __init__(self) -> None:
        self.__directory = "/"

    def config(self, directory: str):
        if not os.path.isdir(directory):
            console_output.write("WARNING: Create {} because this directory did not exist.")
            os.mkdir(directory)

        self.__directory = directory

    def store(self, username: str, src: str):
        userpath = os.path.join(self.__directory, username)
        if not os.path.isdir(userpath):
            os.mkdir(userpath)

        filename = os.path.split(src)[1]
        filename = filename.split(".")

        extension = filename[-1]
        if extension.isdecimal() and len(extension) > 10:
            filename = ".".join(filename[:-1])
        else:
            filename = ".".join(filename)

        dst = os.path.join(userpath, filename)
        if os.path.isfile(dst):
            os.remove(dst)

        os.rename(src, dst)

    def get_path(self, username, filename):
        userpath = os.path.join(self.__directory, username)
        if not os.path.isdir(userpath):
            os.mkdir(userpath)
            return None

        path = os.path.join(userpath, filename)
        if os.path.isfile(path):
            return path

        return None
