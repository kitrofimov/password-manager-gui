from utils import Popups

def delete_button_click(_, __, index):
    print(index)
    Popups.PopupChoice('Are you sure you want to delete this password?',
                       {
                           'Yes (delete)': {
                               'user_data': None,
                               'callback': None
                           },
                           'No (keep it)': {
                               'user_data': None,
                               'callback': None
                           },
                       })
