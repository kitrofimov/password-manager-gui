import dearpygui.dearpygui as dpg
import pandas as pd
from dpg_classes import items, base

class Container(base.BaseItem):
    def add_child(self, child, before=0):
        dpg.move_item(child.id, parent=self.id, before=before)

    def get_children(self):
        return dpg.get_item_children(self.id)


class Window(Container):
    def __init__(self, label=None, modal=False, show=True, no_title_bar=False,
                 min_size=[100, 100], max_size=[30000, 30000]):
        self._children = []
        with dpg.stage() as stage:
            self.id = dpg.add_window(label=label, modal=modal, show=show, no_title_bar=no_title_bar,
                                     min_size=min_size, max_size=max_size)
        self.stage = stage

    def submit(self):
        dpg.unstage(self.stage)


class MenuBar(Container):
    def __init__(self, config=None):
        """
        config: [None|dict]=None - a dictionary in form {
            "menu_name": {
                "menu_item_name": callback_for_this_menu_item
            }
        }
        """

        with dpg.stage():
            self.id = dpg.add_menu_bar()

            if config is not None:
                for menu_name, menu_item_names_callbacks_dict in config.items():
                    menu = Menu(menu_name)
                    for menu_item_name, menu_item_callback in menu_item_names_callbacks_dict.items():
                        menu_item = items.MenuItem(menu_item_name)
                        if menu_item_callback is not None:
                            menu_item.set_callback(menu_item_callback)
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
    def __init__(self):
        with dpg.stage():
            self.id = dpg.add_table_row()


class TableCell(Container):
    def __init__(self):
        with dpg.stage():
            self.id = dpg.add_table_cell()


class Table(Container):
    def __init__(self, data: pd.DataFrame, row_background=True,
                 borders_outerH=True, borders_outerV=True,
                 borders_innerH=True, borders_innerV=True):
        num_rows = data.shape[0]
        num_columns = data.shape[1]

        with dpg.stage():
            self.id = dpg.add_table(row_background=row_background,
                                    borders_outerH=borders_outerH, borders_outerV=borders_outerV,
                                    borders_innerH=borders_innerH, borders_innerV=borders_innerV)

            for column_i in range(num_columns):
                column = TableColumn(data.columns[column_i])
                self.add_child(column)

            for row_i in range(num_rows):
                row = TableRow()
                for cell_i in range(num_columns):
                    cell = TableCell()
                    text = items.Text(data.iloc[row_i][data.columns[cell_i]])
                    cell.add_child(text)
                    row.add_child(cell)
                self.add_child(row)
                

class Group(Container):
    def __init__(self):
        with dpg.stage():
            self.id = dpg.add_group()
