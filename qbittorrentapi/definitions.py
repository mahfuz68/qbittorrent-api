from enum import Enum

try:
    from collections import UserList
except ImportError:
    from UserList import UserList

from qbittorrentapi._attrdict import AttrDict


class APINames(Enum):
    """
    API namespaces for API endpoints.

    e.g 'torrents' in http://localhost:8080/api/v2/torrents/addTrackers
    """

    Authorization = "auth"
    Application = "app"
    Log = "log"
    Sync = "sync"
    Transfer = "transfer"
    Torrents = "torrents"
    RSS = "rss"
    Search = "search"
    EMPTY = ""


class TorrentStates(Enum):
    """
    Torrent States as defined by qBittorrent.

    Definitions:
        - wiki: https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)#get-torrent-list
        - code: https://github.com/qbittorrent/qBittorrent/blob/master/src/base/bittorrent/torrenthandle.h#L52

    :Usage:
        >>> from qbittorrentapi import Client
        >>> from qbittorrentapi import TorrentStates
        >>> client = Client()
        >>> # print torrent hashes for torrents that are downloading
        >>> for torrent in client.torrents_info():
        >>>     # check if torrent is downloading
        >>>     if torrent.state_enum.is_downloading:
        >>>         print(f'{torrent.hash} is downloading...')
        >>>     # the appropriate enum member can be directly derived
        >>>     state_enum = TorrentStates(torrent.state)
        >>>     print(f'{torrent.hash}: {state_enum.value}')
    """

    ERROR = "error"
    MISSING_FILES = "missingFiles"
    UPLOADING = "uploading"
    PAUSED_UPLOAD = "pausedUP"
    QUEUED_UPLOAD = "queuedUP"
    STALLED_UPLOAD = "stalledUP"
    CHECKING_UPLOAD = "checkingUP"
    FORCED_UPLOAD = "forcedUP"
    ALLOCATING = "allocating"
    DOWNLOADING = "downloading"
    METADATA_DOWNLOAD = "metaDL"
    FORCED_METADATA_DOWNLOAD = "forcedMetaDL"
    PAUSED_DOWNLOAD = "pausedDL"
    QUEUED_DOWNLOAD = "queuedDL"
    FORCED_DOWNLOAD = "forcedDL"
    STALLED_DOWNLOAD = "stalledDL"
    CHECKING_DOWNLOAD = "checkingDL"
    CHECKING_RESUME_DATA = "checkingResumeData"
    MOVING = "moving"
    UNKNOWN = "unknown"

    @property
    def is_downloading(self):
        """Returns True if the State is categorized as Downloading."""
        return self in (
            TorrentStates.DOWNLOADING,
            TorrentStates.METADATA_DOWNLOAD,
            TorrentStates.FORCED_METADATA_DOWNLOAD,
            TorrentStates.STALLED_DOWNLOAD,
            TorrentStates.CHECKING_DOWNLOAD,
            TorrentStates.PAUSED_DOWNLOAD,
            TorrentStates.QUEUED_DOWNLOAD,
            TorrentStates.FORCED_DOWNLOAD,
        )

    @property
    def is_uploading(self):
        """Returns True if the State is categorized as Uploading."""
        return self in (
            TorrentStates.UPLOADING,
            TorrentStates.STALLED_UPLOAD,
            TorrentStates.CHECKING_UPLOAD,
            TorrentStates.QUEUED_UPLOAD,
            TorrentStates.FORCED_UPLOAD,
        )

    @property
    def is_complete(self):
        """Returns True if the State is categorized as Complete."""
        return self in (
            TorrentStates.UPLOADING,
            TorrentStates.STALLED_UPLOAD,
            TorrentStates.CHECKING_UPLOAD,
            TorrentStates.PAUSED_UPLOAD,
            TorrentStates.QUEUED_UPLOAD,
            TorrentStates.FORCED_UPLOAD,
        )

    @property
    def is_checking(self):
        """Returns True if the State is categorized as Checking."""
        return self in (
            TorrentStates.CHECKING_UPLOAD,
            TorrentStates.CHECKING_DOWNLOAD,
            TorrentStates.CHECKING_RESUME_DATA,
        )

    @property
    def is_errored(self):
        """Returns True if the State is categorized as Errored."""
        return self in (TorrentStates.MISSING_FILES, TorrentStates.ERROR)

    @property
    def is_paused(self):
        """Returns True if the State is categorized as Paused."""
        return self in (TorrentStates.PAUSED_UPLOAD, TorrentStates.PAUSED_DOWNLOAD)


class ClientCache(object):
    """
    Caches the client.

    Subclass this for any object that needs access to the Client.
    """

    def __init__(self, *args, **kwargs):
        self._client = kwargs.pop("client")
        super(ClientCache, self).__init__(*args, **kwargs)


class Dictionary(ClientCache, AttrDict):
    """Base definition of dictionary-like objects returned from qBittorrent."""

    def __init__(self, data=None, client=None):
        data = self._normalize_data(data)
        super(Dictionary, self).__init__(data or {}, client=client)
        # allows updating properties that aren't necessarily a part of the AttrDict
        self._setattr("_allow_invalid_attributes", True)

    @classmethod
    def _normalize_data(cls, data):
        """iterate through a dictionary converting any nested dictionaries to
        AttrDicts."""
        converted_dict = AttrDict()
        for key, value in (data or {}).items():
            # if the value is a dictionary, convert it to a AttrDict
            if isinstance(value, dict):
                # recursively send each value to convert its dictionary children
                converted_dict[key] = cls._normalize_data(AttrDict(value))
            else:
                converted_dict[key] = value
        return converted_dict


class List(ClientCache, UserList):
    """Base definition for list-like objects returned from qBittorrent."""

    def __init__(self, list_entries=None, entry_class=None, client=None):

        entries = []
        for entry in list_entries or ():
            if isinstance(entry, dict):
                entries.append(entry_class(data=entry, client=client))
            else:
                entries.append(entry)
        super(List, self).__init__(entries, client=client)


class ListEntry(Dictionary):
    """Base definition for objects within a list returned from qBittorrent."""
