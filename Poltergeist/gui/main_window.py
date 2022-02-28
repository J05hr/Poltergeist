from PyQt5 import uic, QtCore, QtWidgets, QtGui
from Poltergeist.utils import settings_util, autorun_utils, dir_util
from Poltergeist.gui import about_window, log_window


main_window_layout_file = dir_util.get_layouts_dir().joinpath('main_window.ui')
dir_util.dep_check(main_window_layout_file)
FormClass, BaseClass = uic.loadUiType(main_window_layout_file)


class MainWindow(BaseClass, FormClass):
    """Creates a MainWindow object for the GUI based on the main_window_layout_file."""

    def __init__(self, app):
        super(MainWindow, self).__init__()

        # Setup
        self.parent_app = app
        self.setupUi(self)
        icon_filepath = dir_util.get_icons_dir().joinpath('Ghost_Black.png')
        dir_util.dep_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))

        # Windows
        self.about_win = about_window.AboutWindow()
        self.log_win = log_window.LogWindow(self.parent_app)

        # Menu Options
        if self.parent_app.settings.setting['autorun']:
            self.action_auto_run.setChecked(True)
        self.action_auto_run.triggered.connect(self.autorun_action_cb)
        if self.parent_app.settings.setting['start_hidden']:
            self.action_start_hidden.setChecked(True)
        self.action_start_hidden.triggered.connect(self.start_hidden_action_cb)
        if self.parent_app.settings.setting['minimize_to_tray']:
            self.action_minimize_to_tray.setChecked(True)
        self.action_minimize_to_tray.triggered.connect(self.minimize_to_tray_action_cb)
        self.action_info.triggered.connect(self.about_window_action_cb)
        self.action_log.triggered.connect(self.log_window_action_cb)

    def autorun_action_cb(self):
        """Callback for the autorun action, sets the app to autorun on startup."""
        if self.action_auto_run.isChecked():
            self.parent_app.settings.setting['autorun'] = True
            autorun_utils.add_autorun(self.parent_app.logger)
        else:
            self.parent_app.settings.setting['autorun'] = False
            autorun_utils.remove_autorun(self.parent_app.logger)
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    def start_hidden_action_cb(self):
        """Callback for the start hidden action, sets the app to start with the main window hidden."""
        if self.action_start_hidden.isChecked():
            self.parent_app.settings.setting['start_hidden'] = True
        else:
            self.parent_app.settings.setting['start_hidden'] = False
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    def minimize_to_tray_action_cb(self):
        """Callback for the minimize_to_tray action, sets the app to minimize to tray."""
        if self.action_minimize_to_tray.isChecked():
            self.parent_app.settings.setting['minimize_to_tray'] = True
        else:
            self.parent_app.settings.setting['minimize_to_tray'] = False
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    def about_window_action_cb(self):
        """Callback for the Info action, opens the Info/About window for app information."""
        self.about_win.show()

    def log_window_action_cb(self):
        """Callback for the Info action, opens the Info/About window for app information."""
        self.log_win.show()

    def changeEvent(self, event):
        """Override changeEvent() to minimize depending on the 'minimize to tray' setting."""
        if event.type() == QtCore.QEvent.WindowStateChange and self.parent_app.settings.setting['minimize_to_tray']:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.hide()

    def closeEvent(self, close_event):
        """Override closeEvent() to hide the mainWindow instead of quiting the app, you must quit from the tray icon."""
        close_event.ignore()
        self.hide()
