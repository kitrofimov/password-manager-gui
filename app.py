import dearpygui.dearpygui as dpg
import pandas as pd
from dpg_classes import containers, items
import handlers

class App:
    
    def __init__(self, path_to_json, debug=False):
        self.path_to_json = path_to_json
        self.df = pd.read_json(self.path_to_json, orient='index')

        self.window = containers.Window(label='main')
        self.window.submit()

        self.menubar = containers.MenuBar({
            'File': {
                'Import': None,
                'Export': None
            }
        })
        self.window.add_child(self.menubar)

        self.input_group = containers.Group()
        self.name_input = items.InputText(hint='Name')
        self.password_input = items.InputText(hint='Password', password=True)
        self.submit_button = items.Button(label='Add', user_data={
            "name_input": self.name_input,
            "password_input": self.password_input,
            'app': self
        })
        self.generate_button = items.Button(label='Generate random password', user_data={
            'password_input': self.password_input
        })

        self.submit_button.set_callback(handlers.submit_new_password)
        self.generate_button.set_callback(handlers.generate_random_password)

        self.input_group.add_child(self.name_input)
        self.input_group.add_child(self.password_input)
        self.input_group.add_child(self.submit_button)
        self.input_group.add_child(self.generate_button)

        self.window.add_child(self.input_group)

        self.render_table()

        dpg.create_viewport(title='Password Manager v.0.1.0', width=600, height=400,
                            min_width=600, max_width=1000,
                            min_height=400, max_height=600)
        dpg.set_primary_window(self.window.id, True)

        if debug:
            dpg.show_item_registry()


    def render_table(self, df=None, rerender=False):
        if df is not None:
            self.df = df
        else:
            self.df = pd.read_json(self.path_to_json, orient='index')

        if rerender:
            self.table.delete()

        self.table = containers.Table(self.df)
        table_column_for_buttons = containers.TableColumn(init_width_or_weight=0.06)
        self.table.add_child(table_column_for_buttons)

        for index, row_id in enumerate(self.table.get_children()[1]):
            cell = containers.TableCell()
            button = items.Button('X', user_data={
                "index": index,
                "app": self,
                "df": self.df,
                "path_to_json": self.path_to_json
            })
            button.set_callback(handlers.handle_delete_button_click)
            cell.add_child(button)
            dpg.move_item(item=cell.id, parent=row_id)

        self.window.add_child(self.table, before=self.input_group.id)
