from kivy.logger import Logger


class Player:

    _playing = False
    @property
    def playing(self):
        return self._playing

    _playing_record = None
    @property
    def playing_record(self):
        return self._playing_record

    _playing_track_name = None
    @property
    def playing_track_name(self):
        return self._playing_track_name

    def play_record(self, record):
        Logger.info('PLAY ' + record.name)
        self._playing_record = record
        self._playing = True
        self.on_play_record()

    def on_play_record(self):
        raise NotImplementedError()

    def pause(self):
        Logger.info('Player: PAUSE')
        self.on_pause()
        self._playing = False

    def on_pause(self):
        pass

    def resume(self):
        Logger.info('Player: RESUME')
        self.on_resume()
        self._playing = True

    def on_resume(self):
        pass

    def play_next_track(self):
        Logger.info('Player: NEXT')
        self.on_play_next_track()
        self._playing = True

    def on_play_next_track(self):
        pass

    def play_previous_track(self):
        Logger.info('Player: PREV')
        self.on_play_previous_track()
        self._playing = True

    def on_play_previous_track(self):
        pass

    def stop(self):
        Logger.info('Player: STOP')
        self.on_stop()
        self._playing = False
        self._playing_record = None

    def on_stop(self):
        pass

    def update(self):
        pass

    def rescan(self):
        pass

def create_player(player_name):
    Logger.info('player: ' + player_name)
    if player_name == 'mpd':
        from .players.mpd import MPDPlayer
        return MPDPlayer()
    elif player_name == 'dummy':
        from .players.dummy import DummyPlayer
        return DummyPlayer()
    else:
        Logger.error('failed to create player: unrecognized player name {0}'.format(player_name)) 
