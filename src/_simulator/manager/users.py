import os
import json
import threading

from hks_pylib import as_object
from hks_pylib.logger import console_output


@as_object
class Users(object):
    def __init__(self) -> None:
        self.__path: str = None
        self.__lock = threading.Lock()

    def config(self, path) -> None:
        if not os.path.isfile(path):
            console_output.write("WARNING: Create {} because the file didn't exist.")
            with open(path, "wt") as f:
                json.dump({}, f)

        self.__path = path

    def authenticate(self, username: str, password: str):
        self.__lock.acquire()
        
        try:
            with open(self.__path, "rt") as f:
                users = json.load(f)

            if username not in users.keys():
                return False

            if users[username] != password:
                return False

            return True

        finally:
            self.__lock.release()

    def update(self, username: str, password: str):
        self.__lock.acquire()
        
        try:
            with open(self.__path, "rt") as f:
                users = json.load(f)

            users[username] = password

            with open(self.__path, "wt") as f:
                json.dump(users, f)

        finally:
            self.__lock.release()
