from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from . import settings
from .device import create_device
from .player import create_player
from .album import load_albums
from .shutdown import shutdown, reboot
from .ui.browsing import create_browsing_ui
from .ui.playing import create_playing_ui
from .ui.system import create_system_popup


class RecordPlayerApp(App):
         
    def build(self):
        ui = self.playing_ui = create_playing_ui(self)
        self.album_carousel = ui.album_carousel
        self.album_label = ui.header_bar.album_label
        self.play_pause_button = ui.header_bar.play_pause_button
        self.playing_label = ui.play_bar.playing_label 

        ui = self.browsing_ui = create_browsing_ui(self)
        self.album_browser = ui.album_browser
 
        root = BoxLayout()
        root.add_widget(Label(
            text='loading...'
        ))

        return root

    def on_start(self):
        Logger.info('START')
        self.device = create_device(settings.DEVICE)
        self.player = create_player(settings.PLAYER)
        self.init_albums()
        Clock.schedule_interval(lambda dt: self.update_player_status(), 1)
        self.show_browsing_ui()
        self.root_window.bind(on_touch_down=self.on_window_touch_down)

    def init_albums(self):
        self.albums \
            = self.album_carousel.albums \
            = self.album_browser.albums \
            = load_albums(settings.MUSIC_PATH)

    _selected_album = None
    @property
    def selected_album(self):
        return self._selected_album

    @selected_album.setter
    def selected_album(self, album):
        if not album is self._selected_album:
            Logger.info('SELECT ' + album.name if album else '(none)')
            if self._selected_album:
                self._selected_album.on_unselected()
            self._selected_album = album
            if album:
                album.on_selected()
                self.album_label.text = album.name
            else:
                self.album_label.text = ''
            self.playing_label.text = ''

    def on_show_playing_ui_button_press(self,  widget):
        self.show_playing_ui()

    def on_show_browsing_ui_button_press(self,  widget):
        self.show_browsing_ui()

    def show_playing_ui(self, album=None):
        self.show_ui(self.playing_ui)
        if album:
           self.selected_album = album 
        if self.selected_album:
            self.album_carousel.show_album(self.selected_album)

    def show_browsing_ui(self):
        self.show_ui(self.browsing_ui)
        self.album_browser.reset()
        if self.selected_album:
            self.album_browser.show_album(self.selected_album)

    def on_browse_album_press(self, album):
        if not self.selected_album is album:
            self.selected_album = album
        else:
            self.show_playing_ui()
            self.player.play_album(album)
        self.update_play_pause()

    def show_ui(self, ui):
        r = self.root
        r.clear_widgets()
        r.add_widget(ui)

    def on_album_press(self, album):
        p = self.player
        if self.selected_album is album:
            if not p.playing_album is album:
                p.play_album(album)
            elif p.playing:
                p.pause()
            else:
                p.resume()
        else:           
            self.selected_album = album
            if p.playing_album and not p.playing_album is album:
                p.stop()
        self.update_play_pause()

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
        self.update_play_pause()

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
        self.update_play_pause()

    def on_rescan_press(self, widget):
        Logger.info('RESCAN')
        self._system_popup.dismiss()
        p = self.player
        p.stop()
        p.rescan()
        self.selected_album = None
        self.init_albums()

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

    _system_popup = None
    def on_system_button_press(self, widget):
        if not self._system_popup:
            self._system_popup = create_system_popup(self)
        self._system_popup.open()

    def update_play_pause(self):
        b = self.play_pause_button
        b.set_icon('pause' if self.player.playing else 'play')

    def on_window_touch_down(self, *args, **kwargs):
        # Logger.info('window touch')
        self.device.touch()
