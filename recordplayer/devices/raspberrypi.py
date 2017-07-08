import rpi_backlight as bl
from ..device import Device


class RaspberryPiDevice(Device):

    def __init__(self):
        super().__init__()
        self._max_brightness = bl.get_max_brightness()

    def set_screen_brightness(self, brightness, duration=None):
        b = round(brightness * 255)
        if duration:
            bl.set_brightness(b, smooth=True, duration=duration)
        else:
            bl.set_brightness(b)

    def set_screen_on(self, on):
        bl.set_power(on)
