import dearpygui.dearpygui as dpg
from dpg_classes import containers, base

class Item(base.BaseItem):
    def __init__(self, callback=None):
        dpg.set_item_callback(self.id, callback=callback)

    def get_value(self):
        return dpg.get_value(self.id)

    def set_value(self, value):
        dpg.set_value(self.id, value)


class Button(Item):
    def __init__(self, label, callback=None, user_data=None):
        with dpg.stage():
            self.id = dpg.add_button(label=label, user_data=user_data)
            super().__init__(callback=callback)


class MenuItem(Item):
    def __init__(self, label, callback=None, user_data=None):
        with dpg.stage():
            self.id = dpg.add_menu_item(label=label, user_data=user_data)
            super().__init__(callback=callback)


class Text(Item):
    def __init__(self, text, tag=0):
        with dpg.stage():
            self.id = dpg.add_text(text, tag=tag)


class InputText(Item):
    def __init__(self, callback=None, width=0, height=0, hint=None, password=False, tag=0):
        with dpg.stage():
            self.id = dpg.add_input_text(width=width, height=height,
                                         password=password, hint=hint, tag=tag)
            super().__init__(callback=callback)


class SliderInt(Item):
    def __init__(self, callback=None, width=0, height=0, default_value=0, min_value=0, max_value=100):
        with dpg.stage():
            self.id = dpg.add_slider_int(width=width, height=height, default_value=default_value, min_value=min_value, max_value=max_value)
            super().__init__(callback=callback)
