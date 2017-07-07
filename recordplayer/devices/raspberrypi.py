import rpi_backlight as bl
from ..device import Device


class RaspberryPiDevice(Device):
    def set_screen_brightness(self, brightness):
        bl.set_power(brightness > 0.5)
        # bl.set_brightness(round(brightness * 255), smooth=True, duration=3)    