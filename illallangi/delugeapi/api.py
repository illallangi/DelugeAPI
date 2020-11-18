from collections.abc import Sequence
from functools import cached_property
from json import JSONDecoder
from os.path import exists, join
from re import compile

from click import get_app_dir

from loguru import logger

from .host import Host

NOT_WHITESPACE = compile(r'[^\s]')


class API(Sequence):
    def __init__(self, config_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_path = get_app_dir('deluge') if not config_path else config_path

    def __repr__(self):
        return f'{self.__class__}({self.config_path})[{self.__len__()}]'

    def __str__(self):
        return f'{self.__len__()} Host{"" if self.__len__() == 1 else "s"}'

    def __iter__(self):
        return self._hosts.__iter__()

    def __getitem__(self, key):
        return list(self._hosts).__getitem__(key)

    def __len__(self):
        return list(self._hosts).__len__()

    @cached_property
    def _hosts(self):
        if not exists(self.hostlist_path):
            logger.warning('{} not found, no hosts configured', self.hostlist_path)
            return
        pos = 0
        decoder = JSONDecoder()
        with open(self.hostlist_path) as file:
            document = file.read()
            while True:
                match = NOT_WHITESPACE.search(document, pos)
                if not match:
                    break
                pos = match.start()
                obj, pos = decoder.raw_decode(document, pos)
                if 'hosts' in obj.keys():
                    for host in obj['hosts']:
                        yield Host(
                            hostname=host[1],
                            port=host[2],
                            username=host[3],
                            password=host[4]
                        )

    @cached_property
    def hostlist_path(self):
        return join(self.config_path, 'hostlist.conf.1.2')
