import musicplayer
from functools import partial
from kivy.logger import Logger


class Track(object):
    def __init__(self, fn):
                self.url = fn
                self.f = open(fn)

    def __del__(self):
        self.f.close()            

    # `__eq__` is used for the peek stream management
    def __eq__(self, other):
        return self.url == other.url

    # this is used by the player as the data interface
    def readPacket(self, bufSize):
        return self.f.read(bufSize)

    def seekRaw(self, offset, whence):
        r = self.f.seek(offset, whence)
        return self.f.tell()

musicplayer.enableDebugLog(True)
_player = musicplayer.createPlayer()
_player.outSamplerate = 96000 
_playing_album = None

def play(album):
    global _playing_album
    Logger.info('player: PLAY ' + album.name)

    if _player.playing:
        _player.resetPlaying()

    _player.queue = _tracks(album)
    _player.peekQueue = partial(_peek_tracks, album)

    _player.nextSongOnEof = True
    _player.playing = True

    if _playing_album:
        _player.nextSong()
    
    _playing_album = album

def is_playing():
    return _player.playing

def is_playing_album(album):
    return _playing_album is album

def pause():
    if _player.playing:
        Logger.info('player: PAUSE ' + _playing_album.name)
        _player.playing = False

def resume():
    if not _player.playing:
        Logger.info('player: RESUME ' + _playing_album.name)
        _player.playing = True

def _tracks(album):
    for f in album.track_files:
        yield Track(f)

    _on_album_end()

def _peek_tracks(album, n):
    return map(Track, album.track_files[n:])

def _on_album_end():
    global _playing_album
    Logger.info('player: END ' + _playing_album.name)
    _playing_album = None
    _player.nextSongOnEof = False
