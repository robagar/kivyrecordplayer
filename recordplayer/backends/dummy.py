from ..backend import Backend


class DummyBackend(Backend):
    def __init__(self, listener):
        super().__init__('dummy backend', listener)
        
    def on_play_record(self):
        pass 