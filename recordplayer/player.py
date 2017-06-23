from mpd import MPDClient 
from functools import partial
from kivy.logger import Logger


# class Track(object):
#     def __init__(self, fn):
#         self.url = fn


_player = MPDClient()
_player.connect('localhost', 6600)
_playing_album = None

def play(album):
    global _playing_album
    Logger.info('player: PLAY ' + album.name)

    _player.clear()
    _player.add(album.name)
    _player.play()

    # if _player.playing:
    #     _player.resetPlaying()

    # _player.queue = _tracks(album)
    # _player.peekQueue = partial(_peek_tracks, album)

    # _player.nextSongOnEof = True
    # _player.playing = True

    # if _playing_album:
    #     _player.nextSong()
    
    # _playing_album = album

def is_playing():
    return False #_player.playing

def is_playing_album(album):
    return _playing_album is album

def pause():
    pass
    # if _player.playing:
    #     Logger.info('player: PAUSE ' + _playing_album.name)
    #     _player.playing = False

def resume():
    pass
    # if not _player.playing:
    #     Logger.info('player: RESUME ' + _playing_album.name)
    #     _player.playing = True

# def _tracks(album):
#     for f in album.track_files:
#         yield Track(f)

#     _on_album_end()

# def _peek_tracks(album, n):
#     return map(Track, album.track_files[n:])

# def _on_album_end():
#     global _playing_album
#     Logger.info('player: END ' + _playing_album.name)
#     _playing_album = None
#     _player.nextSongOnEof = False
