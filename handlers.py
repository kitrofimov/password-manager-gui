from dpg_classes import Popup
import pandas as pd
from dpg_classes import items
import secrets
import string

def handle_delete_button_click(sender, app_data, user_data):
    index = user_data['index']
    app = user_data['app']
    popup = Popup.PopupChoice('Are you sure you want to delete this password? This action CANNOT be undone!')
    popup.render({
                    "Yes (delete)": {
                        "user_data": {
                            'delete': True, 
                            'popup_window': popup.window,
                            'index': index,
                            'app': app
                        },
                        "callback": handle_popup_click
                    },
                    "No (keep)": {
                        "user_data": {
                            'delete': False, 
                            'popup_window': popup.window,
                            'index': index,
                            'app': app
                        },
                        "callback": handle_popup_click
                    }
                 })


def handle_popup_click(sender, app_data, user_data):
    user_data['popup_window'].configure_item(show=False)

    if user_data['delete']:
        new_df = user_data['app'].df.drop(user_data['index'], axis=0).reset_index(drop=True)
        new_df.to_json(user_data['app'].path_to_json, orient='index', indent=4)
        app = user_data['app']
        app.render_table(df=new_df, rerender=True)


def submit_new_password(sender, app_data, user_data):
    name = user_data['name_input']
    password = user_data['password_input']
    app = user_data['app']

    if not len(name.get_value()):
        Popup.PopupOK("You can't create a password with empty name")
    elif len(password.get_value()) < 8:
        Popup.PopupOK('Your password should be at least 8 symbols long.')
    else:
        new_df = pd.concat([
            app.df, pd.DataFrame([[name.get_value(), password.get_value()]], columns=['name', 'password'])
        ], axis=0).reset_index(drop=True)
        new_df.to_json(app.path_to_json, orient='index', indent=4)
        name.set_value('')
        password.set_value('')

        app.render_table(df=new_df, rerender=True)


def generate_random_password(sender, app_data, user_data):
    def __generate():
        length = popup.input.get_value()
        password = ''.join(secrets.choice(alphabet) for i in range(length))

        password_input = user_data['password_input']
        password_input.set_value(password)

        popup.window.configure_item(show=False)

    alphabet = string.ascii_letters + string.digits + string.punctuation
    popup = Popup.PopupSliderInt('Length of generated password:', callback=__generate, min_value=8, max_value=32, default_value=8)
