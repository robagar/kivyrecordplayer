from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class RecordWidget(ButtonBehavior, Image):
    def __init__(self, record, **kwargs):
        super().__init__(
            source=record.cover_image_path,
            size_hint=(None, None), 
            size=(350, 350), 
            allow_stretch=True,
            **kwargs
        )
        self.record = record
        record.carousel_widget = self
        self.on_unselected()

    def on_selected(self):
        self.color = [1, 1, 1, 1]

    def on_unselected(self):
        self.color = [1, 1, 1, 0.5]       


class RecordCarousel(ScrollView):
    def __init__(self, listener, **kwargs):
        super().__init__(**kwargs)
        self._listener = listener 

        ac = self.record_container = BoxLayout(
            orientation='horizontal',
            padding=15,
            spacing=30, 
            size_hint_x=None
        )

    #     # TODO uncomment when kivy 1.10 is available
    #     # ac.bind(minimum_width=ac.setter('width'))
 
        self.add_widget(ac)

    _records = None
    @property
    def records(self):
        return self._records

    @records.setter
    def records(self, value):
        self._records = value
        ac = self.record_container
        ac.clear_widgets()
        if self._records:
            for a in self._records:
                self.add_record(a)
        self._update_content_width()

    def add_record(self, record):
        w = RecordWidget(
            record,
            on_press=self.on_record_press
        )
        ac = self.record_container
        ac.add_widget(w)

    def _update_content_width(self):
        # hack pending minimum_width in kivy 1.10
        self.record_container.width = 30 + len(self.records) * 380 

    def show_record(self, record):
        self.scroll_to(record.carousel_widget, padding=225)

    def on_record_press(self, widget):
        record = widget.record
        self.show_record(record)
        self._listener.on_record_press(record)


