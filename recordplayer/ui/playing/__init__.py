from kivy.uix.boxlayout import BoxLayout
from .headerbar import HeaderBar
from .playbar import PlayBar
from .carousel import RecordCarousel

def create_playing_ui(listener):
    ui = BoxLayout(orientation='vertical')
    ui.header_bar = HeaderBar(listener)
    ui.add_widget(ui.header_bar);
    ui.record_carousel = RecordCarousel(listener)
    ui.add_widget(ui.record_carousel);
    ui.play_bar = PlayBar(listener)
    ui.add_widget(ui.play_bar);
    return ui

