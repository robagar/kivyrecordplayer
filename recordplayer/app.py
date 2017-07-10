from cProfile import Profile

from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from . import settings
from .device import create_device
from .player import create_player
from .record import load_records
from .shutdown import shutdown, reboot
from .ui.browsing import create_browsing_ui
from .ui.playing import create_playing_ui
from .ui.system import create_system_popup


class RecordPlayerApp(App):

    PLAYING = 'playing'
    BROWSING = 'browsing'
         
    def build(self):
        ui = self.playing_ui = create_playing_ui(self)
        s = self.playing_screen = Screen(name=self.PLAYING)
        s.add_widget(ui)
        self.record_carousel = ui.record_carousel
        self.record_label = ui.header_bar.record_label
        self.play_pause_button = ui.header_bar.play_pause_button
        self.playing_label = ui.play_bar.playing_label 

        ui = self.browsing_ui = create_browsing_ui(self)
        s = self.browsing_screen = Screen(name=self.BROWSING)
        s.add_widget(ui)
        self.record_browser = ui.record_browser
 
        sm = self.screen_manager = ScreenManager(transition=FadeTransition())
        sm.add_widget(self.browsing_screen)
        sm.add_widget(self.playing_screen)

        return sm

    def on_start(self):
        Logger.info('START')
        self.profile = Profile()
        self.profile.enable()
        Clock.schedule_once(self.end_profiling, 3*60)

        self.device = create_device(settings.DEVICE)
        self.player = create_player(settings.PLAYER)
        self.init_records()
        Clock.schedule_interval(lambda dt: self.update_player_status(), 1)
        self.show_browsing_ui()
        self.root_window.bind(on_touch_down=self.on_window_touch_down)

    def init_records(self):
        self.records \
            = self.record_carousel.records \
            = self.record_browser.records \
            = load_records(settings.MUSIC_PATH)

    _selected_record = None
    @property
    def selected_record(self):
        return self._selected_record

    @selected_record.setter
    def selected_record(self, record):
        if not record is self._selected_record:
            Logger.info('SELECT ' + record.name if record else '(none)')
            if self._selected_record:
                self._selected_record.on_unselected()
            self._selected_record = record
            if record:
                record.on_selected()
                self.record_label.text = record.name
            else:
                self.record_label.text = ''
            self.playing_label.text = ''

    def on_show_playing_ui_button_press(self,  widget):
        self.show_playing_ui()

    def on_show_browsing_ui_button_press(self,  widget):
        self.show_browsing_ui()

    def show_playing_ui(self):
        self.selected_record = self.player.playing_record or self.selected_record
        self.screen_manager.current = self.PLAYING
        if self.selected_record:
            self.record_carousel.show_record(self.selected_record)

    def show_browsing_ui(self):
        self.screen_manager.current = self.BROWSING
        self.record_browser.reset()
        if self.selected_record:
            self.record_browser.show_record(self.selected_record)
            self.selected_record = None

    def on_browse_record_press(self, record):
        if self.selected_record is record:
            self.player.play_record(record)
            self.show_playing_ui()
        elif not self.selected_record:
            self.selected_record = record
        else:
            self.selected_record = None
        self.update_play_pause()
        return self.selected_record

    def on_record_press(self, record):
        p = self.player
        if self.selected_record is record:
            if not p.playing_record is record:
                p.play_record(record)
            elif p.playing:
                p.pause()
            else:
                p.resume()
        else:           
            self.selected_record = record
            if p.playing_record and not p.playing_record is record:
                p.stop()
        self.update_play_pause()

    def on_prev_button_press(self, widget):
        record = self.selected_record
        if record:
            self.record_carousel.show_record(record)
            p = self.player
            if p.playing_record is record:
                p.play_previous_track()

    def on_next_button_press(self, widget):
        record = self.selected_record
        if record:
            self.record_carousel.show_record(record)
            p = self.player
            if p.playing_record is record:
                p.play_next_track()
            else:
                p.play_record(record)
        self.update_play_pause()

    def on_play_pause_button_press(self, widget):
        record = self.selected_record
        if record:
            self.record_carousel.show_record(record)
            p = self.player
            if not p.playing_record is record:
                p.play_record(record)
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
        self.selected_record = None
        self.init_records()

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

    def end_profiling(self, dt):
        Logger.info('saving profile data after running for {0} seconds'.format(dt))
        self.profile.disable()
        self.profile.dump_stats('/tmp/recordplayer.profile')
