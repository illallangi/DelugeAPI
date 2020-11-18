class Filter(object):
    def __init__(self, host, tuple, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self._tuple = tuple

    def __repr__(self):
        return f'{self.__class__}({self.key}: {self.value})'

    def __str__(self):
        return f'{self.key}: {self.value}'

    @property
    def iserror(self):
        return self.key == 'Error'

    @property
    def key(self):
        return self._tuple[0].decode('UTF-8')

    @property
    def value(self):
        return self._tuple[1]
