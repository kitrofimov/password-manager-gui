import os
from pathlib import Path

import dearpygui.dearpygui as dpg
import pandas as pd
from cryptography.fernet import Fernet

import handlers.form
import handlers.log_in
import handlers.menubar.about
import handlers.menubar.file
import handlers.table


class App:

    def __init__(self, window_title, debug=False):
        self.window_title = window_title
        self.debug = debug

        userpath = Path(os.path.expanduser("~"))
        self.app_path = userpath / ".password_manager"
        if not self.app_path.is_dir():  # if there is no app's directory
            self.app_path.mkdir()
            self.df = pd.DataFrame([], columns=["name", "password"])
            self.df.to_json(self.app_path / "passwords.json", orient="index", indent=4)
            with open(self.app_path / ".key", "w+") as file:
                self.key = Fernet.generate_key().decode()
                file.write(self.key)
            self.ask_master = False  # attribute to set the master password
        else:
            self.df = pd.read_json(self.app_path / "passwords.json", orient="index")
            with open(self.app_path / ".key", "r") as file:
                self.key = file.read()
            self.ask_master = True  # attribute to ask the master password later

        self.window = dpg.add_window(label="Main Window", tag="main_window")
        if self.debug:  # skip the log in if debug
            self.render_contents()
        else:
            self.ask_to_log_in()
        self.init_theme()

        dpg.set_primary_window("main_window", True)
        dpg.create_viewport(
            title=self.window_title,
            width=800,
            height=600,
            max_width=800,
            max_height=600,
            min_width=600,
            min_height=400,
        )

        if self.debug:
            dpg.show_item_registry()
            dpg.show_style_editor()

    def ask_to_log_in(self):
        if self.ask_master:  # log in
            dpg.add_text(
                "Hello! Please, enter your MASTER PASSWORD below.",
                wrap=400,
                parent=self.window,
            )
            input_master = dpg.add_input_text(
                width=390, hint="MASTER PASSWORD", parent=self.window
            )
            dpg.add_button(
                label="Submit",
                callback=handlers.log_in.log_in,
                parent=self.window,
                user_data={"input": input_master, "app": self},
            )

        else:  # set up the master password
            text = dpg.add_text(
                "Hello! Please, set your MASTER PASSWORD below. (?)",
                wrap=400,
                parent=self.window,
            )
            with dpg.tooltip(text):
                dpg.add_text(
                    "This is a password, that you are going to use EVERY TIME you log in in this password manager. If you lose it, you are going to lose all your other passwords!",
                    wrap=300,
                )
            input_master_1 = dpg.add_input_text(
                width=390, hint="MASTER PASSWORD", parent=self.window
            )
            input_master_2 = dpg.add_input_text(
                width=390, hint="repeat MASTER PASSWORD", parent=self.window
            )
            dpg.add_button(
                label="Submit",
                callback=handlers.log_in.set_master_password,
                user_data={"inputs": [input_master_1, input_master_2], "app": self},
                parent=self.window,
            )

    def init_theme(self):  # initialize the window's theme
        with dpg.theme() as self.theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowRounding, 4, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ChildRounding, 4, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_PopupRounding, 4, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_ScrollbarRounding, 4, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_GrabRounding, 4, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_TabRounding, 4, category=dpg.mvThemeCat_Core
                )

                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowTitleAlign,
                    0.5,
                    0.5,
                    category=dpg.mvThemeCat_Core,
                )

        dpg.bind_theme(self.theme)

    def render_contents(self):  # render the main contents of the app
        with dpg.menu_bar(parent=self.window):
            with dpg.menu(label="File"):
                dpg.add_menu_item(
                    label="Import",
                    callback=handlers.menubar.file.import_passwords,
                    user_data={"app": self},
                )
                dpg.add_menu_item(
                    label="Export",
                    callback=handlers.menubar.file.export_passwords,
                    user_data={"app": self},
                )
                dpg.add_menu_item(
                    label="Change encryption key",
                    callback=handlers.menubar.file.change_encryption_key,
                    user_data={"app": self},
                )
            with dpg.menu(label="About"):
                dpg.add_menu_item(label="Help", callback=handlers.menubar.about.help)
                dpg.add_menu_item(
                    label="Path to program's directory",
                    callback=handlers.menubar.about.path,
                    user_data={"app": self},
                )

        self.render_table(rerender=False)

        with dpg.group(parent=self.window, tag="form"):
            input_name = dpg.add_input_text(hint="Name", width=400)
            input_password = dpg.add_input_text(hint="Password", width=400)
            dpg.add_button(
                label="Add",
                callback=handlers.form.add_password,
                user_data={
                    "inputs": {"name": input_name, "password": input_password},
                    "app": self,
                },
            )
            dpg.add_button(
                label="Generate password",
                callback=handlers.form.generate,
                user_data={"input_password": input_password},
            )

    def render_table(self, rerender=True):  # render the table
        if rerender:
            dpg.delete_item(self.table)

        with dpg.table(parent=self.window, before="form") as self.table:
            dpg.add_table_column(label="Name")
            dpg.add_table_column(label="Password")
            dpg.add_table_column(init_width_or_weight=0.05)

            for row_i in range(len(self.df)):
                row = dpg.add_table_row()
                for column_i in range(3):
                    cell = dpg.add_table_cell(parent=row)
                    if column_i == 0:
                        dpg.add_text(
                            self.df.iloc[row_i][self.df.columns[column_i]], parent=cell
                        )
                    elif column_i == 1:
                        dpg.add_button(
                            label="Show",
                            parent=cell,
                            callback=handlers.table.show_password,
                            user_data={"app": self, "row_i": row_i},
                        )
                    else:
                        dpg.add_button(
                            label="X",
                            parent=cell,
                            callback=handlers.table.delete_password,
                            user_data={"app": self, "row_i": row_i},
                        )
