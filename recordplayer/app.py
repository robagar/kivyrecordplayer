from kivy.app import App
from kivy.logger import Logger
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup

from . import settings
from .player import create_player
from .album import load_albums
from .shutdown import shutdown, reboot


class RecordWidget(ButtonBehavior, Image):
    def __init__(self, album, *args, **kwargs):
        super(RecordWidget, self).__init__(*args, **kwargs)
        self.album = album


class RecordPlayerApp(App):

    def build(self):
        root = BoxLayout(orientation='vertical')
        root.add_widget(self.init_albums_view());
        root.add_widget(self.init_toolbar());
        return root

    def init_albums_view(self):
        ac = self.album_container = StackLayout(
            padding=10,
            spacing=10#, 
            # size_hint_y=None
        )
        # ac.bind(minimum_height=ac.setter('height'))
        v = ScrollView()
        v.add_widget(ac)
        return v

    def init_toolbar(self):
        tb = self.toolbar = BoxLayout(
            size_hint_y=None,
            height=50,
            padding=5,
            spacing=5,
            orientation='horizontal'
        )

        # previous track
        self.prev_button = Button(
            text="prev",
            size_hint_x=None,
            width=100,
            on_press=self.on_prev_button_press
        )
        tb.add_widget(self.prev_button)

        # pause / resume
        self.pause_button = Button(
            text="pause",
            size_hint_x=None,
            width=100,
            on_press=self.on_pause_button_press
        )
        tb.add_widget(self.pause_button)
        
        # next track
        self.next_button = Button(
            text="next",
            size_hint_x=None,
            width=100,
            on_press=self.on_next_button_press
        )
        tb.add_widget(self.next_button)
        
        # currently playing
        self.playing_label = Label(
            text="(not playing)"
        )
        tb.add_widget(self.playing_label)

        # system popup
        self.init_system_popup()
        tb.add_widget(Button(
            text='system',
            size_hint_x=None,
            width=100,
            on_press=self.system_popup.open
        ))
        return tb

    def init_system_popup(self):
        c = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10
        )
        c.add_widget(Button(
            text='shutdown',
            on_press=self.on_shutdown_press
        ))
        c.add_widget(Button(
            text='reboot',
            on_press=self.on_reboot_press
        ))
        self.system_popup = Popup(
            title='Record Player',
            size_hint=(0.5, 0.5),
            content=c
        )

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

    def on_prev_button_press(self, widget):
        pass

    def on_next_button_press(self, widget):
        pass

    def on_pause_button_press(self, widget):
        pass

    def on_shutdown_press(self, widget):
        if not settings.DEBUG:
            Logger.info('RecordPlayer: SHUTDOWN')
            shutdown()
        else:
            Logger.info('RecordPlayer: SHUTDOWN (not really - DEBUG is true)')

    def on_reboot_press(self, widget):
        if not settings.DEBUG:
            Logger.info('RecordPlayer: REBOOT')
            reboot()
        else:
            Logger.info('RecordPlayer: REBOOT (not really - DEBUG is true)')
