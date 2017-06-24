from kivy.logger import Logger


class Player:

    _playing = False
    @property
    def playing(self):
        return self._playing

    _playing_album = None
    def playing_album(self, album):
        return self._playing_album is album

    def play_album(self, album):
        Logger.info('PLAY ' + album.name)
        self._playing_album = album
        self._playing = True
        self.start_playing_album(album)

    def start_playing_album(self, album):
        raise NotImplementedError()

    def pause(self):
        Logger.info('PAUSE')
        self.on_pause()
        self._playing = False

    def on_pause(self):
        pass

    def resume(self):
        Logger.info('RESUME')
        self.on_resume()
        self._playing = True

    def on_resume(self):
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
