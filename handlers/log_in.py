import dearpygui.dearpygui as dpg
import hashlib

def __delete_all_contents_and_render(app):
    [dpg.delete_item(item) for item in dpg.get_item_children(app.window)[1]]
    app.render_contents()


def set_master_password(sender, app_data, user_data):  # called as callback for first-time user to set his master password
    values = [dpg.get_value(input_) for input_ in user_data['inputs']]
    app = user_data['app']

    if len(values[0]) < 8:  # if the password is too small
        with dpg.window(popup=True) as popup:
            dpg.add_text('The MASTER PASSWORD cannot be less than 8 symbols!', wrap=270)
            dpg.add_button(label='OK', callback=lambda x: dpg.delete_item(popup))

    elif values[0] != values[1]:  # if two passwords mismatch
        with dpg.window(popup=True) as popup:
            dpg.add_text('Sorry, the passwords do not match!', wrap=270)
            dpg.add_button(label='OK', callback=lambda x: dpg.delete_item(popup))

    else:
        # hash the password and store it in apppath/.master, then render all contents as needed
        with open(app.app_path / '.master', 'w+') as file:
            file.write(hashlib.md5(values[0].encode()).hexdigest())

        app.logged_in = True
        __delete_all_contents_and_render(app)


def log_in(sender, app_data, user_data):  # called as a callback when user tries to log-in
    input_bar = user_data['input']
    app = user_data['app']

    with open(app.app_path / '.master', 'r') as file:
        hash = file.read()

    if hashlib.md5(dpg.get_value(input_bar).encode()).hexdigest() == hash:
        app.logged_in = True
        __delete_all_contents_and_render(app)
    
    else:
        with dpg.window(popup=True):
            dpg.add_text('Incorrect password')
            dpg.add_button(label='OK', callback=lambda x: dpg.delete_item(dpg.get_item_parent(x)))
