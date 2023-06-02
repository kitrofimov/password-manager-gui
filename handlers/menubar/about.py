import dearpygui.dearpygui as dpg

def help(sender, app_data, user_data):  # help
    with dpg.window(popup=True, modal=True, no_title_bar=True) as popup:
        dpg.add_text("Password manager written in Python and Dear PyGUI as a practice project by fahlerile in late May-June 2023. Although it has all the basic features, I wouldn't personally use it, because I am not an expert in cryptography, and, as I said, this was planned just as practice project for my Dear PyGUI skills. GitHub: https://github.com/fahlerile/password-manager-gui.", wrap=500)
        dpg.add_button(label='OK', callback=lambda x: dpg.delete_item(popup))

def path(sender, app_data, user_data):  # path to programs directory
    app = user_data['app']

    with dpg.window(popup=True, modal=True, no_title_bar=True) as popup:
        dpg.add_text(f"The path to program's directory: {app.app_path}", wrap=500)
        dpg.add_button(label='OK', callback=lambda x: dpg.delete_item(popup))
