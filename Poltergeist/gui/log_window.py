from PyQt5 import uic, QtGui, QtWidgets
from Poltergeist.utils import files_util, logging_util


log_window_layout_file = files_util.get_layouts_dir().joinpath('log_window.ui')
files_util.dep_check(log_window_layout_file)
FormClass, BaseClass = uic.loadUiType(log_window_layout_file)


class LogWindow(BaseClass, FormClass):
    """Creates a LogWindow object for the GUI based on the log_window_layout_file."""

    def __init__(self, app):
        super(LogWindow, self).__init__()

        # Setup
        self.setupUi(self)
        icon_filepath = files_util.get_icons_dir().joinpath('Ghost_Black.png')
        log_filepath = files_util.get_log_dir().joinpath('log.txt')
        files_util.dep_check(icon_filepath)
        files_util.dep_check(log_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))
        self.log_text_Label = self.findChild(QtWidgets.QLabel, 'LogText')

        # Import log text
        log_text = logging_util.read_log(log_filepath, app.logger)
        self.log_text_Label.setText(log_text)
