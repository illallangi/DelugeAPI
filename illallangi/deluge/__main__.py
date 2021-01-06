from html import unescape
from re import Pattern, compile
from sys import stderr

from beets.util import asciify_path, sanitize_path

from click import Choice as CHOICE, FLOAT, STRING, argument, confirm, echo, group, option, style

from illallangi.delugeapi import API as DELUGE_API
from illallangi.orpheusapi import API as ORP_API
from illallangi.redactedapi import API as RED_API
from illallangi.torrentapi import API as TORRENT_API

from loguru import logger

from notifiers.logging import NotificationHandler


@group()
@option('--log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        default='DEBUG')
@option('--slack-webhook',
        type=STRING,
        envvar='SLACK_WEBHOOK',
        default=None)
@option('--slack-username',
        type=STRING,
        envvar='SLACK_USERNAME',
        default=__name__)
@option('--slack-format',
        type=STRING,
        envvar='SLACK_FORMAT',
        default='{message}')
def cli(log_level, slack_webhook, slack_username, slack_format):
    logger.remove()
    logger.add(stderr, level=log_level)

    if slack_webhook:
        params = {
            "username": slack_username,
            "webhook_url": slack_webhook
        }
        slack = NotificationHandler("slack", defaults=params)
        logger.add(slack, format=slack_format, level="SUCCESS")


@cli.command(name='configure-hosts')
@argument('host-filter',
          type=STRING,
          default='')
@option('--max-download-speed',
        type=FLOAT)
def configure_hosts(host_filter, max_download_speed):
    hosts = DELUGE_API()
    host_filter = compile(host_filter) if not isinstance(host_filter, Pattern) else host_filter

    filtered_hosts = [host for host in hosts if host_filter.search(str(host))]
    logger.info(f'{hosts} ({len(filtered_hosts)} filtered):')
    for host in filtered_hosts:
        logger.info(f'  {host}:')
        if (max_download_speed and host.config.max_download_speed != max_download_speed):
            logger.info(f'    Changing max_download_speed from {host.config.max_download_speed} to {max_download_speed}')
            host.config.max_download_speed = max_download_speed


@cli.command(name='get-hosts')
@argument('host-filter',
          type=STRING,
          default='')
@argument('torrent-filter',
          type=STRING,
          default='')
def get_hosts(host_filter, torrent_filter):
    hosts = DELUGE_API()
    host_filter = compile(host_filter) if not isinstance(host_filter, Pattern) else host_filter

    filtered_hosts = [host for host in hosts if host_filter.search(str(host))]
    logger.info(f'{hosts} ({len(filtered_hosts)} filtered):')
    for host in filtered_hosts:
        echo(f'  {host}:', nl=False)
        echo(f' [{len(host.state_tree)} state filter(s):', nl=False)
        for filter in host.state_tree:
            if filter.value > 0 and filter.fg:
                echo(style(f'{filter}, ', fg=filter.fg), nl=False)
            else:
                echo(style(f'{filter}, '), nl=False)
        echo(f'],[{len(host.tracker_tree)} tracker filter(s):', nl=False)
        for filter in host.tracker_tree:
            if filter.value > 0 and filter.fg:
                echo(style(f'{filter}, ', fg=filter.fg), nl=False)
            else:
                echo(style(f'{filter}, '), nl=False)
        echo(f']')


@cli.command(name='restore-trackers')
@argument('host-filter',
          type=STRING,
          default='')
@argument('torrent-filter',
          type=STRING,
          default='')
def restore_trackers(host_filter, torrent_filter):
    torrent_api = TORRENT_API()
    hosts = DELUGE_API()
    host_filter = compile(host_filter) if not isinstance(host_filter, Pattern) else host_filter
    torrent_filter = compile(torrent_filter) if not isinstance(torrent_filter, Pattern) else torrent_filter

    filtered_hosts = [host for host in hosts if host_filter.search(str(host))]
    logger.info(f'{hosts} ({len(filtered_hosts)} filtered):')
    for host in filtered_hosts:
        logger.info(f'  {host}:')
        filtered_torrents = [torrent for torrent in host.torrents if torrent_filter.search(str(torrent))]
        logger.info(f'    {host.torrents} ({len(filtered_torrents)} filtered):')
        for torrent in filtered_torrents:
            if len(torrent.trackers) == 0:
                torrent_file = torrent_api.get_torrent(torrent.hash)
                logger.info(f'      {torrent}:')
                logger.info(f'      {torrent_file.announce_list}')
                torrent.trackers.set([
                    url
                    for tier in torrent_file.announce_list
                    for url in tier])


@cli.command(name='rename-files')
@argument('host-filter',
          type=STRING,
          default='')
@argument('torrent-filter',
          type=STRING,
          default='')
@option('--orpheus-api-key',
        envvar='ORP_API_KEY',
        type=STRING)
@option('--redacted-api-key',
        envvar='RED_API_KEY',
        type=STRING)
def rename_files(host_filter, torrent_filter, orpheus_api_key, redacted_api_key):
    hosts = DELUGE_API()
    apis = []

    if (orpheus_api_key):
        logger.trace('Testing Orpheus API configuration')
        orp_api = ORP_API(orpheus_api_key)
        orp_index = orp_api.get_index()
        logger.success(f'Connected to Orpheus as {orp_index.username}')
        apis.append(orp_api)

    if (redacted_api_key):
        logger.trace('Testing Redacted API configuration')
        red_api = RED_API(redacted_api_key)
        red_index = red_api.get_index()
        logger.success(f'Connected to Redacted as {red_index.username}')
        apis.append(red_api)

    host_filter = compile(host_filter) if not isinstance(host_filter, Pattern) else host_filter
    torrent_filter = compile(torrent_filter) if not isinstance(torrent_filter, Pattern) else torrent_filter

    filtered_hosts = [host for host in hosts if host_filter.search(str(host))]
    logger.info(f'{hosts} ({len(filtered_hosts)} filtered):')
    total_torrents = 0
    total_files = 0
    renamed_torrents = 0
    renamed_files = 0
    failed_torrents = 0
    failed_files = 0
    for host in filtered_hosts:
        logger.info(f'  {host}:')
        filtered_torrents = [torrent for torrent in host.torrents if torrent_filter.search(str(torrent))]
        logger.info(f'    {host.torrents} ({len(filtered_torrents)} filtered):')
        for torrent in filtered_torrents:
            total_torrents += 1
            logger.info(f'      {torrent}:')
            logger.info(f'        {torrent.trackers}:')
            for tracker in torrent.trackers:
                logger.info(f'          {tracker}')
            logger.info(f'        {torrent.files}:')
            changed = False
            failed = False
            prompt = False
            for api in apis:
                if torrent.trackers.tracker in api.supported_trackers:
                    logger.success(f'Renaming files with {type(api)}')
                    for file in torrent.files:
                        total_files += 1
                        logger.info(f'          {file}')
                        result = api.rename_torrent_file(torrent.hash, file.path)
                        if result is None:
                            failed_files += 1
                            failed = True
                            continue
                        path = sanitize_path(asciify_path(unescape(result), '_')).replace('_', '').replace(' (VBR)]', ']')
                        if file.path != path and (not prompt or confirm(f'Rename {file.path} to {path}?', default=True)):
                            renamed_files += 1
                            file.path = path
                            changed = True
            if changed:
                renamed_torrents += 1
                torrent.force_recheck()
            if failed:
                failed_torrents += 1

    echo(f'Checked {total_files} files in {total_torrents} torrents', nl=False)
    if renamed_files > 0:
        echo(', ' + style(f'renamed {renamed_files} files in {renamed_torrents} torrents', fg='green'), nl=False)
    if failed_files > 0:
        echo(', ' + style(f'failed {failed_files} files in {failed_torrents} torrents', fg='red'), nl=False)
    echo('.')


if __name__ == "__main__":
    cli()
