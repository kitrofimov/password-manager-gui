import pandas as pd
import dearpygui.dearpygui as dpg
from dpg_classes.Window import Window
from dpg_classes import containers, items
from utils import handlers

class App:

    def __init__(self, path_to_encrypted, debug):
        self.path_to_encrypted = path_to_encrypted
        # add encryption
        self.df = pd.read_json(self.path_to_encrypted, orient='index')
        self.num_rows = self.df.shape[0]
        self.num_columns = self.df.shape[1]

        self.window = Window(min_size=[600, 400],
                             max_size=[1000, 600])
        self.window.submit()
        self.window.create_viewport(title='Password Manager v.0.1.0',
                                    size=[1000, 600])
        self.window.set_primary()

        self.render_contents()

        if debug:
            dpg.show_item_registry()


    def render_contents(self):
        self.contents = containers.Group([
            containers.Table([
                *[containers.TableColumn(name) for name in ['Name', 'Password', '']],
                *[
                    containers.TableRow([
                        containers.TableCell([
                            items.Text(self.df.iloc[row_i][self.df.columns[cell_i]]) if cell_i != 2 else \
                            items.Button('X', callback=handlers.delete_button_click, user_data=row_i) # add handler
                        ]) for cell_i in range(self.num_columns+1)
                    ]) for row_i in range(self.num_rows)
                ]
            ], policy=dpg.mvTable_SizingStretchProp),
            containers.Group([
                items.InputText(hint='Name'),
                items.InputText(hint='Password', password=True),
                items.Button(label='Add'),
                items.Button(label='Generate random password')
            ])
        ])
        self.window.add_child(self.contents)
