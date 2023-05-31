import dearpygui.dearpygui as dpg
import pandas as pd
from dpg_classes import items, base

class Container(base.BaseItem):
    def add_child(self, child, before=0):
        dpg.move_item(child.id, parent=self.id, before=before)

    def get_children(self):
        return dpg.get_item_children(self.id)


class MenuBar(Container):
    def __init__(self, config=None):
        """
        config: [None|dict]=None - a dictionary in form {
            "menu_name": {
                "menu_item_name": {
                    "callback": None,
                    "user_data": None
                }
            }
        }
        """

        with dpg.stage():
            self.id = dpg.add_menu_bar()

            if config is not None:
                for menu_name, menu_item_options_dict in config.items():
                    menu = Menu(menu_name)
                    for menu_item_name, menu_item_options in menu_item_options_dict.items():
                        menu_item = items.MenuItem(menu_item_name, user_data=menu_item_options.get('user_data'), \
                                                   callback=menu_item_options.get('callback'))
                        menu.add_child(menu_item)
                    self.add_child(menu)


class Menu(Container):
    def __init__(self, label):
        with dpg.stage():
            self.id = dpg.add_menu(label=label)


class TableColumn(Container):
    def __init__(self, label=None, init_width_or_weight=0):
        with dpg.stage():
            self.id = dpg.add_table_column(label=label, init_width_or_weight=init_width_or_weight)


class TableRow(Container):
    def __init__(self, children=None):
        with dpg.stage():
            self.id = dpg.add_table_row()

            if children is not None:
                for child in children:
                    self.add_child(child)


class TableCell(Container):
    def __init__(self, children=None):
        with dpg.stage():
            self.id = dpg.add_table_cell()

            if children is not None:
                for child in children:
                    self.add_child(child)


class Table(Container):
    def __init__(self, children=None, row_background=True,
                 borders_outerH=True, borders_outerV=True,
                 borders_innerH=True, borders_innerV=True,
                 resizable=False, policy=0):

        with dpg.stage():
            self.id = dpg.add_table(row_background=row_background,
                                    borders_outerH=borders_outerH, borders_outerV=borders_outerV,
                                    borders_innerH=borders_innerH, borders_innerV=borders_innerV,
                                    resizable=resizable, policy=policy)
            
            if children is not None:
                for child in children:
                    self.add_child(child)
                

class Group(Container):
    def __init__(self, children: list=None):
        with dpg.stage():
            self.id = dpg.add_group()

            if children is not None:
                for child in children:
                    self.add_child(child)
