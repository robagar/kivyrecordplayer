from kivy.logger import Logger
from ..device import Device


class DummyDevice(Device):
    def set_screen_brightness(self, brightness):
        Logger.info('dummy device: screen brightness {0}'.format(brightness))