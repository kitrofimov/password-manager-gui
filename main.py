# https://dearpygui.readthedocs.io/en/latest/
# https://cryptography.io/en/latest/
# https://pypi.org/project/python-dotenv/

import dearpygui.dearpygui as dpg
from window import set_up_ui

if __name__ == '__main__':
    dpg.create_context()

    set_up_ui()

    # dpg.show_item_registry()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()