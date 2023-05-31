from dpg_classes import containers

class AppMenuBar(containers.MenuBar):

    def __init__(self):
        super().__init__({
            "File": {
                "Import": {
                    "callback": None,
                    "user_data": None
                },
                "Export": {
                    "callback": None,
                    "user_data": None
                },
                "Path to encrypted file": {
                    "callback": None,
                    "user_data": None
                }
            }
        })
        