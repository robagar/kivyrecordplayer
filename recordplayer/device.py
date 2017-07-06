from kivy.logger import Logger
from kivy.clock import Clock
from .settings import SCREEN_DIM_TIME


class Device:
    def __init__(self):
        self._schedule_dim_screen = Clock.schedule_once(lambda dt: self.dim_screen(), SCREEN_DIM_TIME)

    _screen_dimmed = False

    def touch(self):
        self._schedule_dim_screen.cancel()
        self._schedule_dim_screen()

        if self._screen_dimmed:
            self.brighten_screen()

    def dim_screen(self):
        Logger.info('DIM SCREEN')
        self.set_screen_brightness(0.25)
        self._screen_dimmed = True

    def brighten_screen(self):
        Logger.info('BRIGHTEN SCREEN')
        self.set_screen_brightness(1)
        self._screen_dimmed = False

    def set_screen_brightness(self, brightness):
        raise NotImplementedError()

def create_device(device_name):
    Logger.info('device: ' + device_name)
    if device_name == 'raspberrypi':
        from .devices.raspberrypi import RaspberryPiDevice
        return RaspberryPiDevice()
    elif device_name == 'dummy':
        from .devices.dummy import DummyDevice
        return DummyDevice()
    else:
        Logger.error('failed to create device: unrecognized device name {0}'.format(device_name)) 
       