from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class AlbumIcon(ButtonBehavior, Image):
    def __init__(self, album, **kwargs):
        super().__init__(
            source=album.cover_image_path,
            size_hint=(None, None), 
            size=(95, 95), 
            allow_stretch=True,
            **kwargs
        )
        self.album = album
        album.icon_widget = self
        self.on_unselected()

    def on_selected(self):
        pass

    def on_unselected(self):
        pass       


class AlbumBrowser(ScrollView):
    def __init__(self, listener, **kwargs):
        self._listener = listener 
        super().__init__(**kwargs)

        ac = self.album_container = StackLayout(
            padding=0,
            spacing=5, 
            size_hint_y=None
        )

        ac.bind(minimum_height=ac.setter('height'))
 
        self.add_widget(ac)

    _albums = None
    @property
    def albums(self):
        return self._albums

    @albums.setter
    def albums(self, value):
        self._albums = value
        ac = self.album_container
        ac.clear_widgets()
        if self._albums:
            for a in self._albums:
                self.add_album(a)

    def add_album(self, album):
        w = AlbumIcon(
            album,
            on_press=self.on_album_press
        )
        ac = self.album_container
        ac.add_widget(w)

    # def show_album(self, album):
    #     self.scroll_to(album.icon_widget)

    def on_album_press(self, widget):
        album = widget.album
        # self.show_album(album)
        # self._listener.on_album_press(album)


