import dearpygui.dearpygui as dpg
from dpg_classes import containers, items
import handlers

class Popup:
    def __init__(self, text, label=None):
        self.window = containers.Window(label=label, modal=True, show=False, no_title_bar=True)

        self.popup_text = items.Text(text)
        self.window.add_child(self.popup_text)


class PopupOK(Popup):
    def __init__(self, text, label=None):
        super().__init__(text, label=label)
        self.button_ok = items.Button('OK')
        self.button_ok.set_callback(lambda _: self.window.configure_item(show=False))
        self.window.add_child(self.button_ok)
        self.window.configure_item(show=True)


class PopupChoice(Popup):
    def __init__(self, text, label=None):
        '''
        choices = {
            "choice": {
                "user_data": {},
                "callback": callback
            }
        }
        '''
        super().__init__(text, label=label)

    def render(self, choices):
        for choice, options in choices.items():
            button = items.Button(choice, user_data=options.get('user_data', None))
            button.set_callback(options.get('callback', None))
            self.window.add_child(button)
        self.window.configure_item(show=True)


class PopupSliderInt(Popup):
    def __init__(self, text, label=None, width=0, height=0, default_value=0, callback=None,
                 min_value=0, max_value=100):
        super().__init__(text, label=label)
        self.input = items.SliderInt(width=width, height=height, default_value=default_value, min_value=min_value, max_value=max_value)
        self.button_ok = items.Button('OK')
        self.button_ok.set_callback(callback=callback)
        self.window.add_child(self.input)
        self.window.add_child(self.button_ok)
        self.window.configure_item(show=True)
