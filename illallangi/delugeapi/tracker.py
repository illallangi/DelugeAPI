from functools import cached_property

from loguru import logger

from yarl import URL


class Tracker(object):
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
            b'complete_sent',
            b'fail_limit',
            b'fails',
            b'last_error',
            b'message',
            b'min_announce',
            b'next_announce',
            b'scrape_complete',
            b'scrape_downloaded',
            b'scrape_incomplete',
            b'send_stats',
            b'source',
            b'start_sent',
            b'tier',
            b'trackerid',
            b'updating',
            b'url',
            b'verified',
        ]

    def __repr__(self):
        return f'{self.__class__}({self.tier}: {self.url})'

    def __str__(self):
        return f'{self.tier}: {self.url}'

    @cached_property
    def complete_sent(self):
        # TODO: implement return self._dictionary[b'complete_sent'].decode('UTF-8')
        pass

    @cached_property
    def fail_limit(self):
        # TODO: implement return self._dictionary[b'fail_limit'].decode('UTF-8')
        pass

    @cached_property
    def fails(self):
        # TODO: implement return self._dictionary[b'fails'].decode('UTF-8')
        pass

    @cached_property
    def last_error(self):
        # TODO: implement return self._dictionary[b'last_error'].decode('UTF-8')
        pass

    @cached_property
    def message(self):
        return self._dictionary[b'message'].decode('UTF-8')

    @cached_property
    def min_announce(self):
        # TODO: implement return self._dictionary[b'min_announce'].decode('UTF-8')
        pass

    @cached_property
    def next_announce(self):
        # TODO: implement return self._dictionary[b'next_announce'].decode('UTF-8')
        pass

    @cached_property
    def scrape_complete(self):
        # TODO: implement return self._dictionary[b'scrape_complete'].decode('UTF-8')
        pass

    @cached_property
    def scrape_downloaded(self):
        # TODO: implement return self._dictionary[b'scrape_downloaded'].decode('UTF-8')
        pass

    @cached_property
    def scrape_incomplete(self):
        # TODO: implement return self._dictionary[b'scrape_incomplete'].decode('UTF-8')
        pass

    @cached_property
    def send_stats(self):
        # TODO: implement return self._dictionary[b'send_stats'].decode('UTF-8')
        pass

    @cached_property
    def source(self):
        # TODO: implement return self._dictionary[b'source'].decode('UTF-8')
        pass

    @cached_property
    def start_sent(self):
        # TODO: implement return self._dictionary[b'start_sent'].decode('UTF-8')
        pass

    @cached_property
    def tier(self):
        return self._dictionary[b'tier']

    @cached_property
    def trackerid(self):
        # TODO: implement return self._dictionary[b'trackerid'].decode('UTF-8')
        pass

    @cached_property
    def updating(self):
        # TODO: implement return self._dictionary[b'updating'].decode('UTF-8')
        pass

    @cached_property
    def url(self):
        return URL(self._dictionary[b'url'].decode('UTF-8'))

    @cached_property
    def verified(self):
        # TODO: implement return self._dictionary[b'verified'].decode('UTF-8')
        pass
