from mpd import MPDClient
from ..backend import Backend


class MPDBackend(Backend):
    def __init__(self, listener):
        super().__init__('mpd', listener)
        self._mpd = MPDClient()
        self._mpd.connect('localhost', 6600)

    def on_play_record(self):
        self._reset()
        self._mpd.add(self.playing_record.url)
        self._mpd.play()

    def on_pause(self):
        self._mpd.pause(1)

    def on_resume(self):
        self._mpd.pause(0)

    def on_play_next_track(self):
        m = self._mpd
        try:
            m.next()
        except:
            pass

    def on_play_previous_track(self):
        m = self._mpd
        try:
            m.previous()
        except:
            pass

    def on_stop(self):
        m = self._mpd
        m.pause()
        m.clear()

    _mpd_states = {
        'play': Backend.PLAYING,
        'pause': Backend.PAUSED,
        'stop': Backend.STOPPED
    } 

    def update(self):
        t = self._mpd.currentsong()
        self.playing_track_name = t.get('title') if t else None

        status = self._mpd.status()
        self.state = self._mpd_states.get(status.get('state'))

    def rescan(self):
        self._mpd.update()

    def _reset(self):
        m = self._mpd
        m.clear()
        m.repeat(0)
        m.random(0)
        m.single(0)
        m.consume(0)


