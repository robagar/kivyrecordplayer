from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


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
        self.prev_button = Button(
            text="prev",
            size_hint_x=None,
            width=100,
            on_press=listener.on_prev_button_press
        )
        self.add_widget(self.prev_button)

        # currently playing
        self.playing_label = Label(
            text="(not playing)"
        )
        self.add_widget(self.playing_label)
        
        # next track
        self.next_button = Button(
            text="next",
            size_hint_x=None,
            width=100,
            on_press=listener.on_next_button_press
        )
        self.add_widget(self.next_button)
