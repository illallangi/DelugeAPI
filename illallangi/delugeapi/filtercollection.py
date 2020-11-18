from collections.abc import Sequence

from .filter import Filter


class FilterCollection(Sequence):
    def __init__(self, host, filters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self._filters = [Filter(self.host, filter) for filter in filters]

    def __repr__(self):
        return f'{self.__class__}({self.host.username}@{self.host.hostname}:{self.host.port})[{self.__len__()}]'

    def __str__(self):
        return f'{self.__len__()} Filter{"" if self.__len__() == 1 else "s"}'

    def __iter__(self):
        return self._filters.__iter__()

    def __getitem__(self, key):
        return list(self._filters).__getitem__(key)

    def __len__(self):
        return list(self._filters).__len__()
