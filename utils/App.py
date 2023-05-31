import pandas as pd
import dearpygui.dearpygui as dpg
from dpg_classes.Window import Window
from dpg_classes import containers, items
from utils import handlers

class App:

    def __init__(self, path_to_encrypted, debug):
        self.path_to_encrypted = path_to_encrypted

        self.window = Window(min_size=[600, 400],
                             max_size=[1000, 600])
        self.window.submit()
        self.window.create_viewport(title='Password Manager v.0.1.3',
                                    size=[1000, 600])
        self.window.set_primary()

        self.window.add_child(
            containers.MenuBar({
                "File": {
                    "Import": {
                        "callback": None,
                        "user_data": None
                    },
                    "Export": {
                        "callback": None,
                        "user_data": None
                    },
                    "Path to encrypted file": {
                        "callback": None,
                        "user_data": None
                    }
                }
            })
        )

        self.render_contents()

        if debug:
            dpg.show_item_registry()


    def render_contents(self, rerender=False):
        # add encryption
        self.df = pd.read_json(self.path_to_encrypted, orient='index')

        self.num_rows = self.df.shape[0]
        self.num_columns = self.df.shape[1]

        if rerender:
            self.contents.delete()

        self.contents = containers.Group([
            containers.Table([
                *[containers.TableColumn(name) if name != '' else \
                  containers.TableColumn(name, init_width_or_weight=0.05) for name in ['Name', 'Password', '']],
                *[
                    containers.TableRow([  # what the hell this is
                        containers.TableCell([
                            items.Text(self.df.iloc[row_i][self.df.columns[cell_i]])
                            if cell_i == 0 else 
                            items.Button(self.df.iloc[row_i][self.df.columns[cell_i]], callback=handlers.password_click, \
                                         user_data={'index': row_i, 'app': self}) \
                            if cell_i == 1 else \
                            items.Button('X', callback=handlers.delete_button_click, user_data={'index': row_i, 'app': self})
                        ]) for cell_i in range(self.num_columns+1)
                    ]) for row_i in range(self.num_rows)
                ]
            ]),
            containers.Group([
                items.InputText(hint='Name', tag='name_input'),
                items.InputText(hint='Password', password=True, tag='password_input'),
                items.Button(label='Add', callback=handlers.create_button_click, user_data={
                    'name_input_tag': 'name_input',
                    'password_input_tag': 'password_input',
                    'app': self
                }),
                items.Button(label='Generate random password', callback=handlers.generate_button_click, user_data={
                    'password_input_tag': 'password_input'
                })
            ])
        ])
        self.window.add_child(self.contents)
