from kivy.uix.boxlayout import BoxLayout
# from .headerbar import HeaderBar
from .content import AlbumBrowser

def create_browsing_ui(listener):
    ui = BoxLayout(orientation='vertical')
    # ui.header_bar = HeaderBar(listener)
    # ui.add_widget(ui.header_bar);
    ui.album_browser = AlbumBrowser(listener)
    ui.add_widget(ui.album_browser);
    return ui