import dearpygui.dearpygui as dpg
from dpg_classes import containers, base

class Item(base.BaseItem):
    def set_callback(self, callback):
        dpg.set_item_callback(self.id, callback)

    def get_value(self):
        return dpg.get_value(self.id)

    def set_value(self, value):
        dpg.set_value(self.id, value)


class Button(Item):
    def __init__(self, label, user_data=None):
        with dpg.stage():
            self.id = dpg.add_button(label=label, user_data=user_data)


class MenuItem(Item):
    def __init__(self, label):
        with dpg.stage():
            self.id = dpg.add_menu_item(label=label)


class Text(Item):
    def __init__(self, text):
        with dpg.stage():
            self.id = dpg.add_text(text)


class InputText(Item):
    def __init__(self, width=0, height=0, hint=None, password=False):
        with dpg.stage():
            self.id = dpg.add_input_text(width=width, height=height,
                                         password=password, hint=hint)


class SliderInt(Item):
    def __init__(self, width=0, height=0, default_value=0, min_value=0, max_value=100):
        with dpg.stage():
            self.id = dpg.add_slider_int(width=width, height=height, default_value=default_value, min_value=min_value, max_value=max_value)
