from . import base
from .AlbumPlaylistId import AlbumPlaylistId
from .AlbumBrowseId import AlbumBrowseId
from . import utils

__type__ = __name__.split('.')[-1]
__all__  = (__type__,)

class AlbumId(base.BaseType):
    _patterns = utils.patterns \
    (
        AlbumPlaylistId,
        AlbumBrowseId,
    )