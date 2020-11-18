from collections.abc import Sequence

from .torrent import Torrent


class TorrentCollection(Sequence):
    def __init__(self, host, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        if self.host.client.connected:
            torrents = self.host.client.call('core.get_torrents_status', {}, ['name', 'files', 'hash', 'trackers'])
            self._torrents = [Torrent(self.host, torrents[key]) for key in torrents]

    def __repr__(self):
        return f'{self.__class__}({self.host.username}@{self.host.hostname}:{self.host.port})[{self.__len__()}]'

    def __str__(self):
        return f'{self.__len__()} Torrent{"" if self.__len__() == 1 else "s"}'

    def __iter__(self):
        return self._torrents.__iter__()

    def __getitem__(self, key):
        return list(self._torrents).__getitem__(key)

    def __len__(self):
        return list(self._torrents).__len__()
