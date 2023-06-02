import dearpygui.dearpygui as dpg
from App import App

def main():
    app = App('Password Manager v0.2.0', debug=True)


if __name__ == '__main__':
    dpg.create_context()

    main()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
