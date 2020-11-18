# DelugeAPI
[![Docker Pulls](https://img.shields.io/docker/pulls/illallangi/delugeapi.svg)](https://hub.docker.com/r/illallangi/delugeapi)
[![Image Size](https://images.microbadger.com/badges/image/illallangi/delugeapi.svg)](https://microbadger.com/images/illallangi/delugeapi)
![Build](https://github.com/illallangi/DelugeAPI/workflows/Build/badge.svg)

Tool and Python bindings to manage the Deluge torrent client

## Installation

```shell
pip install git+git://github.com/illallangi/DelugeAPI.git
```

## Usage

```shell
$ deluge-tool
Usage: deluge-tool [OPTIONS] COMMAND [ARGS]...

Options:
  --log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG|SUCCESS|TRACE]
  --slack-webhook TEXT
  --slack-username TEXT
  --slack-format TEXT
  --help                          Show this message and exit.

Commands:
  configure-hosts
  get-hosts
  rename-files
  restore-trackers
```
