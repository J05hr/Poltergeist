from pathlib import Path
from PyQt5 import uic, QtGui, QtWidgets
from Poltergeist.utils import settings_util, dir_util


custom_sounds_window_layout_file = files_util.get_layouts_dir().joinpath('custom_sounds_window.ui')
files_util.dep_check(custom_sounds_window_layout_file)
FormClass, BaseClass = uic.loadUiType(custom_sounds_window_layout_file)


class CustomSoundsWindow(BaseClass, FormClass):
    """Creates a CustomSoundsWindow object for the GUI based on the custom_sounds_window_layout_file."""

    def __init__(self, app):
        super(CustomSoundsWindow, self).__init__()

        # Setup
        self.parent_app = app
        self.setupUi(self)
        icon_filepath = files_util.get_icons_dir().joinpath('mic.png')
        files_util.dep_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))

        # File browsing
        self.mute_browse_dialog = None
        self.unmute_browse_dialog = None
        self.mute_sound_filename = None
        self.unmute_sound_filename = None
        self.mute_browse_button = self.findChild(QtWidgets.QPushButton, 'muteBrowseButton')
        self.mute_browse_button.clicked.connect(self.mute_browse_button_cb)
        self.unmute_browse_button = self.findChild(QtWidgets.QPushButton, 'unmuteBrowseButton')
        self.unmute_browse_button.clicked.connect(self.unmute_browse_button_cb)
        self.mute_filename_text = self.findChild(QtWidgets.QLineEdit, 'muteSoundName')
        self.mute_filename_text.setText(self.parent_app.settings.setting["sound_files"][0]["mute_sound"])
        self.unmute_filename_text = self.findChild(QtWidgets.QLineEdit, 'unmuteSoundName')
        self.unmute_filename_text.setText(self.parent_app.settings.setting["sound_files"][1]["unmute_sound"])

        # Volume controls
        self.volume_level = self.parent_app.settings.setting["sound_volume"] * 100
        self.volume_label = self.findChild(QtWidgets.QLabel, 'volumeLabel')
        self.volume_label.setText(str(self.volume_level))
        self.volume_slider = self.findChild(QtWidgets.QSlider, 'volumeSlider')
        self.volume_slider.setValue(self.volume_level)
        self.volume_slider.valueChanged.connect(self.slider_cb)

    def slider_cb(self):
        """Callback to the volume slider, updates the sound_volume setting on change."""
        self.volume_label.setText(str(self.volume_slider.value()))
        self.volume_level = self.volume_slider.value()
        self.parent_app.settings.setting["sound_volume"] = self.volume_level / 100
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    def mute_browse_button_cb(self):
        """Callback to the mute sound browse button, updates the mute_sound setting on change."""
        self.mute_browse_dialog = QtWidgets.QFileDialog()
        sounds_dir = files_util.get_sounds_dir()
        self.mute_sound_filename = QtWidgets.QFileDialog.getOpenFileName(self.mute_browse_dialog, "", str(sounds_dir))
        if self.mute_sound_filename[0] != "" and Path(self.mute_sound_filename[0]).is_file():
            self.parent_app.settings.setting["sound_files"][0]["mute_sound"] = Path(self.mute_sound_filename[0]).name
            self.mute_filename_text.setText(self.parent_app.settings.setting["sound_files"][0]["mute_sound"])
            settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    def unmute_browse_button_cb(self):
        """Callback to the unmute sound browse button, updates the unmute_sound setting on change."""
        self.unmute_browse_dialog = QtWidgets.QFileDialog()
        sounds_dir = files_util.get_sounds_dir()
        self.unmute_sound_filename = QtWidgets.QFileDialog.getOpenFileName(self.mute_browse_dialog, "", str(sounds_dir))
        if self.unmute_sound_filename[0] != "" and Path(self.unmute_sound_filename[0]).is_file():
            self.parent_app.settings.setting["sound_files"][1]["unmute_sound"] = Path(self.unmute_sound_filename[0]).name
            self.unmute_filename_text.setText(self.parent_app.settings.setting["sound_files"][1]["unmute_sound"])
            settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)
