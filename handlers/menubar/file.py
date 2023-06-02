import dearpygui.dearpygui as dpg
from cryptography.fernet import Fernet
import pandas as pd

def import_passwords(sender, app_data, user_data):  # import a .csv file with passwords, encrypt it and store
    app = user_data['app']

    def file_dialog():
        def selected_a_file(sender, app_data, user_data):
            selected_file_path = app_data['file_path_name']
            app.df = pd.read_csv(selected_file_path, index_col=False)
            print(app.df)
            app.df['password'] = app.df['password'].apply(lambda x: Fernet(app.key).encrypt(bytes(str(x), encoding='utf-8')).decode())
            app.df.to_json(app.app_path / 'passwords.json', orient='index', indent=4)
            app.render_table()

        with dpg.file_dialog(directory_selector=False, callback=selected_a_file, cancel_callback=None, width=600, height=400):
            dpg.add_file_extension(".csv")

    with dpg.window(modal=True, no_title_bar=True) as popup:
        dpg.add_text("NOTE: your existing passwords will be removed! (another note: in your .csv file there should be two columns: name and password (lowercase and specifically password after name column))", wrap=500)
        dpg.add_button(label='OK', callback=lambda x: (
            dpg.delete_item(popup),
            file_dialog()
        ))
        dpg.add_button(label='Exit', callback=lambda x: dpg.delete_item(popup))


def export_passwords(sender, app_data, user_data):  # export a decrypted .json file with passwords as .csv
    app = user_data['app']

    def selected_a_file(sender, app_data, user_data):
        selected_file_path = app_data['file_path_name']
        df = app.df
        df['password'] = df['password'].apply(lambda x: Fernet(app.key).decrypt(str(x)).decode())
        df.to_csv(selected_file_path, index=False)

    with dpg.file_dialog(directory_selector=False, callback=selected_a_file, cancel_callback=None, width=600, height=400):
        dpg.add_file_extension(".csv")


def change_encryption_key(sender, app_data, user_data):  # re-encrypt everything with new key
    app = user_data['app']

    def change_encryption_key_():
        old_key = app.key
        with open(app.app_path / '.key', 'w') as file:
            new_key = Fernet.generate_key().decode()
            file.write(new_key)
        app.key = new_key

        app.df['password'] = app.df['password'].apply(lambda x: Fernet(old_key).decrypt(str(x)).decode())  # decrypt with old key
        app.df['password'] = app.df['password'].apply(lambda x: Fernet(new_key).encrypt(bytes(str(x), encoding='utf-8')).decode())  # encrypt with new one

        app.df.to_json(app.app_path / 'passwords.json', orient='index', indent=4)
        app.render_table()

    with dpg.window(modal=True, no_title_bar=True) as popup:
        dpg.add_text("Are you sure?")
        dpg.add_button(label='Yes', callback=lambda: (
            dpg.delete_item(popup),
            change_encryption_key_()
        ))
        dpg.add_button(label='No, exit', callback=lambda: dpg.delete_item(popup))
