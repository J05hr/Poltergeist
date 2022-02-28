

class Settings:
    """Establishes an object representing the application settings."""

    def __init__(self, autorun, start_hidden, minimize_to_tray, routines):

        self.setting = {
            "autorun": autorun,   # autorun at startup, boolean
            "start_hidden": start_hidden,  # start in minimized, boolean
            "minimize_to_tray": minimize_to_tray,   # minimize to tray, boolean
            "routines": routines,  # routine configurations
        }