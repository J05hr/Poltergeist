from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """Creates a SystemTrayIcon object for the GUI, this provides the task bar tray icon and functionality"""

    def __init__(self, icon_filename, app, main_window):
        # Setup
        icon = QtGui.QIcon(str(icon_filename))
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent=None)
        self.parent_app = app
        self.main_window = main_window
        self.setToolTip('Poltergeist v1.0')

        # Menu Options
        self.menu = QtWidgets.QMenu(parent=None)
        self.action_open = QtWidgets.QAction("Open")
        self.action_open.triggered.connect(self.open_action_cb)
        self.action_quit = QtWidgets.QAction("Quit")
        self.action_quit.triggered.connect(self.quit_action_cb)
        self.menu.addAction(self.action_open)
        self.menu.addAction(self.action_quit)
        self.setContextMenu(self.menu)

    def open_action_cb(self):
        """Callback for the Open action, opens the main window."""
        if self.main_window.windowState() == QtCore.Qt.WindowMinimized:
            self.main_window.setWindowState(QtCore.Qt.WindowNoState)  # Window is minimised. Restore it.
        if self.main_window.isHidden():
            self.main_window.show()

    def quit_action_cb(self):
        """Callback for the Quit action, quits the app, closing and exiting."""
        self.parent_app.quit()
