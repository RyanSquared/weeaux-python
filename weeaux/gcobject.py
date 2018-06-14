# pylint: disable=missing-docstring


class GCObject(object):
    def __init__(self):
        self._closed = False

    def assert_open(self):
        if self._closed:
            raise Exception("usage of object after close")

    def close(self):
        raise NotImplementedError()
