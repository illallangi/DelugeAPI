from functools import cached_property

from loguru import logger


class HostConfig(object):
    def __init__(self, host, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self._dictionary = dictionary

        for key in self._dictionary.keys():
            if key not in self._keys:
                logger.warning(f'Unhandled key in {self.__class__}: {key}')
            logger.trace('{}: {}"{}"', key, type(self._dictionary[key]), self._dictionary[key])

    @property
    def _keys(self):
        return [
            b'add_paused',
            b'allow_remote',
            b'auto_managed',
            b'autoadd_enable',
            b'autoadd_location',
            b'cache_expiry',
            b'cache_size',
            b'compact_allocation',
            b'copy_torrent_file',
            b'daemon_port',
            b'del_copy_torrent_file',
            b'dht',
            b'dont_count_slow_torrents',
            b'download_location',
            b'enabled_plugins',
            b'enc_in_policy',
            b'enc_level',
            b'enc_out_policy',
            b'enc_prefer_rc4',
            b'geoip_db_location',
            b'ignore_limits_on_local_network',
            b'info_sent',
            b'listen_interface',
            b'listen_ports',
            b'lsd',
            b'max_active_downloading',
            b'max_active_limit',
            b'max_active_seeding',
            b'max_connections_global',
            b'max_connections_per_second',
            b'max_connections_per_torrent',
            b'max_download_speed',
            b'max_download_speed_per_torrent',
            b'max_half_open_connections',
            b'max_upload_slots_global',
            b'max_upload_slots_per_torrent',
            b'max_upload_speed',
            b'max_upload_speed_per_torrent',
            b'move_completed',
            b'move_completed_path',
            b'natpmp',
            b'new_release_check',
            b'outgoing_ports',
            b'peer_tos',
            b'plugins_location',
            b'prioritize_first_last_pieces',
            b'proxies',
            b'queue_new_to_top',
            b'random_outgoing_ports',
            b'random_port',
            b'rate_limit_ip_overhead',
            b'remove_seed_at_ratio',
            b'seed_time_limit',
            b'seed_time_ratio_limit',
            b'send_info',
            b'share_ratio_limit',
            b'stop_seed_at_ratio',
            b'stop_seed_ratio',
            b'torrentfiles_location',
            b'upnp',
            b'utpex'
        ]

    def __repr__(self):
        return f'{self.__class__}({str(self.host)})'

    def __str__(self):
        return f'{str(self.host)}'

    @cached_property
    def move_completed_path(self):
        return self._dictionary[b'move_completed_path'].decode('UTF-8')

    @property
    def max_download_speed(self):
        return self._dictionary[b'max_download_speed']

    @max_download_speed.setter
    def max_download_speed(self, value):
        self.host.client.call('core.set_config', {b'max_download_speed': value})
        self._dictionary[b'max_download_speed'] = self.host.client.call('core.get_config_value', b'max_download_speed')
