import dearpygui.dearpygui as dpg

class BaseItem:
    def delete(self):
        dpg.delete_item(self.id)

    def configure_item(self, **kwargs):
        dpg.configure_item(self.id, **kwargs)
