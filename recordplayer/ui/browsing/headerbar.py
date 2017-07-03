from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class HeaderBar(BoxLayout):
    def __init__(self, listener):
        self._listener = listener
        super().__init__(
            size_hint_y=None,
            height=50,
            spacing=5,
            orientation='horizontal'
        )        

        # system popup
        self.add_widget(Button(
            text='system',
            size_hint_x=None,
            width=100,
            on_press=listener.on_system_button_press
        ))
 
        # currently playing
        self.album_label = Label(
            text=""
        )
        self.add_widget(self.album_label)

        # show playing UI
        self.show_playing_ui_button = Button(
            text="play",
            size_hint_x=None,
            width=100,
            on_press=listener.on_show_playing_ui_button_press
        )
        self.add_widget(self.show_playing_ui_button)
