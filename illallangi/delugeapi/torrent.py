from functools import cached_property

from loguru import logger

from .filecollection import FileCollection
from .trackercollection import TrackerCollection


class Torrent(object):
    def __init__(self, host, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self._dictionary = dictionary

        for key in self._dictionary.keys():
            if key not in self._keys:
                raise Exception(f'Unhandled key in {self.__class__}: {key}')
            logger.trace('{}: {}"{}"', key, type(self._dictionary[key]), self._dictionary[key])

    @property
    def _keys(self):
        return [
            b'files',
            b'hash',
            b'name',
            b'trackers',
        ]

    def __repr__(self):
        return f'{self.__class__}({self.hash} - {self.name})'

    def __str__(self):
        return f'{self.hash} - {self.name}'

    @cached_property
    def files(self):
        return FileCollection(self, self._dictionary[b'files'])

    @cached_property
    def hash(self):
        return self._dictionary[b'hash'].decode('UTF-8')

    @cached_property
    def name(self):
        return self._dictionary[b'name'].decode('UTF-8')

    @cached_property
    def trackers(self):
        return TrackerCollection(self, self._dictionary[b'trackers'])

    def force_recheck(self):
        if self.host.client.connected:
            logger.info('Forcing Recheck')
            self.host.client.call('core.force_recheck', [self.hash])
