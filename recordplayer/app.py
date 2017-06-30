from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.uix.widget import Widget

from . import settings
from .player import create_player
from .album import load_albums
from .shutdown import shutdown, reboot
from .ui.albums import create_browsing_ui
from .ui.playing import create_playing_ui


class RecordPlayerApp(App):
         
    def build(self):


        ui = create_playing_ui(self)
        self.album_carousel = ui.album_carousel
        self.album_label = ui.header_bar.album_label
        self.playing_label = ui.play_bar.playing_label 

        self.browsing_ui = create_browsing_ui(self)
        self.album_browser = self.browsing_ui.album_browser 

        # root = Widget()
        # root.add_widget(self.browsing_ui)

        return self.browsing_ui

    def on_start(self):
        Logger.info('START')
        self.player = create_player(settings.PLAYER)
        self.albums \
            = self.album_carousel.albums \
            = self.album_browser.albums \
            = load_albums(settings.MUSIC_PATH)
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


