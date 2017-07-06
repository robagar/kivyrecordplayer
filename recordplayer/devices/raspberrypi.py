from rpi_backlight import set_brightness
from ..device import Device


class RaspberryPiDevice(Device):
    def set_screen_brightness(self, brightness):
        set_brightness(round(brightness * 255), smooth=True, duration=3)    