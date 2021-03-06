import os
import random
import yaml
from kivy.logger import Logger


def load_records(root_dir_path):
    Logger.info('loading records...')
    sticky_records = []
    nonsticky_records = []
    for d in os.listdir(root_dir_path):
        if d[0] == '.':
            continue

        p = os.path.join(root_dir_path, d)
        if is_valid_record_dir(p):
            # Logger.info(d)
            r = Record(p)
            l = sticky_records if r.sticky else nonsticky_records 
            l.append(r)

    # sticky records sorted by name
    sticky_records.sort(key=lambda r: r.name)

    # rest random (but consistent)
    random.seed(1)
    random.shuffle(nonsticky_records)

    return sticky_records + nonsticky_records

def is_valid_record_dir(dir_path):
    p = dir_path
    if not os.path.isdir(p):
        return False

    return True


class Record(object):
    MUSIC_EXTENSIONS = ['mp3', 'flac', 'ogg', 'wma']
    IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']
    DEFAULT_COVER_IMAGE_PATH = None

    def __init__(self, dir_path):
        self._dir_path = dir_path
        self._widgets = set()

        self._name = os.path.basename(self._dir_path)

        try:
            with open(os.path.join(self._dir_path, 'record.yaml'), 'r') as f:
                ps = yaml.safe_load(f)
        except:
            ps = {}
            
        self._url = ps.get('url', self._name)
        self._sticky = bool(ps.get('sticky', False))

        self._scan_files()
        # Logger.info(str(self._cover_image_file))

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def sticky(self):
        return self._sticky

    @property
    def widgets(self):
        return self._widgets

    _carousel_widget = None
    @property
    def carousel_widget(self):
        return self._carousel_widget

    @carousel_widget.setter
    def carousel_widget(self, widget):
        self._carousel_widget = widget
        self._widgets.add(widget)

    _icon_widget = None
    @property
    def icon_widget(self):
        return self._icon_widget

    @icon_widget.setter
    def icon_widget(self, widget):
        self._icon_widget = widget
        self._widgets.add(widget)

    @property
    def cover_image_path(self):
        if self._cover_image_file:
            return os.path.join(self._dir_path, self._cover_image_file)
        else:
            return self.DEFAULT_COVER_IMAGE_PATH

    @property
    def track_files(self):
        return self._track_files

    def _scan_files(self):
        self._cover_image_file = None
        self._track_files = []

        for f in os.listdir(self._dir_path):
            if f[0] == '.':
                continue

            p = os.path.join(self._dir_path, f)
            if not os.path.isfile(p):
                continue

            _, ext = os.path.splitext(f)
            if not ext:
                continue

            ext = ext[1:].lower()

            if ext in self.MUSIC_EXTENSIONS:
                self._track_files.append(os.path.join(self._dir_path, f))
            elif ext in self.IMAGE_EXTENSIONS:
                if not self._cover_image_file:
                    self._cover_image_file = f

        self._track_files.sort()

    def on_selected(self):
        for w in self.widgets:
            w.on_selected()

    def on_unselected(self):
        for w in self.widgets:
            w.on_unselected()

