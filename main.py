# https://dearpygui.readthedocs.io/en/latest/
# https://cryptography.io/en/latest/
# https://pypi.org/project/python-dotenv/

import dearpygui.dearpygui as dpg
from utils.App import App

if __name__ == '__main__':
    dpg.create_context()

    app = App('./passwords.json', debug=True)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
