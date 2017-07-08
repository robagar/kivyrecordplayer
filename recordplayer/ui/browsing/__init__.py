from kivy.uix.boxlayout import BoxLayout
from .headerbar import HeaderBar
from .content import RecordBrowser

def create_browsing_ui(listener):
    ui = BoxLayout(orientation='vertical')
    ui.header_bar = HeaderBar(listener)
    ui.add_widget(ui.header_bar);
    ui.record_browser = RecordBrowser(listener)
    ui.record_browser.record_label = ui.header_bar.record_label
    ui.add_widget(ui.record_browser);
    return ui