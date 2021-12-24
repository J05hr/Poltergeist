import win32api
import win32gui
from PyQt5 import QtGui
from Poltergeist.utils import dir_util
from Poltergeist.core import sound_output_thread


WM_APPCOMMAND = 0x319
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1a * 0x10000
APPCOMMAND_MICROPHONE_VOLUME_DOWN = 0x19 * 0x10000


def mute(app, logger):
    """Performs the mute action by sending the windows commands and starting a sound playback thread."""

    # Set the icon.
    icon_filepath = files_util.get_icons_dir().joinpath('mutemic.png')
    files_util.dep_check(icon_filepath)
    app.tray.setIcon(QtGui.QIcon(str(icon_filepath)))

    # Send the win32 app command.
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

    # Play mute sound if enabled by the settings.
    if app.settings.setting["enable_mute_sound"]:
        mute_sound_path = files_util.get_sounds_dir().joinpath(app.settings.setting["sound_files"][0]["mute_sound"])
        try:
            sound_output_thread.SoundOutputThread(
                mute_sound_path,
                int(app.settings.setting["sound_volume"] * 100), app).start()
        except Exception as s_e:
            logger.error("Error starting mute sound thread, " + str(s_e), exc_info=True)


def unmute(app, logger):
    """Performs the unmute action by sending the windows commands and starting a sound playback thread."""

    # Set the icon.
    icon_filepath = files_util.get_icons_dir().joinpath('unmutemic.png')
    files_util.dep_check(icon_filepath)
    app.tray.setIcon(QtGui.QIcon(str(icon_filepath)))

    # Send the win32 app command.
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)

    # Play unmute sound if enabled by the settings.
    if app.settings.setting["enable_unmute_sound"]:
        unmute_sound_path = files_util.get_sounds_dir().joinpath(app.settings.setting["sound_files"][1]["unmute_sound"])
        try:
            sound_output_thread.SoundOutputThread(
                unmute_sound_path,
                int(app.settings.setting["sound_volume"] * 100), app).start()
        except Exception as s_e:
            logger.error("Error starting unmute sound thread, " + str(s_e), exc_info=True)


def basic_unmute():
    """Performs the basic mute action by sending the windows commands only"""
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)


def basic_mute():
    """Performs the basic unmute action by sending the windows commands only"""
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
