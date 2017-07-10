from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

# 93, 7
# 110, 5
# 130, 4
# 156, 5

class RecordIcon(ButtonBehavior, Image):
    def __init__(self, record, **kwargs):
        super().__init__(
            source=record.cover_image_path,
            size_hint=(None, None), 
            size=(156, 156), 
            allow_stretch=True,
            **kwargs
        )
        self.record = record
        record.icon_widget = self
        self.on_unselected()

    def on_selected(self):
        pass

    def on_unselected(self):
        pass

    def dim(self):
        self.color = [1, 1, 1, 0.5]       

    def brighten(self):
        self.color = [1, 1, 1, 1]       


class RecordBrowser(ScrollView):
    def __init__(self, listener, **kwargs):
        self._listener = listener 
        super().__init__(**kwargs)

        ac = self.record_container = StackLayout(
            padding=0,
            spacing=5, 
            size_hint_y=None
        )

        ac.bind(minimum_height=ac.setter('height'))
 
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

    def add_record(self, record):
        w = RecordIcon(
            record,
            on_press=self.on_record_press
        )
        ac = self.record_container
        ac.add_widget(w)

    def on_record_press(self, widget):
        record = self._listener.on_browse_record_press(widget.record)
        if record:
            self.highlight_record(record)
            self.record_label.text = record.name
        else:
            self.reset()

    def highlight_record(self, record):
        for a in self.records:
            if a is record:
                a.icon_widget.brighten()
            else:
                a.icon_widget.dim()
        self.show_record(record)

    def show_record(self, record):
        self.scroll_to(record.icon_widget, padding=25)

    def reset(self):
        self.record_label.text = ''
        for record in self.records:
            record.icon_widget.brighten()
        

