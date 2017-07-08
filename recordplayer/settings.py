DEBUG = False
MUSIC_PATH = '/music'
PLAYER = 'mpd'
DEVICE = 'raspberrypi'
SCREEN_DIM_TIME = 3*60
SCREEN_OFF_TIME = 60*60

try:
    from .settings_local import *
except ImportError:
    pass