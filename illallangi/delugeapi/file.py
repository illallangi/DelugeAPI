from loguru import logger


class File(object):
    def __init__(self, torrent, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.torrent = torrent
        self._dictionary = dictionary

        for key in self._dictionary.keys():
            if key not in self._keys:
                raise Exception(f'Unhandled key in {self.__class__}: {key}')
            logger.trace('{}: {}"{}"', key, type(self._dictionary[key]), self._dictionary[key])

    @property
    def _keys(self):
        return [
            b'index',
            b'size',
            b'offset',
            b'path',
        ]

    def __repr__(self):
        return f'{self.__class__}({self.index}: {self.path})'

    def __str__(self):
        return f'{self.index}: {self.path}'

    @property
    def index(self):
        return self._dictionary[b'index']

    @property
    def size(self):
        return self._dictionary[b'size']

    @property
    def offset(self):
        return self._dictionary[b'offset']

    @property
    def path(self):
        return self._dictionary[b'path'].decode('UTF-8')

    @path.setter
    def path(self, value):
        self._dictionary[b'path'] = value.encode('UTF-8')
        if self.torrent.host.client.connected:
            logger.info('Renaming File')
            self.torrent.host.client.call('core.rename_files', self.torrent.hash, [[self.index, value.encode('UTF-8')]])
