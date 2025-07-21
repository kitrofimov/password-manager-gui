import dearpygui.dearpygui as dpg

from App import App

PROGRAM_NAME = "Wordman"
VERSION = "v0.2.2"


def main():
    App(f"{PROGRAM_NAME} {VERSION}", debug=False)


if __name__ == "__main__":
    dpg.create_context()

    main()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
