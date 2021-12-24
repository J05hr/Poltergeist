from pynput import mouse, keyboard
from PyQt5 import uic, QtWidgets, QtGui
from Poltergeist.utils import settings_util, dir_util


toggle_keybinding_window_layout_file = dir_util.get_layouts_dir().joinpath('toggle_keybinding_window.ui')
dir_util.dep_check(toggle_keybinding_window_layout_file)
FormClass, BaseClass = uic.loadUiType(toggle_keybinding_window_layout_file)


class ToggleKeyBindingWindow(BaseClass, FormClass):
    """Creates a ToggleKeyBindingWindow object for the GUI based on the toggle_keybinding_window_layout_file."""

    def __init__(self, app):
        # Setup
        super(ToggleKeyBindingWindow, self).__init__()
        self.setupUi(self)
        icon_filepath = dir_util.get_icons_dir().joinpath('mic.png')
        dir_util.dep_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))
        self.keyboard_listener = None
        self.mouse_listener = None
        self.parent_app = app

        # GUI components
        self.toggle_key_input_text = self.findChild(QtWidgets.QLineEdit, 'ToggleKeybinding')
        self.toggle_key_input_text.setText(self.parent_app.settings.setting["toggle_keybinding"])
        self.toggle_keybinding = None
        self.listen_button = self.findChild(QtWidgets.QPushButton, 'listenButton')
        self.listen_button.clicked.connect(self.listen_button_cb)
        self.save_button = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.save_button.clicked.connect(self.save_button_cb)

    def on_click(self, x, y, button, pressed):
        """Callback for the mouse listener click action, sets the keybinding to the button clicked"""
        self.toggle_key_input_text.setText(str(button))
        self.toggle_keybinding = str(button)
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def on_press(self, key):
        """Callback for the keyboard listener press action, sets the keybinding to the key pressed"""
        key_str = str(key).strip('\'\\')
        self.toggle_key_input_text.setText(key_str)
        self.toggle_keybinding = key_str
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
        if self.toggle_keybinding:
            self.parent_app.settings.setting["toggle_keybinding"] = self.toggle_keybinding
            settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)
            self.hide()
