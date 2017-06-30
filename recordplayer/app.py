from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
# from kivy.uix.stacklayout import StackLayout
# from kivy.uix.scrollview import ScrollView
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# from kivy.uix.label import Label
# from kivy.uix.behaviors import ButtonBehavior
# from kivy.uix.popup import Popup

from . import settings
from .player import create_player
from .album import load_albums
from .shutdown import shutdown, reboot
from .ui.playing import create_playing_ui




class RecordPlayerApp(App):

    # def init_albums_view(self):
    #     ac = self.album_container = BoxLayout(
    #         orientation='horizontal',
    #         padding=15,
    #         spacing=30, 
    #         size_hint_x=None
    #     )

    #     # TODO uncomment when kivy 1.10 is available
    #     # ac.bind(minimum_width=ac.setter('width'))
 
    #     v = self.album_view = ScrollView()
    #     v.add_widget(ac)
    #     return v


         
    def build(self):
        ui = create_playing_ui(self)
        self.album_carousel = ui.album_carousel
        self.album_label = ui.header_bar.album_label
        self.playing_label = ui.play_bar.playing_label 
        return ui

    def on_start(self):
        Logger.info('START')
        self.player = create_player(settings.PLAYER)
        self.album_carousel.albums = self.albums = load_albums(settings.MUSIC_PATH)
        Clock.schedule_interval(lambda dt: self.update_player_status(), 1)

    selected_album = None

    def on_album_press(self, album):
        if not album is self.selected_album:
            if self.selected_album:
                self.selected_album.on_unselected()
            self.selected_album = album
            album.on_selected()
            self.album_label.text = album.name
            self.playing_label.text = ''

        p = self.player
        if p.playing_album and not p.playing_album is album:
            p.stop()

    def on_prev_button_press(self, widget):
        album = self.selected_album
        if album:
            self.album_carousel.show_album(album)
            p = self.player
            if p.playing_album is album:
                p.play_previous_track()

    def on_next_button_press(self, widget):
        album = self.selected_album
        if album:
            self.album_carousel.show_album(album)
            p = self.player
            if p.playing_album is album:
                p.play_next_track()
            else:
                p.play_album(album)

    def on_play_pause_button_press(self, widget):
        album = self.selected_album
        if album:
            self.album_carousel.show_album(album)
            p = self.player
            if not p.playing_album is album:
                p.play_album(album)
            elif p.playing:
                p.pause()
            else:
                p.resume() 

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


