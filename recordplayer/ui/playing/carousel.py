from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class AlbumWidget(ButtonBehavior, Image):
    def __init__(self, album, **kwargs):
        super().__init__(
            source=album.cover_image_path,
            size_hint=(None, None), 
            size=(350, 350), 
            allow_stretch=True,
            **kwargs
        )
        self.album = album
        album.carousel_widget = self
        self.on_unselected()

    def on_selected(self):
        self.color = [1, 1, 1, 1]

    def on_unselected(self):
        self.color = [1, 1, 1, 0.5]       


class AlbumCarousel(ScrollView):
    def __init__(self, listener, **kwargs):
        super().__init__(**kwargs)
        self._listener = listener 

        ac = self.album_container = BoxLayout(
            orientation='horizontal',
            padding=15,
            spacing=30, 
            size_hint_x=None
        )

    #     # TODO uncomment when kivy 1.10 is available
    #     # ac.bind(minimum_width=ac.setter('width'))
 
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
        self._update_content_width()

    def add_album(self, album):
        w = AlbumWidget(
            album,
            on_press=self.on_album_press
        )
        ac = self.album_container
        ac.add_widget(w)

    def _update_content_width(self):
        # hack pending minimum_width in kivy 1.10
        self.album_container.width = 30 + len(self.albums) * 380 

    def show_album(self, album):
        self.scroll_to(album.carousel_widget, padding=225)

    def on_album_press(self, widget):
        album = widget.album
        self.show_album(album)
        self._listener.on_album_press(album)


