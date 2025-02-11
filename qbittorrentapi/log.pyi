from typing import Iterable
from typing import Text

from qbittorrentapi.client import Client
from qbittorrentapi.definitions import ClientCache
from qbittorrentapi.definitions import List
from qbittorrentapi.definitions import ListEntry
from qbittorrentapi.request import Request

class LogPeersList(List):
    def __init__(
        self, list_entries: Iterable = None, client: Client = None
    ) -> None: ...

class LogPeer(ListEntry): ...

class LogMainList(List):
    def __init__(
        self, list_entries: Iterable = None, client: Client = None
    ) -> None: ...

class LogEntry(ListEntry): ...

class Log(ClientCache):
    main: _Main
    def __init__(self, client: Client) -> None: ...
    def peers(
        self, last_known_id: Text | int = None, **kwargs
    ) -> LogPeersList[LogPeer]: ...

    class _Main(ClientCache):
        def _api_call(
            self,
            normal: bool = None,
            info: bool = None,
            warning: bool = None,
            critical: bool = None,
            last_known_id: bool = None,
            **kwargs
        ) -> LogMainList[LogEntry]: ...
        def __call__(
            self,
            normal: bool = None,
            info: bool = None,
            warning: bool = None,
            critical: bool = None,
            last_known_id: bool = None,
            **kwargs
        ) -> LogMainList[LogEntry]: ...
        def info(
            self, last_known_id: Text | int = None, **kwargs
        ) -> LogMainList[LogEntry]: ...
        def normal(
            self, last_known_id: Text | int = None, **kwargs
        ) -> LogMainList[LogEntry]: ...
        def warning(
            self, last_known_id: Text | int = None, **kwargs
        ) -> LogMainList[LogEntry]: ...
        def critical(
            self, last_known_id: Text | int = None, **kwargs
        ) -> LogMainList[LogEntry]: ...

class LogAPIMixIn(Request):
    @property
    def log(self) -> Log: ...
    def log_main(
        self,
        normal: bool = None,
        info: bool = None,
        warning: bool = None,
        critical: bool = None,
        last_known_id: bool = None,
        **kwargs
    ) -> LogMainList[LogEntry]: ...
    def log_peers(
        self, last_known_id: Text | int = None, **kwargs
    ) -> LogPeersList[LogPeer]: ...
