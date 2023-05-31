import dearpygui.dearpygui as dpg
from dpg_classes import containers, items
from dpg_classes.Window import Window

class Popup(Window):
    def __init__(self, children, label=None):
        super().__init__(label=label, modal=True, no_title_bar=True)
        self.contents = containers.Group(children=children)
        self.add_child(self.contents)


class PopupOK(Popup):
    
    def __init__(self, text, callback=None, user_data=None):
        super().__init__(children=[
            items.Text(text),
            items.Button('OK', callback=callback, user_data=user_data)
        ])


class PopupChoice(Popup):
    
    def __init__(self, text, buttons):
        '''
        buttons = {
            "button_text": {
                "user_data": {},
                "callback": {}
            }
        }
        '''

        super().__init__(children=[
            items.Text(text),
            *[
                items.Button(button_text, callback=options.get('callback'), user_data=options.get('user_data')) for button_text, options in buttons.items()
            ]
        ])
