import dearpygui.dearpygui as dpg
from dpg_classes import containers, items
import pandas as pd

def set_up_ui():
    window = containers.Window('main')
    window.submit()

    menubar = containers.MenuBar({
        'File': {
            'Import': None,
            'Export': None
        }
    })
    window.add_child(menubar)

    data = pd.read_json('./passwords.json')
    table = containers.Table(data)
    table_column_for_buttons = containers.TableColumn()
    table.add_child(table_column_for_buttons)
    for index, row_id in enumerate(table.get_children()[1]):
        cell = containers.TableCell()
        button = items.Button('X', user_data=index)
        button.set_callback(lambda sender, app_data, user_data: print('button was clicked!', sender, app_data, user_data))
        cell.add_child(button)
        dpg.move_item(item=cell.id, parent=row_id)
    window.add_child(table)

    dpg.create_viewport(title='Password Manager v.1.0.0', width=600, height=400)
    dpg.set_primary_window(window.id, True)
