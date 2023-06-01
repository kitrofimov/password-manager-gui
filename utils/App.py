import pandas as pd
import dearpygui.dearpygui as dpg
from dpg_classes.Window import Window
from dpg_classes import containers, items
from utils import handlers
from cryptography.fernet import Fernet
from utils import menu_bar_handlers
import os
from utils import Popups
import hashlib

class App:

    def __init__(self, title, path, debug=False):
        self.user = os.getlogin()
        self.path = path
        self.path_to_encrypted = path / 'passwords.json'
        self.path_to_key = path / '.key'
        self.path_to_master_pass = path / '.master'

        self.set_master_password = False
        try:
            with open(self.path_to_key, 'r') as file:
                self.key = bytes(file.read(), 'utf-8')
            with open(self.path_to_master_pass, 'r') as file:
                self.master_pass = file.read()
        except FileNotFoundError:
            with open(self.path_to_key, 'w+') as file:
                self.key = Fernet.generate_key().decode()
                file.write(self.key)
            self.set_master_password = True

        self.window = Window(min_size=[600, 400],
                             max_size=[1000, 600])
        self.window.submit()
        self.window.create_viewport(title=title, size=[1000, 600])
        self.window.set_primary()

        self.render_window()

        if debug:
            dpg.show_item_registry()


    def render_window(self, rerender=False):
        try:
            self.df = pd.read_json(self.path_to_encrypted, orient='index')
        except FileNotFoundError:
            self.df = pd.DataFrame([], columns=['name', 'password'])
            self.df.to_json(self.path_to_encrypted, indent=4, orient='index')

        self.num_rows = self.df.shape[0]
        self.num_columns = self.df.shape[1]

        if rerender:
            self.contents.delete()
            self.menubar.delete()

            self.render_contents()
            self.render_menubar()

        elif not self.set_master_password:
            self.render_login_form()

        else:
            self.render_set_master_password()


    def render_set_master_password(self):
        def master_pass_submit(_, __, input_tag):
            with open(self.path_to_master_pass, 'w+') as file:
                file.write(hashlib.sha3_512(dpg.get_value(input_tag).encode('utf-8')).hexdigest())
            popup.delete()
            self.render_contents()
            self.render_menubar()

        popup = Popups.Popup(children=[
                        items.Text(f'Please, set the MASTER PASSWORD for {self.user}.\
                                   NOTE: you should remember it! if you forget it, you cant get your passwords back!', wrap=300),
                        items.InputText(tag='input_master_pass'),
                        items.Button('Submit', callback=master_pass_submit, user_data='input_master_pass')
                    ])


    def render_login_form(self):
        def login_submit(_, __, user_data):
            with open(self.path_to_master_pass, 'w+') as file:
                master_password_hex = file.read()

            pass_correct = hashlib.sha3_512(dpg.get_value('input_master_pass').encode('utf-8')).hexdigest() \
            == master_password_hex

            if pass_correct:
                popup.delete()
                self.render_contents()
                self.render_menubar()
            else:
                Popups.PopupOK('Incorrect password', modal=False)

        popup = Popups.Popup([
            items.InputText(label=f'Master Password for {os.getlogin()}', tag='input_master_pass'),
            items.Button('Log in', callback=login_submit)
        ])


    def render_contents(self):
        AppTable = containers.Table([
            *[containers.TableColumn(name) if name != '' else \
                containers.TableColumn(name, init_width_or_weight=0.05) for name in ['Name', 'Password', '']],
            *[
                containers.TableRow([  # what the hell this is
                    containers.TableCell([
                        items.Text(self.df.iloc[row_i][self.df.columns[cell_i]])
                        if cell_i == 0 else 
                        items.Button('Show', \
                                     callback=handlers.password_click, \
                                     user_data={'index': row_i, 'app': self, 'key': self.key}) \
                        if cell_i == 1 else \
                        items.Button('X', callback=handlers.delete_button_click, user_data={'index': row_i, 'app': self})
                    ]) for cell_i in range(self.num_columns+1)
                ]) for row_i in range(self.num_rows)
            ]
        ])

        AppForm = containers.Group([
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

        self.contents = containers.Group([
            AppTable,
            AppForm
        ])
        self.window.add_child(self.contents)


    def render_menubar(self):
        self.menubar = containers.MenuBar({
            "File": {
                "Import .csv": {
                    "callback": menu_bar_handlers.import_csv,
                    "user_data": {
                        'app': self,
                        'key': self.key
                    }
                },
                "Export .csv": {
                    "callback": menu_bar_handlers.export_csv,
                    "user_data": {
                        'df': self.df,
                        'key': self.key
                    }
                },
                "Path to encrypted file": {
                    "callback": menu_bar_handlers.path_to_enc,
                    "user_data": self.path_to_encrypted
                },

            },
            "Other": {
                "Change encryption key": {
                    "callback": menu_bar_handlers.change_enc_key,
                    "user_data": {
                        'app': self,
                        'key': self.key
                    }
                },
                "About": {
                    "callback": menu_bar_handlers.about
                }
            }
        })

        self.window.add_child(self.menubar)
