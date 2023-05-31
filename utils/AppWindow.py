from dpg_classes.Window import Window
from utils.AppMenuBar import AppMenuBar
from dpg_classes import containers, items

class AppWindow(Window):

    def __init__(self, title, size=[800, 600], min_size=[100, 100], max_size=[30000, 30000]):
        super().__init__(min_size=min_size,
                         max_size=max_size)
        self.submit()
        self.create_viewport(title=title, size=size)
        self.set_primary()

        self.add_child(AppMenuBar())
