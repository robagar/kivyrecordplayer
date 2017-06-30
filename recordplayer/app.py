from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
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
        self.album.widget = self
        self.on_unselected()

    def on_selected(self):
        self.color = [1, 1, 1, 1]

    def on_unselected(self):
        self.color = [1, 1, 1, 0.5]        


class RecordPlayerApp(App):

    def build(self):
        root = BoxLayout(orientation='vertical')
        root.add_widget(self.init_header_bar());
        root.add_widget(self.init_albums_view());
        root.add_widget(self.init_play_bar());
        return root

    def init_header_bar(self):
        hb = self.header_bar = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=5,
            orientation='horizontal'
        )

        # system popup
        self.init_system_popup()
        hb.add_widget(Button(
            text='system',
            size_hint_x=None,
            width=100,
            on_press=self.system_popup.open
        ))
 
        # currently playing
        self.album_label = Label(
            text="(please select an album to play...)"
        )
        hb.add_widget(self.album_label)

        # pause / resume
        self.play_pause_button = Button(
            text="play",
            size_hint_x=None,
            width=100,
            on_press=self.on_play_pause_button_press
        )
        hb.add_widget(self.play_pause_button)

        return hb


    def init_albums_view(self):
        ac = self.album_container = BoxLayout(
            orientation='horizontal',
            padding=15,
            spacing=30, 
            size_hint_x=None
        )

        # TODO uncomment when kivy 1.10 is available
        # ac.bind(minimum_width=ac.setter('width'))
 
        v = self.album_view = ScrollView()
        v.add_widget(ac)
        return v

    def init_play_bar(self):
        pb = self.play_bar = BoxLayout(
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
            on_press=self.on_prev_button_press
        )
        pb.add_widget(self.prev_button)

        # currently playing
        self.playing_label = Label(
            text="(not playing)"
        )
        pb.add_widget(self.playing_label)
        
        # next track
        self.next_button = Button(
            text="next",
            size_hint_x=None,
            width=100,
            on_press=self.on_next_button_press
        )
        pb.add_widget(self.next_button)

        return pb

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

        ac = self.album_container
        n = 0
        for a in self.albums:
            if a.cover_image_path:
                w = RecordWidget(
                    a,
                    on_press=self.on_record_press,
                    size_hint=(None, None), 
                    size=(350, 350), 
                    source=a.cover_image_path, 
                    allow_stretch=True
                )
                ac.add_widget(w)
                n += 1
        ac.width = 30 + n * 380 # hack pending minimum_width in kivy 1.10

        Clock.schedule_interval(lambda dt: self.update_player_status(), 1)

    selected_album = None

    def on_record_press(self, widget):
        album = widget.album
        if not album is self.selected_album:
            if self.selected_album:
                self.selected_album.widget.on_unselected()
            self.selected_album = album
            album.widget.on_selected()
            self.album_view.scroll_to(album.widget, padding=225)
            self.album_label.text = album.name
            self.playing_label.text = ''

        p = self.player
        if p.playing_album and not p.playing_album is album:
            p.stop()
            self.on_stop_playing()

    def on_prev_button_press(self, widget):
        p = self.player
        if p.playing_album:
            p.play_previous_track()

    def on_next_button_press(self, widget):
        p = self.player
        if p.playing_album:
            p.play_next_track()
        elif self.selected_album:
            p.play_album(self.selected_album)
            self.on_playing()

    def on_play_pause_button_press(self, widget):
        album = self.selected_album
        if album:
            p = self.player
            if not p.playing_album is album:
                p.play_album(album)
                self.on_playing()
            elif p.playing:
                p.pause()
                self.on_stop_playing()
            else:
                p.resume() 
                self.on_playing()

    def on_playing(self):
        self.play_pause_button.text = 'pause'

    def on_stop_playing(self):
        self.play_pause_button.text = 'play'

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

    def update_player_status(self):
        p = self.player
        p.update()
        tn = p.playing_track_name
        self.playing_label.text = tn if tn else ''


