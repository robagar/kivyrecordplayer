from mpd import MPDClient
from ..player import Player


class MPDPlayer(Player):
    def __init__(self):
        self._mpd = MPDClient()
        self._mpd.connect('localhost', 6600)

    def on_play_record(self):
        self._mpd.clear()
        self._mpd.add(self.playing_record.name)
        self._mpd.play()

    def on_pause(self):
        self._mpd.pause(1)

    def on_resume(self):
        self._mpd.pause(0)

    def on_play_next_track(self):
        m = self._mpd
        m.repeat(1)
        m.next()
        m.repeat(0)

    def on_play_previous_track(self):
        m = self._mpd
        m.repeat(1)
        m.previous()
        m.repeat(0)

    def on_stop(self):
        m = self._mpd
        m.pause()
        m.clear()

    def update(self):
        t = self._mpd.currentsong()
        self._playing_track_name = t.get('title') if t else None

    def rescan(self):
        self._mpd.update()




