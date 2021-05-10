from hks_pylib.done import Done


def error(result: Done):
    if result.has("message"):
        return Done(False, error="{} ({}).".format(result.reason, result.message.decode()))

    return Done(False, error=result.reason)
