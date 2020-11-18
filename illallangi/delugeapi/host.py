from functools import cached_property

from deluge_client import DelugeRPCClient

from .filtercollection import FilterCollection
from .hostconfig import HostConfig
from .torrentcollection import TorrentCollection


class Host(object):
    def __init__(self, hostname, port, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def __repr__(self):
        return f'{self.__class__}({self.username}@{self.hostname}:{self.port})'

    def __str__(self):
        return f'{self.username}@{self.hostname}:{self.port}'

    @cached_property
    def client(self):
        client = DelugeRPCClient(self.hostname, self.port, self.username, self.password)
        client.connect()
        return client

    @cached_property
    def torrents(self):
        return TorrentCollection(self)

    @cached_property
    def config(self):
        return HostConfig(self, self.client.call('core.get_config'))

    @cached_property
    def state_tree(self):
        return FilterCollection(self, self.client.call('core.get_filter_tree')[b'state'])

    @cached_property
    def tracker_tree(self):
        return FilterCollection(self, self.client.call('core.get_filter_tree')[b'tracker_host'])
