from kivy.app import App
from kivy.logger import Logger
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

from . import settings
from .player import create_player
from .album import load_albums


class RecordWidget(ButtonBehavior, Image):
    def __init__(self, album, *args, **kwargs):
        super(RecordWidget, self).__init__(*args, **kwargs)
        self.album = album


class RecordPlayerApp(App):

    def build(self):
        ac = self.album_container = StackLayout(spacing=10, size_hint_y=None)
        ac.bind(minimum_height=ac.setter('height'))
        root = ScrollView()
        root.add_widget(ac)
        return root

    def on_start(self):
        Logger.info('START')
        self.player = create_player(settings.PLAYER)
        self.albums = load_albums(settings.MUSIC_PATH)

        for a in self.albums:
            if a.cover_image_path:
                w = RecordWidget(
                    a,
                    on_press=self.on_record_press,
                    size_hint=(None, None), 
                    size=(150, 150), 
                    source=a.cover_image_path, 
                    allow_stretch=True
                )
                self.album_container.add_widget(w)

    def on_record_press(self, widget):
        a = widget.album
        p = self.player
        if p.playing:
            p.pause()
        elif p.playing_album(a):
            p.resume()
        else:    
            p.play_album(a)
