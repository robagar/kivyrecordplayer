from kivy.logger import Logger
from ..device import Device


class DummyDevice(Device):
    def set_screen_brightness(self, brightness, duration=None):
        Logger.info('dummy device: screen brightness {0}, duration: {1}'.format(brightness, duration))

    def set_screen_on(self, on):
        Logger.info('dummy device: screen {0}'.format('ON' if on else 'OFF'))
