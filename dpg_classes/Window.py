import dearpygui.dearpygui as dpg
from dpg_classes.containers import Container

class Window(Container):
    def __init__(self, label=None, modal=False, show=True, no_title_bar=False,
                 min_size=[100, 100], max_size=[30000, 30000]):
        self.min_size = min_size
        self.max_size = max_size
        with dpg.stage() as stage:
            self.id = dpg.add_window(label=label, modal=modal, show=show, no_title_bar=no_title_bar,
                                     min_size=min_size, max_size=max_size)
        self.stage = stage

    def submit(self):
        dpg.unstage(self.stage)

    def create_viewport(self, title, size):
        dpg.create_viewport(title=title,
                            width=size[0], height=size[1],
                            min_width=self.min_size[0], max_width=self.max_size[0],
                            min_height=self.min_size[1], max_height=self.max_size[1])

    def set_primary(self):
        dpg.set_primary_window(self.id, True)
