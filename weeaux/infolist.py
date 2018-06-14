# pylint: disable=import-error,missing-docstring
from weechat import (infolist_get, infolist_free, infolist_next,
                     infolist_fields, infolist_integer, infolist_string,
                     infolist_pointer, infolist_time)
from .gcobject import GCObject


class InfoListItem(GCObject):
    """
    This is an internal class and should not be constructed by users.

    Usage of items after the current iteration step should only be accessed
    by the `InfoListItem.clone()` method. See `InfoListItem.clone()` for more
    information.
    """
    def __init__(self, infolist, keys):
        """
        :string: infolist - WeeChat InfoList item
        :string: keys - WeeChat InfoList keys
        """
        GCObject.__init__(self)
        self._infolist = infolist
        self._keys = {t[2:]: t[0] for t in keys.split(",")}

    def clone(self):
        """
        This method should be used when an item from an InfoList is required
        later. InfoList items are not loaded automatically to improve RAM
        usage. This method returns a Python dict with no metadata attached.

        Usage:

        buffers.append(item.clone())
        """
        self.assert_open()
        return {item: self[item] for item in self._keys}

    def close(self):
        self.assert_open()
        self._closed = True

    def __getitem__(self, index):
        self.assert_open()
        typ = self._keys[index]  # KeyError => index doesn't exist
        if typ == "i":
            return self._infolist.get_integer(index)
        elif typ == "s":
            return self._infolist.get_string(index)
        elif typ == "p":
            return self._infolist.get_pointer(index)
        elif typ == "t":
            return self._infolist.get_time(index)
        else:
            raise Exception("Invalid key for __getitem__", typ)


class InfoList(GCObject):
    """
    Usage:

    with InfoList("buffer") as infolist:
        for item in infolist:
            if item["number"] > 1:
                # do whatever with this buffer :D
                pass
    """

    def __init__(self, name, pointer=None, arguments=None):
        GCObject.__init__(self)
        self.name = name
        args = [name, pointer or "", arguments or ""]
        self._infolist = infolist_get(*args)
        if not self._infolist:
            raise ValueError("invalid infolist: %r" % name)
        self._old_item = InfoListItem("", "a:b")
        self._closed = False

    def get_integer(self, name):
        "Get an integer from an InfoList"
        self.assert_open()
        return infolist_integer(self._infolist, name)

    def get_string(self, name):
        "Get a string from an InfoList"
        self.assert_open()
        return infolist_string(self._infolist, name)

    def get_pointer(self, name):
        "Get a pointer from an InfoList"
        self.assert_open()
        return infolist_pointer(self._infolist, name)

    def get_time(self, name):
        "Get a time value from an InfoList"
        self.assert_open()
        return infolist_time(self._infolist, name)

    def close(self):
        self.assert_open()
        self._closed = True
        infolist_free(self._infolist)

    def __enter__(self):
        self.assert_open()
        return self

    def __exit__(self, typ, traceback, exception):
        self.assert_open()
        self.close()
        return self

    def __iter__(self):
        self.assert_open()
        return self

    def __next__(self):
        return self.next()

    def next(self):
        """
        Return the next item in an InfoList, or raise StopIteration
        """
        self.assert_open()
        if not infolist_next(self._infolist):
            raise StopIteration()
        self._old_item.close()
        new_item = InfoListItem(self, infolist_fields(self._infolist))
        self._old_item = new_item
        return new_item
