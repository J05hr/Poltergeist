import json
from Poltergeist.core import settings
from Poltergeist.utils import dir_util


config_dir = dir_util.get_config_dir()
config_filename = dir_util.get_config_dir().joinpath('poltergeist_config.json')
dir_util.dep_check(config_filename)


"""defaults: (ptt mode, y key, t key, don't autorun, don't start hidden, minimize to tray,
              enable mute sound, enable unmute sound, default sounds, 50% volume) """

default_settings = settings.Settings('ptt', 'y', 't', False, False, True, True, True,
                                     [{"mute_sound": 'beep300.wav'},
                                         {"unmute_sound": 'beep750.wav'}], 0.5)


def read_settings(logger):
    """Try to read the last settings or fallback to defaults."""
    try:
        with open(config_filename, "r") as config_file:
            current_settings = json.load(config_file)

        mode = current_settings["mode"]
        toggle_keybinding = current_settings["toggle_keybinding"]
        ptt_keybinding = current_settings["ptt_keybinding"]
        autorun = current_settings["autorun"]
        start_hidden = current_settings["start_hidden"]
        minimize_to_tray = current_settings["minimize_to_tray"]
        enable_mute_sound = current_settings["enable_mute_sound"]
        enable_unmute_sound = current_settings["enable_unmute_sound"]
        sound_files = current_settings["sound_files"]
        # update sounds to default if None
        if current_settings["sound_files"][0]["mute_sound"] is None:
            current_settings["sound_files"][0]["mute_sound"] = 'beep300.wav'
            write_settings(current_settings, logger)
        if current_settings["sound_files"][1]["unmute_sound"] is None:
            current_settings["sound_files"][1]["unmute_sound"] = 'beep750.wav'
            write_settings(current_settings, logger)
        sound_volume = current_settings["sound_volume"]

        return settings.Settings(mode, toggle_keybinding, ptt_keybinding, autorun, start_hidden, minimize_to_tray,
                                 enable_mute_sound, enable_unmute_sound, sound_files, sound_volume)

    except Exception as e:
        logger.error("Error reading settings, " + str(e), exc_info=True)
        write_settings(default_settings, logger)  # fallback to defaults, overwrite the corrupted config
        return default_settings


def write_settings(new_settings, logger):
    """Try to write the settings to the poltergeist_config.json or fallback and write defaults."""
    try:
        with open(config_filename, "w") as config_file:
            json_settings = {
                "mode": new_settings.setting["mode"],
                "toggle_keybinding": new_settings.setting["toggle_keybinding"],
                "ptt_keybinding": new_settings.setting["ptt_keybinding"],
                "autorun": new_settings.setting["autorun"],
                "start_hidden": new_settings.setting["start_hidden"],
                "minimize_to_tray": new_settings.setting["minimize_to_tray"],
                "enable_mute_sound": new_settings.setting["enable_mute_sound"],
                "enable_unmute_sound": new_settings.setting["enable_unmute_sound"],
                "sound_files": new_settings.setting["sound_files"],
                "sound_volume": new_settings.setting["sound_volume"]
            }
            json.dump(json_settings, config_file)

    except Exception as e:
        logger.error("Error writing settings, " + str(e), exc_info=True)
        with open(config_filename, "w") as config_file:  # fallback to defaults
            json.dump(default_settings, config_file)
