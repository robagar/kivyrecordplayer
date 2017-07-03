from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

# 93, 7
# 110, 5
# 130, 4
# 156, 5

class AlbumIcon(ButtonBehavior, Image):
    def __init__(self, album, **kwargs):
        super().__init__(
            source=album.cover_image_path,
            size_hint=(None, None), 
            size=(156, 156), 
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

    def dim(self):
        self.color = [1, 1, 1, 0.5]       

    def brighten(self):
        self.color = [1, 1, 1, 1]       


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

    def on_album_press(self, widget):
        album = widget.album
        for a in self.albums:
            if a is album:
                a.icon_widget.brighten()
            else:
                a.icon_widget.dim()
        self.show_album(album)
        self.album_label.text = album.name
        self._listener.on_browse_album_press(album)

    def show_album(self, album):
        self.scroll_to(album.icon_widget, padding=25)

    def reset(self):
        self.album_label.text = ''
        for album in self.albums:
            album.icon_widget.brighten()
        

