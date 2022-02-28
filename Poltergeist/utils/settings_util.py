import json
from Poltergeist.core import settings
from Poltergeist.utils import dir_util


config_dir = dir_util.get_config_dir()
config_filename = dir_util.get_config_dir().joinpath('poltergeist_config.json')
dir_util.dep_check(config_filename)


"""defaults: (don't autorun, don't start hidden, minimize to tray, default routines) """

default_settings = settings.Settings(False, False, True,
                                     [{"id": 0, "name": "default", "enabled": False, "schedules": None},
                                         {"id": 1, "name": "keep_alive", "enabled": False, "schedules": None}])


def read_settings(logger):
    """Try to read the last settings or fallback to defaults."""
    try:
        with open(config_filename, "r") as config_file:
            current_settings = json.load(config_file)

        autorun = current_settings["autorun"]
        start_hidden = current_settings["start_hidden"]
        minimize_to_tray = current_settings["minimize_to_tray"]
        routines = current_settings["routines"]

        return settings.Settings(autorun, start_hidden, minimize_to_tray, routines)

    except Exception as e:
        logger.error("Error reading settings, " + str(e), exc_info=True)
        write_settings(default_settings, logger)  # fallback to defaults, overwrite the corrupted config
        return default_settings


def write_settings(new_settings, logger):
    """Try to write the settings to the poltergeist_config.json or fallback and write defaults."""
    try:
        with open(config_filename, "w") as config_file:
            json_settings = {
                "autorun": new_settings.setting["autorun"],
                "start_hidden": new_settings.setting["start_hidden"],
                "minimize_to_tray": new_settings.setting["minimize_to_tray"],
                "routines": new_settings.setting["routines"]
            }
            json.dump(json_settings, config_file)

    except Exception as e:
        logger.error("Error writing settings, " + str(e), exc_info=True)
        with open(config_filename, "w") as config_file:  # fallback to defaults
            json.dump(default_settings, config_file)
