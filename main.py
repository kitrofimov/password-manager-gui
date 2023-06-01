# https://dearpygui.readthedocs.io/en/latest/
# https://cryptography.io/en/latest/
# https://pypi.org/project/python-dotenv/

import dearpygui.dearpygui as dpg
from utils.App import App

import os
from pathlib import Path

def main():
    userpath = Path(os.path.expanduser('~'))
    apppath = userpath / 'password_manager'
    apppath.mkdir(parents=False, exist_ok=True)
    app = App('Password Manager v.0.1.3', apppath, debug=True)


if __name__ == '__main__':
    dpg.create_context()

    main()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
