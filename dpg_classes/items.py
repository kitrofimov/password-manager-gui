import dearpygui.dearpygui as dpg

class Item:
    def set_callback(self, callback):
        dpg.set_item_callback(self.id, callback)


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