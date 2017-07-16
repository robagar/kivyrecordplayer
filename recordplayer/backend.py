from kivy.logger import Logger


class BackendListener:
    def on_backend_state_change(self, old_state, new_state):
        raise NotImplementedError()

    def on_backend_playing_track(self, playing_track_name):
        raise NotImplementedError()


class Backend:
    PLAYING = 'PLAYING'
    PAUSED = 'PAUSED'
    STOPPED = 'STOPPED'

    def __init__(self, name, listener):
        self._name = name
        self._listener = listener

    @property
    def name(self):
        return self._name

    _state = STOPPED
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state != value:
            old_state = self._state
            self._state = value
            self._listener.on_backend_state_change(old_state, self._state)

    @property
    def playing(self):
        return self._state == self.PLAYING

    @property
    def paused(self):
        return self._state == self.PAUSED

    @property
    def stopped(self):
        return self._state == self.STOPPED

    _playing_record = None
    @property
    def playing_record(self):
        return self._playing_record

    _playing_track_name = None
    @property
    def playing_track_name(self):
        return self._playing_track_name

    @playing_track_name.setter
    def playing_track_name(self, value):
        if self._playing_track_name != value:
            self._playing_track_name = value
            self._listener.on_backend_playing_track(value)


    def play_record(self, record):
        Logger.info('PLAY ' + record.name)
        self._playing_record = record
        self._playing = True
        self.on_play_record()

    def on_play_record(self):
        raise NotImplementedError()

    def pause(self):
        Logger.info('Backend: PAUSE')
        self.on_pause()
        self._playing = False

    def on_pause(self):
        pass

    def resume(self):
        Logger.info('Backend: RESUME')
        self.on_resume()
        self._playing = True

    def on_resume(self):
        pass

    def play_next_track(self):
        Logger.info('Backend: NEXT')
        self.on_play_next_track()
        self._playing = True

    def on_play_next_track(self):
        pass

    def play_previous_track(self):
        Logger.info('Backend: PREV')
        self.on_play_previous_track()
        self._playing = True

    def on_play_previous_track(self):
        pass

    def stop(self):
        Logger.info('Backend: STOP')
        self.on_stop()
        self._playing = False
        self._playing_record = None

    def on_stop(self):
        pass

    def update(self):
        pass

    def rescan(self):
        pass


def create_backend(backend_name, listener):
    Logger.info('backend: ' + backend_name)
    if backend_name == 'mpd':
        from .backends.mpd import MPDBackend
        return MPDBackend(listener)
    elif backend_name == 'dummy':
        from .backends.dummy import DummyBackend
        return DummyBackend(listener)
    else:
        Logger.error('failed to create backend: unrecognized backend name {0}'.format(backend_name)) 
