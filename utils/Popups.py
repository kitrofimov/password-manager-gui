import dearpygui.dearpygui as dpg
from dpg_classes import containers, items
from dpg_classes.Window import Window

class Popup(Window):
    def __init__(self, children, label=None, tag=0, modal=True):
        super().__init__(label=label, modal=modal, no_title_bar=True, tag=tag, show=True)
        self.__render(children=children)

    def update_contents(self, children: list, height=0, width=0):
        dpg.configure_item(self.id, width=width, height=height)
        self.contents.delete()
        self.__render(children=children)

    def __render(self, children):
        self.contents = containers.Group(children=children)
        self.add_child(self.contents)


class PopupOK(Popup):

    def __init__(self, text, user_data=None, tag=0, modal=True, callback=None, wrap=-1):
        super().__init__(children=[
            items.Text(text, wrap=wrap),
            items.Button('OK', callback=callback, user_data=user_data) \
            if callback is not None else \
            items.Button('OK', callback=(lambda _: self.delete()), user_data=user_data)
        ], tag=tag, modal=modal)


class PopupChoice(Popup):
    
    def __init__(self, text, buttons, tag=0, modal=True):
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
        ], tag=tag, modal=modal)


class PopupSliderInt(Popup):

    def __init__(self, text, button_text, callback=None, user_data=None, default_value=0, min_value=0, max_value=100, tag=0, modal=True):
        super().__init__(children=[
            items.Text(text),
            items.SliderInt(default_value=default_value,
                            min_value=min_value, max_value=max_value),
            items.Button(button_text, callback=callback, user_data=user_data)
        ], tag=tag, modal=modal)
