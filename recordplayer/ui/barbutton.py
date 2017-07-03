from kivy.uix.button import Button
from .iconfonts import icon


class BarButton(Button):
    def __init__(self, icon_name, **kwargs):
        super().__init__(
            markup=True,
            text=icon('fa-' + icon_name),
            font_size=32,
            size_hint_x=None,
            width=100,
            background_normal='',
            background_color=[0,0,0,1],
            **kwargs
        )

    def set_icon(self, icon_name):
        self.text=icon('fa-' + icon_name)