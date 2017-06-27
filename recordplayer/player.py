from kivy.logger import Logger


class Player:

    _playing = False
    @property
    def playing(self):
        return self._playing

    _playing_album = None
    @property
    def playing_album(self):
        return self._playing_album

    @property
    def playing_track_name(self):
        return '(unknown)'

    def play_album(self, album):
        Logger.info('PLAY ' + album.name)
        self._playing_album = album
        self._playing = True
        self.on_play_album()

    def on_play_album(self):
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
        self._playing_album = None

    def on_stop(self):
        pass

    def update(self):
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
