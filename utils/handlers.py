from utils import Popups
import dearpygui.dearpygui as dpg
import pandas as pd
import secrets
from dpg_classes import items
from xkcdpass import xkcd_password as xp
import pyperclip
from cryptography.fernet import Fernet

def delete_button_click(_, __, user_data):

    def handle_popup_click(_, __, user_data):
        delete = user_data['delete']
        index = user_data['index']
        app = user_data['app']

        dpg.delete_item('delete_or_no_popup')

        if delete:
            new_df = app.df.drop(index).reset_index(drop=True)
            new_df.to_json(app.path_to_encrypted, orient='index', indent=4)
            app.render_window(rerender=True)

    Popups.PopupChoice('Are you sure you want to delete this password?', tag='delete_or_no_popup',
                       buttons={
                           'Yes (delete)': {
                               'user_data': {
                                   'delete': True,
                                   **user_data
                               },
                               'callback': handle_popup_click
                           },
                           'No (keep it)': {
                               'user_data': {
                                   'delete': False,
                                   **user_data
                               },
                               'callback': handle_popup_click
                           },
                       })


def create_button_click(_, __, user_data):
    name_input_tag = user_data['name_input_tag']
    password_input_tag = user_data['password_input_tag']
    app = user_data['app']

    name, password = dpg.get_value(name_input_tag), dpg.get_value(password_input_tag)

    if not len(name):
        Popups.PopupOK("You can't create a password without specifying a name.")
    elif len(password) < 8:
        Popups.PopupOK("Your password should be at least 8 symbols long.")
    else:
        new_df = pd.concat([
            app.df,
            pd.DataFrame([[name, Fernet(app.key).encrypt(bytes(password, 'utf-8')).decode()]],
                        columns=['name', 'password'])
        ], axis=0).reset_index(drop=True)
        new_df.to_json(app.path_to_encrypted, orient='index', indent=4)
        app.render_window(rerender=True)

        dpg.set_value(name_input_tag, '')
        dpg.set_value(password_input_tag, '')


def generate_button_click(_, __, user_data):
    password_input_tag = user_data['password_input_tag']

    def password():
        def generate():
            slider_id = dpg.get_item_children(popup.get_children()[1][0])[1][1]
            n_symbols = dpg.get_value(slider_id)
            popup.delete()
            dpg.set_value(password_input_tag, secrets.token_urlsafe(round(n_symbols/1.375)))

        popup.update_contents([
            items.Text('Number of symbols:'),
            items.SliderInt(default_value=16,
                            min_value=8, max_value=32),
            items.Button('Submit', callback=generate)
        ], width=150)
    
    def passphrase():
        popup.delete()

        wordfile = xp.locate_wordfile()
        mywords = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)
        dpg.set_value(password_input_tag, xp.generate_xkcdpassword(mywords, acrostic="face", delimiter='_'))

    popup = Popups.PopupChoice('', {
        "Password": {
            "user_data": None,
            "callback": password
        },
        "Passphrase": {
            "user_data": None,
            "callback": passphrase
        }
    }, modal=True)


def password_click(button, __, user_data):
    index = user_data['index']
    app = user_data['app']
    key = user_data['key']

    def hide_password(OKbutton):
        dpg.set_item_label(button, 'Show')
        dpg.delete_item(dpg.get_item_parent(dpg.get_item_parent(OKbutton)))


    dpg.set_item_label(button, Fernet(key).decrypt(bytes(app.df.iloc[index]['password'], 'utf-8')).decode())

    pyperclip.copy(Fernet(key).decrypt(bytes(app.df.iloc[index]['password'], 'utf-8')).decode())
    popup = Popups.PopupOK('The password was copied to clipboard!', modal=False, callback=hide_password)
