from pathlib import Path
from cryptography.fernet import Fernet
import os
import dearpygui.dearpygui as dpg
import handlers

class App:

    def __init__(self, window_title, debug=False):
        self.window_title = window_title
        self.debug = debug

        userpath = Path(os.path.expanduser('~'))
        self.app_path = userpath / '.password_manager'
        if not self.app_path.is_dir():  # if there is no app's directory
            self.app_path.mkdir()
            (self.app_path / 'passwords.json').touch()
            with open(self.app_path / '.key', 'w+') as file:
                self.key = Fernet.generate_key().decode()
                file.write(self.key)
            self.ask_master = False  # attribute to set the master password
        else:
            self.ask_master = True  # attribute to ask the master password later
        self.logged_in = False

        self.window = dpg.add_window(label='Main Window', tag='main_window')
        self.render_contents()

        dpg.set_primary_window('main_window', True)
        dpg.create_viewport(title=self.window_title, width=800, height=600)
        
        if self.debug:
            dpg.show_item_registry()


    def render_contents(self):
        if not self.logged_in:  # if not logged in
            if self.ask_master:  # log in     # SuperGoydaVAC
                dpg.add_text('Hello! Please, enter your MASTER PASSWORD below.',
                              wrap=400, parent=self.window)
                input_master = dpg.add_input_text(width=390, hint='MASTER PASSWORD', parent=self.window)
                dpg.add_button(label='Submit', callback=handlers.log_in, parent=self.window, user_data={
                    'input': input_master,
                    'app': self
                })

            else:  # set up the master password
                dpg.add_text('Hello! Please, set your MASTER PASSWORD below. If you lose it, you are going to lose all your other passwords!',
                              wrap=400, parent=self.window)
                input_master_1 = dpg.add_input_text(width=390, hint='MASTER PASSWORD', parent=self.window)
                input_master_2 = dpg.add_input_text(width=390, hint='repeat MASTER PASSWORD', parent=self.window)
                dpg.add_button(label='Submit', callback=handlers.set_master_password, user_data={
                    'inputs': [input_master_1, input_master_2],
                    'app': self
                }, parent=self.window)

        else:  # if logged in
            dpg.add_text('You logged in! VAC!!!', parent=self.window)

