from utils import Popups
from cryptography.fernet import Fernet
import dearpygui.dearpygui as dpg
import pandas as pd

def import_csv(_, __, user_data):
    def get_path(___, app_data):
        path = app_data['file_path_name']
        df = pd.read_csv(path)
        df['password'] = df['password'].apply(lambda x: Fernet(key).encrypt(bytes(x, 'utf-8')).decode())
        df.to_json(app.path_to_encrypted, indent=4, orient='index')
        app.render_contents(rerender=True)

    app = user_data['app']
    key = user_data['key']
    with dpg.file_dialog(callback=get_path, height=500, modal=True, directory_selector=False):
        dpg.add_file_extension(".csv")


def export_csv(_, __, user_data):
    def get_path(___, app_data):
        path = app_data['file_path_name'] + '.csv'
        df['password'] = df['password'].apply(lambda x: Fernet(key).decrypt(bytes(x, 'utf-8')).decode())
        df.to_csv(path, index=False)

    df = user_data['df']
    key = user_data['key']

    with dpg.add_file_dialog(callback=get_path, height=500, modal=True, directory_selector=False):
        dpg.add_file_extension(".csv")


def change_enc_key(_, __, user_data):
    try:
        app = user_data['app']
        key = user_data['key']

        df = app.df
        df['password'] = df['password'].apply(lambda x: Fernet(key).decrypt(bytes(x, 'utf-8')).decode())
        app.key = Fernet.generate_key().decode()
        with open(app.path_to_key, 'w') as file:
            file.write(app.key)
        df['password'] = df['password'].apply(lambda x: Fernet(app.key).encrypt(bytes(x, 'utf-8')).decode())
        df.to_json(app.path_to_encrypted, orient='index', indent=4)
        app.render_contents(rerender=True)

        Popups.PopupOK('The encryption key was successfully changed!')
    except Exception as e:
        Popups.PopupOK(e)


def path_to_enc(_, __, path):
    Popups.PopupOK(f"Path to encrypted file: {path}", wrap=500)


def about():
    Popups.PopupOK("A GUI password manager made by fahlerile in May-June 2023. Uses cryptography's Fernet encryption. GitHub link: https://github.com/fahlerile/password-manager-gui", wrap=500)