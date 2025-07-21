import secrets

import dearpygui.dearpygui as dpg
import pandas as pd
from cryptography.fernet import Fernet
from xkcdpass import xkcd_password as xp


def add_password(sender, app_data, user_data):  # add new password
    input_name, input_password = (
        user_data["inputs"]["name"],
        user_data["inputs"]["password"],
    )
    app = user_data["app"]

    input_name_value, input_password_value = dpg.get_value(input_name), dpg.get_value(
        input_password
    )

    if not len(input_name_value):  # if there is nothing in "name" field
        with dpg.window(popup=True) as popup:
            dpg.add_text("You cannot create a password without specifying a name.")
            dpg.add_button(label="OK", callback=lambda x: dpg.delete_item(popup))
    elif len(input_password_value) < 8:  # if password is less than 8 symbols long
        with dpg.window(popup=True) as popup:
            dpg.add_text("Your password should be at least 8 symbols long.")
            dpg.add_button(label="OK", callback=lambda x: dpg.delete_item(popup))
    else:  # if everything is okay
        [dpg.set_value(field, "") for field in [input_name, input_password]]
        app.df = pd.concat(
            [
                app.df,
                pd.DataFrame(
                    [
                        [
                            input_name_value,
                            Fernet(app.key)
                            .encrypt(bytes(input_password_value, "utf-8"))
                            .decode(),
                        ]
                    ],
                    columns=["name", "password"],
                ),
            ],
            axis=0,
        ).reset_index(drop=True)
        app.df.to_json(app.app_path / "passwords.json", orient="index", indent=4)
        app.render_table()


def generate(sender, app_data, user_data):  # generate password
    input_password = user_data["input_password"]

    def generate_password():  # code to execute if user wants to generate a password
        [
            dpg.delete_item(item) for item in dpg.get_item_children(popup)[1]
        ]  # delete everything from popup
        dpg.add_text("Number of symbols:", parent=popup)
        slider = dpg.add_slider_int(
            min_value=8, default_value=16, max_value=32, parent=popup
        )
        dpg.add_button(
            label="Generate",
            parent=popup,
            callback=lambda x: dpg.set_value(
                input_password,
                secrets.token_urlsafe(  # generating password
                    round(dpg.get_value(slider) / 1.375)
                ),
            ),
        )

    def generate_passphrase():  # code to execute if user wants to generate a passphrase

        def generate():  # generate a passphrase
            wordfile = xp.locate_wordfile()
            mywords = xp.generate_wordlist(
                wordfile=wordfile, min_length=5, max_length=8
            )
            dpg.set_value(
                input_password,
                xp.generate_xkcdpassword(
                    mywords, acrostic="face", delimiter=dpg.get_value(separator_input)
                ),
            )

        [
            dpg.delete_item(item) for item in dpg.get_item_children(popup)[1]
        ]  # delete everything from popup
        dpg.add_text("Separator:", parent=popup)
        separator_input = dpg.add_input_text(parent=popup)
        dpg.add_button(label="Generate", parent=popup, callback=generate)

    with dpg.window(
        popup=True
    ) as popup:  # ask user to choice what type of password to generate
        dpg.add_button(label="Password", callback=generate_password)
        dpg.add_button(label="Passphrase", callback=generate_passphrase)
