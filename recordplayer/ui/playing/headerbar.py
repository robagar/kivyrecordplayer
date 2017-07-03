from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from ..barbutton import BarButton


class HeaderBar(BoxLayout):
    def __init__(self, listener):
        self._listener = listener
        super().__init__(
            size_hint_y=None,
            height=50,
            spacing=5,
            orientation='horizontal'
        )        

        # show browsing UI
        self.add_widget(BarButton(
            icon_name='music',
            on_press=listener.on_show_browsing_ui_button_press
        ))
 
        # currently playing
        self.album_label = Label(
            text=""
        )
        self.add_widget(self.album_label)

        # pause / resume
        self.play_pause_button = BarButton(
            icon_name="play",
            on_press=listener.on_play_pause_button_press
        )
        self.add_widget(self.play_pause_button)
