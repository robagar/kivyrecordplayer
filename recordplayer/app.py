from cProfile import Profile

from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from . import settings
from .device import create_device
from .backend import create_backend, BackendListener
from .record import load_records
from .shutdown import shutdown, reboot
from .ui.browsing import create_browsing_ui
from .ui.playing import create_playing_ui
from .ui.system import create_system_popup


class RecordPlayerApp(BackendListener, App):

    INITIALIZING = 'initializing'
    PLAYING = 'playing'
    BROWSING = 'browsing'
         
    def build(self):
        sm = self.screen_manager = ScreenManager(transition=NoTransition())

        # initial loading screen
        s = Screen(name=self.INITIALIZING)
        s.add_widget(Label(text='loading...'))
        sm.add_widget(s)

        # browsing
        ui = self.browsing_ui = create_browsing_ui(self)
        s = self.browsing_screen = Screen(name=self.BROWSING)
        s.add_widget(ui)
        self.record_browser = ui.record_browser
        sm.add_widget(s)
 
        # playing
        ui = self.playing_ui = create_playing_ui(self)
        s = self.playing_screen = Screen(name=self.PLAYING)
        s.add_widget(ui)
        self.record_carousel = ui.record_carousel
        self.record_label = ui.header_bar.record_label
        self.play_pause_button = ui.header_bar.play_pause_button
        self.playing_label = ui.play_bar.playing_label 
        sm.add_widget(s)

        return sm

    def on_start(self):
        Logger.info('START')

        # self.profile = Profile()
        # self.profile.enable()
        # Clock.schedule_once(self.end_profiling, 3*60)

        self.device = create_device(settings.DEVICE)
        self.backend = create_backend(settings.BACKEND, self)
        Clock.schedule_interval(lambda dt: self.backend.update(), 1)

        self.root_window.bind(on_touch_down=self.on_window_touch_down)

        # load records after displaying "loading..." 
        self.screen_manager.current = self.INITIALIZING
        Clock.schedule_once(lambda dt: Clock.schedule_once(lambda dt: self.init_records(), 0), 0)
        
        self.device.brighten_screen()

    def init_records(self):
        Logger.info('initializing records...')
        self.records \
            = self.record_carousel.records \
            = self.record_browser.records \
            = load_records(settings.MUSIC_PATH)
        self.show_browsing_ui()
 
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
        self.selected_record = self.backend.playing_record or self.selected_record
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
            self.backend.play_record(record)
            self.show_playing_ui()
        elif not self.selected_record:
            self.selected_record = record
        else:
            self.selected_record = None
        self.update_play_pause()
        return self.selected_record

    def on_record_press(self, record):
        b = self.backend
        if self.selected_record is record:
            if not b.playing_record is record:
                b.play_record(record)
            elif b.playing:
                b.pause()
            else:
                b.resume()
        else:           
            self.selected_record = record
            if b.playing_record and not b.playing_record is record:
                b.stop()
        self.update_play_pause()

    def on_prev_button_press(self, widget):
        record = self.selected_record
        if record:
            self.record_carousel.show_record(record)
            b = self.backend
            if b.playing_record is record:
                b.play_previous_track()

    def on_next_button_press(self, widget):
        record = self.selected_record
        if record:
            self.record_carousel.show_record(record)
            b = self.backend
            if b.playing_record is record:
                b.play_next_track()
            else:
                b.play_record(record)
        self.update_play_pause()

    def on_play_pause_button_press(self, widget):
        record = self.selected_record
        if record:
            self.record_carousel.show_record(record)
            b = self.backend
            if not b.playing_record is record:
                b.play_record(record)
            elif b.playing:
                b.pause()
            else:
                b.resume() 
        self.update_play_pause()

    def on_rescan_press(self, widget):
        Logger.info('RESCAN')
        self._system_popup.dismiss()
        b = self.backend
        b.stop()
        b.rescan()
        self.selected_record = None
        self.init_records()

    def on_sleep_press(self, widget):
        Logger.info('SLEEP')
        self._system_popup.dismiss()
        self.device.screen_off()
        self.backend.stop()
        self.selected_record = None

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

    def on_backend_state_change(self, old_state, new_state):
        Logger.info('{0}: {1} -> {2}'.format(self.backend.name, old_state, new_state))
        if self.backend.stopped:
            self.device.dim_screen()

    def on_backend_playing_track(self, playing_track_name):
        Logger.info('{0}: playing track {1}'.format(self.backend.name, playing_track_name))    
        ptn = playing_track_name
        self.playing_label.text = ptn if ptn else ''

    _system_popup = None
    def on_system_button_press(self, widget):
        if not self._system_popup:
            self._system_popup = create_system_popup(self)
        self._system_popup.open()

    def update_play_pause(self):
        b = self.play_pause_button
        b.set_icon('pause' if self.backend.playing else 'play')

    def on_window_touch_down(self, *args, **kwargs):
        # Logger.info('window touch')
        self.device.touch()

    # def end_profiling(self, dt):
    #     Logger.info('saving profile data after running for {0} seconds'.format(dt))
    #     self.profile.disable()
    #     self.profile.dump_stats('/tmp/recordbackend.profile')
