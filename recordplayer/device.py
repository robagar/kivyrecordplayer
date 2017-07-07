from kivy.logger import Logger
from kivy.clock import Clock
from . import settings


class Device:
    def __init__(self):
        self._schedule_dim_screen = Clock.schedule_once(lambda dt: self.dim_screen(), settings.SCREEN_DIM_TIME)
        self._schedule_off_screen = Clock.schedule_once(lambda dt: self.screen_off(), settings.SCREEN_OFF_TIME)

    _screen_bright = False

    def touch(self):
        self._schedule_dim_screen.cancel()
        self._schedule_dim_screen()

        self._schedule_off_screen.cancel()
        self._schedule_off_screen()

        if not self._screen_bright:
            self.brighten_screen()

    def dim_screen(self):
        Logger.info('DIM SCREEN')
        self.set_screen_brightness(0.1, duration=3)
        self._screen_bright = False

    def screen_off(self):
        Logger.info('SCREEN OFF')
        self.set_screen_on(False)
        self._screen_bright = False

    def brighten_screen(self):
        Logger.info('BRIGHTEN SCREEN')
        self.set_screen_on(True)
        self.set_screen_brightness(1)
        self._screen_bright = True

    def set_screen_on(self, on):
        raise NotImplementedError()

    def set_screen_brightness(self, brightness, duration=None):
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
       