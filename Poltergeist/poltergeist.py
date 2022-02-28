import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from Poltergeist.gui import main_window, system_tray
from Poltergeist.utils import settings_util, autorun_utils, dir_util, logging_util


class Poltergeist:
    """Establishes the high level application and encapsulates the GUI application and other components."""
    def __init__(self, logger):
        # Logger
        self.logger = logger

        # Settings
        self.settings = settings_util.read_settings(self.logger)

        # GUI
        self.gui_app = None
        self.style_file = None
        self.win = None
        self.tray = None

        # Threads
        self.threads = None

    def on_exit(self):
        """Kill any existing threads and do any cleanup when the GUI application exits."""
        [thread.stop() for thread in self.threads]

    def run(self):
        """The main run method to start the GUI and execute the program."""
        # Get icon.
        icon_filepath = dir_util.get_icons_dir().joinpath('Ghost_Black.png')
        dir_util.dep_check(icon_filepath)

        # Get the Style
        style_filepath = dir_util.get_layouts_dir().joinpath('styles\\main_style.qss')
        dir_util.dep_check(style_filepath)

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
        settings_util.write_settings(settings_util.default_settings, base_logger)  # Reset the settings to default.
