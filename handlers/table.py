import dearpygui.dearpygui as dpg
import pyperclip
from cryptography.fernet import Fernet


def show_password(sender, app_data, user_data):
    row_i = user_data["row_i"]
    app = user_data["app"]

    dpg.hide_item(sender)  # hide the 'Show' button
    cell = dpg.get_item_parent(sender)
    temp_text_value = (
        Fernet(app.key)
        .decrypt(bytes(app.df.iloc[row_i]["password"], "utf-8"))  # decrypting password
        .decode()
    )
    temp_text = dpg.add_text(temp_text_value, parent=cell)  # adding temporary text
    pyperclip.copy(temp_text_value)
    with dpg.window(no_title_bar=True) as popup:
        dpg.add_text("The password copied to clipboard!")
        dpg.add_button(
            label="OK",
            callback=lambda x: (
                dpg.delete_item(popup),  # delete popup on click
                dpg.delete_item(temp_text),  # delete temporary text
                dpg.show_item(sender),  # show the 'Show' button again
            ),
        )


def delete_password(sender, app_data, user_data):
    def __delete_password():
        app.df = app.df.drop(row_i, axis=0).reset_index(drop=True)
        app.df.to_json(app.app_path / "passwords.json", orient="index", indent=4)
        dpg.delete_item(popup)
        app.render_table()

    row_i = user_data["row_i"]
    app = user_data["app"]

    with dpg.window(popup=True) as popup:
        dpg.add_text("Are you sure you want to delete this password?")
        dpg.add_button(label="Yes (delete)", callback=__delete_password)
        dpg.add_button(label="No (keep)", callback=lambda x: dpg.delete_item(popup))
