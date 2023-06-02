import dearpygui.dearpygui as dpg
from App import App

def main():
    app = App('Password Manager v0.2.1', debug=False)


if __name__ == '__main__':
    dpg.create_context()

    main()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
