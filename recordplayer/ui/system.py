from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup


def create_system_popup(listener):
    c = BoxLayout(
        orientation='vertical',
        padding=10,
        spacing=10
    )
    c.add_widget(Button(
        text='shutdown',
        on_press=listener.on_shutdown_press
    ))
    c.add_widget(Button(
        text='reboot',
        on_press=listener.on_reboot_press
    ))
    return Popup(
        title='Record Player',
        size_hint=(0.5, 0.5),
        content=c
    )
