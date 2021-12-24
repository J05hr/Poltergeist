import sys
from PyQt5.QtCore import QFile, QTextStream
from pynput import mouse, keyboard
from PyQt5.QtWidgets import QApplication
from Poltergeist.core import mic_controls, mute_sanity_thread, mic_input_read_thread
from Poltergeist.gui import main_window, system_tray
from Poltergeist.utils import settings_util, autorun_utils, dir_util, logging_util


class Poltergeist:
    """Establishes the high level application and encapsulates the GUI application and other components."""

    def __init__(self, logger):
        # Logger
        self.logger = logger

        # Settings
        self.settings = settings_util.read_settings(self.logger)

        # States
        self.mode = self.settings.setting['mode']
        self.ptt_key_pushed = False
        self.input_level = None
        self.toggle_state = 'unmuted'

        # GUI
        self.gui_app = None
        self.style_file = None
        self.win = None
        self.tray = None

        # Threads
        self.mute_sanity_thread = mute_sanity_thread.MuteSanityThread(self)
        self.mic_input_read_thread = mic_input_read_thread.MicInputReadThread(self)
        self.m_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.k_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)

    def on_exit(self):
        """Kill any existing threads and do any cleanup when the GUI application exits."""
        self.mute_sanity_thread.stop()
        self.mic_input_read_thread.stop()
        self.m_listener.stop()
        self.k_listener.stop()
        mic_controls.basic_unmute()  # Ensure unmute on exit.

    def on_mouse_click(self, x, y, button, pressed):
        """Callback for the mouse listener click action."""
        if self.mode == 'ptt':
            if pressed:
                # Unmute if the keybinding is pressed.
                if str(button) == self.settings.setting['ptt_keybinding']:
                    self.ptt_key_pushed = True
                    mic_controls.unmute(self, self.logger)
            else:
                # Mute if the keybinding is released.
                if str(button) == self.settings.setting['ptt_keybinding']:
                    self.ptt_key_pushed = False
                    mic_controls.mute(self, self.logger)
        elif self.mode == 'toggle':
            if pressed:
                if str(button) == self.settings.setting['toggle_keybinding']:
                    # Toggle the mute.
                    if self.toggle_state == 'unmuted':
                        mic_controls.mute(self, self.logger)
                        self.toggle_state = 'muted'
                    else:
                        mic_controls.unmute(self, self.logger)
                        self.toggle_state = 'unmuted'

    def on_key_press(self, key):
        """Callback for the keyboard listener press action."""
        if self.mode == 'ptt':
            # Unmute if the keybinding is pressed.
            if str(key).strip('\'\\') == self.settings.setting['ptt_keybinding']:
                if not self.ptt_key_pushed:
                    self.ptt_key_pushed = True
                    mic_controls.unmute(self, self.logger)
        elif self.mode == 'toggle':
            if str(key).strip('\'\\') == self.settings.setting['toggle_keybinding']:
                # Toggle the mute.
                if self.toggle_state == 'unmuted':
                    mic_controls.mute(self, self.logger)
                    self.toggle_state = 'muted'
                else:
                    mic_controls.unmute(self, self.logger)
                    self.toggle_state = 'unmuted'

    def on_key_release(self, key):
        """Callback for the keyboard listener release action."""
        if self.mode == 'ptt':
            # Mute if the keybinding is released.
            if str(key).strip('\'\\') == self.settings.setting['ptt_keybinding']:
                mic_controls.mute(self, self.logger)
                self.ptt_key_pushed = False

    def run(self):
        """The main run method to start the GUI and execute the program."""

        # Get icon.
        icon_filepath = files_util.get_icons_dir().joinpath('mutemic.png')
        files_util.dep_check(icon_filepath)

        # Get the Style
        style_filepath = files_util.get_layouts_dir().joinpath('styles\\main_style.qss')
        files_util.dep_check(style_filepath)

        # Run the GUI.
        self.gui_app = QApplication(sys.argv)
        self.style_file = QFile(str(style_filepath))
        self.style_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(self.style_file)
        self.gui_app.setStyleSheet(stream.readAll())
        self.gui_app.aboutToQuit.connect(self.on_exit)
        self.win = main_window.MainWindow(self)
        self.tray = system_tray.SystemTrayIcon(icon_filepath, self.gui_app, self.win)
        self.tray.show()
        if not self.settings.setting["start_hidden"]:
            self.win.show()

        # Add autostart to windows if autorun setting is true.
        autorun = self.settings.setting['autorun']
        if autorun:
            autorun_utils.add_autorun(self.logger)
        else:
            autorun_utils.remove_autorun(self.logger)

        # Listen for mouse and keyboard inputs.
        self.m_listener.start()
        self.k_listener.start()

        # Start the sanity check thread and the input reader thread.
        self.mic_input_read_thread.start()
        self.mute_sanity_thread.start()

        # Start muted if ptt mode or un-muted if toggle mode.
        if self.mode == 'ptt':
            mic_controls.mute(self, self.logger)
        elif self.mode == 'toggle':
            mic_controls.unmute(self, self.logger)

        sys.exit(self.gui_app.exec())


if __name__ == '__main__':
    """Instantiates and runs the high level application for Poltergeist v1.0."""

    base_logger = logging_util.new_logger()

    try:
        Poltergeist = Poltergeist(base_logger)
        Poltergeist.run()

    except Exception as e:
        print(e)
        base_logger.error("Fatal Error, " + str(e), exc_info=True)
        mic_controls.basic_unmute()  # Ensure the mic is left in an un-muted state.
        settings_util.write_settings(settings_util.default_settings, base_logger)  # Reset the settings to default.
