qBittorrent Web API Client
================================
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/rmartin16/qbittorrent-api/Tests/master?style=flat-square)](https://github.com/rmartin16/qbittorrent-api/actions?query=workflow%3ATests) [![Codecov branch](https://img.shields.io/codecov/c/gh/rmartin16/qbittorrent-api/master?style=flat-square)](https://codecov.io/gh/rmartin16/qbittorrent-api) [![Coverity Scan](https://img.shields.io/coverity/scan/21227?style=flat-square)](https://scan.coverity.com/projects/rmartin16-qbittorrent-api) [![Codacy grade](https://img.shields.io/codacy/grade/e924396ef8e54d918ed4c093834f3708?style=flat-square)](https://app.codacy.com/manual/rmartin16/qbittorrent-api/dashboard)

[![PyPI](https://img.shields.io/pypi/v/qbittorrent-api?style=flat-square)](https://pypi.org/project/qbittorrent-api/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qbittorrent-api?style=flat-square) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/qbittorrent-api?style=flat-square) ![PyPi - Downloads](https://img.shields.io/pypi/dw/qbittorrent-api?color=blue&style=flat-square)

Python client implementation for qBittorrent Web API. Supports qBittorrent v4.1.0+ (i.e. Web API v2.0+).

Currently supports up to qBittorrent [v4.4.3.1](https://github.com/qbittorrent/qBittorrent/releases/tag/release-4.4.3.1) (Web API v2.8.5) released on May 24, 2022.

[Find the full documentation for this client on RTD.](https://qbittorrent-api.readthedocs.io/)

Features
------------
* The entire [qBittorrent Web API](https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)) is implemented.
* qBittorrent version checking for an endpoint's existence/features is automatically handled.
* All Python versions are supported.
* If the authentication cookie expires, a new one is automatically requested in line with any API call.

Installation
------------
Install via pip from [PyPI](https://pypi.org/project/qbittorrent-api/)
```bash
pip install qbittorrent-api
```

Getting Started
---------------
```python
import qbittorrentapi

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(
    host='localhost',
    port=8080,
    username='admin',
    password='adminadmin',
)

# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# display qBittorrent info
print(f'qBittorrent: {qbt_client.app.version}')
print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
for k,v in qbt_client.app.build_info.items(): print(f'{k}: {v}')

# retrieve and show all torrents
for torrent in qbt_client.torrents_info():
    print(f'{torrent.hash[-6:]}: {torrent.name} ({torrent.state})')

# pause all torrents
qbt_client.torrents.pause.all()
```
