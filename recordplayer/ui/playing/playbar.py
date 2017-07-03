from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from ..barbutton import BarButton


class PlayBar(BoxLayout):
    def __init__(self, listener):
        self._listener = listener
        super().__init__(
            size_hint_y=None,
            height=50,
            spacing=5,
            orientation='horizontal'
        )

        # previous track
        self.prev_button = BarButton(
            icon_name="step-backward",
            on_press=listener.on_prev_button_press
        )
        self.add_widget(self.prev_button)

        # currently playing
        self.playing_label = Label(
            text=""
        )
        self.add_widget(self.playing_label)
        
        # next track
        self.next_button = BarButton(
            icon_name="step-forward",
            on_press=listener.on_next_button_press
        )
        self.add_widget(self.next_button)
