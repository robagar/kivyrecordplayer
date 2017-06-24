from mpd import MPDClient
from ..player import Player


def MPDPlayer(Player):
    def __init__(self):
        self._mpd = MPDClient()
        self._mpd.connect('localhost', 6600)

    def start_playing_album(self, album):
        self._mpd.clear()
        self._mpd.add(album.name)
        self._mpd.play()

    def on_pause(self):
        self._mpd.pause(1)

    def on_resume(self):
        self._mpd.pause(0)
