

class Settings:
    """Establishes an object representing the application settings."""

    def __init__(self, mode, toggle_keybinding, ptt_keybinding, autorun, start_hidden, minimize_to_tray,
                 enable_mute_sound, enable_unmute_sound, sound_files, sound_volume):

        self.setting = {
            "mode": mode,  # the current application mode, toggle or ppt
            "toggle_keybinding": toggle_keybinding,  # current toggle keybinding, stores key code
            "ptt_keybinding": ptt_keybinding,  # current ptt keybinding, stores key string
            "autorun": autorun,   # autorun at startup, boolean
            "start_hidden": start_hidden,  # start in minimized, boolean
            "minimize_to_tray": minimize_to_tray,   # minimize to tray, boolean
            "enable_mute_sound": enable_mute_sound,  # play mute sound, boolean
            "enable_unmute_sound": enable_unmute_sound,  # play unmute sound, boolean
            "sound_files": sound_files,  # sound file locations for notifications, tuple of filenames (mute, unmute)
            "sound_volume": sound_volume  # sound volume setting for mute and unmute sounds
        }
