class Filter(object):
    def __init__(self, host, tuple, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self._tuple = tuple

    def __repr__(self):
        return f'{self.__class__}({self.key}: {self.value})'

    def __str__(self):
        return f'{self.key}: {self.value:3}'

    @property
    def fg(self):
        if self.key == 'Seeding':
            return 'green'
        if self.key == 'Downloading':
            return 'yellow'
        if self.key == 'Queued':
            return 'cyan'
        if self.key == 'Checking':
            return 'blue'
        if self.key == 'Paused':
            return 'red'
        if self.key == 'Error':
            return 'red'
        return None

    @property
    def key(self):
        return self._tuple[0].decode('UTF-8')

    @property
    def value(self):
        return self._tuple[1]
