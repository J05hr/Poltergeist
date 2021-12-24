from pynput import mouse, keyboard
from PyQt5 import uic, QtWidgets, QtGui
from Poltergeist.utils import settings_util, dir_util


ptt_keybinding_window_layout_file = files_util.get_layouts_dir().joinpath('ptt_keybinding_window.ui')
files_util.dep_check(ptt_keybinding_window_layout_file)
FormClass, BaseClass = uic.loadUiType(ptt_keybinding_window_layout_file)


class PttKeyBindingWindow(BaseClass, FormClass):
    """Creates a PttKeyBindingWindow object for the GUI based on the ptt_keybinding_window_layout_file."""

    def __init__(self, app):
        # Setup
        super(PttKeyBindingWindow, self).__init__()
        self.setupUi(self)
        icon_filepath = files_util.get_icons_dir().joinpath('mic.png')
        files_util.dep_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))
        self.keyboard_listener = None
        self.mouse_listener = None
        self.parent_app = app

        # GUI components
        self.ptt_key_input_text = self.findChild(QtWidgets.QLineEdit, 'PttKeybinding')
        self.ptt_key_input_text.setText(self.parent_app.settings.setting["ptt_keybinding"])
        self.ptt_keybinding = None
        self.listen_button = self.findChild(QtWidgets.QPushButton, 'listenButton')
        self.listen_button.clicked.connect(self.listen_button_cb)
        self.save_button = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.save_button.clicked.connect(self.save_button_cb)

    def on_click(self, x, y, button, pressed):
        """Callback for the mouse listener click action, sets the keybinding to the button clicked"""
        self.ptt_key_input_text.setText(str(button))
        self.ptt_keybinding = str(button)
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def on_press(self, key):
        """Callback for the keyboard listener press action, sets the keybinding to the key pressed"""
        key_str = str(key).strip('\'\\')
        self.ptt_key_input_text.setText(key_str)
        self.ptt_keybinding = key_str
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def listen_button_cb(self):
        """Callback for the listen action, starts the listeners for click and press actions."""
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def save_button_cb(self):
        """Callback for the save action, saves the current keybinding to settings"""
        if self.ptt_keybinding:
            self.parent_app.settings.setting["ptt_keybinding"] = self.ptt_keybinding
            settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)
            self.hide()


