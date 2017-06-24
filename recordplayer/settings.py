MUSIC_PATH = '/music'
PLAYER = 'mpd'

try:
    from .settings_local import *
except ImportError:
    pass