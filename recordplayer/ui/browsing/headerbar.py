from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from ..system import create_system_popup


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
            on_press=create_system_popup(listener).open
        ))
 
        # currently playing
        self.title_label = Label(
            text=""
        )
        self.add_widget(self.title_label)

        # show playing UI
        self.show_playing_ui_button = Button(
            text="play",
            size_hint_x=None,
            width=100,
            on_press=listener.on_show_playing_ui_button_press
        )
        self.add_widget(self.show_playing_ui_button)
