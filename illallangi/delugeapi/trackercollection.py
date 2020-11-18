from collections.abc import Sequence
from functools import cached_property
from re import compile

from loguru import logger

from .tracker import Tracker


TRACKER_REGEX = compile(r'[^.]+\.[^.]+$')


class TrackerCollection(Sequence):
    def __init__(self, torrent, sequence, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.torrent = torrent
        self._sequence = [Tracker(self.torrent, t) for t in sequence]

    def __repr__(self):
        return f'{self.__class__}()[{self.__len__()}] - {self.tracker}'

    def __str__(self):
        return f'{self.__len__()} Tracker{"" if self.__len__() == 1 else "s"} - {self.tracker}'

    def __iter__(self):
        return self._sequence.__iter__()

    def __getitem__(self, key):
        return self._sequence.__getitem__(key)

    def __len__(self):
        return self._sequence.__len__()

    @cached_property
    def tracker(self):
        if self.__len__() == 0:
            logger.warning('"{}" on {} has no trackers', self.torrent, self.torrent.host)
            return None
        return '.'.join(sorted((tracker for tracker in self if tracker.tier == sorted(self, key=lambda x: x.tier)[0].tier), key=lambda x: x.url)[0].url.host.split('.')[-2:])

    def set(self, value):
        if self.torrent.host.client.connected:
            logger.info('Setting Tracker')
            self.torrent.host.client.call('core.set_torrent_trackers', self.torrent.hash, [{'tier': 0, 'url': v.encode('UTF-8')} for v in value])
