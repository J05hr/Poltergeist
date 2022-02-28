from pathlib import Path


cwd = Path.cwd()
layouts_dir = cwd.joinpath('layouts')
config_dir = cwd.joinpath('config')
icons_dir = cwd.joinpath('icons')
log_dir = cwd.joinpath('log')


def get_cwd():
    """Return the current working directory if it currently exists."""
    if Path.exists(cwd):
        return cwd
    else:
        raise NotADirectoryError(f"Required directory {cwd} doesn't exist")


def get_layouts_dir():
    """Return the layouts directory if it currently exists."""
    if Path.exists(layouts_dir):
        return layouts_dir
    else:
        raise NotADirectoryError(f"Required directory {layouts_dir} doesn't exist")


def get_config_dir():
    """Return the config directory if it currently exists."""
    if Path.exists(config_dir):
        return config_dir
    else:
        raise NotADirectoryError(f"Required directory {config_dir} doesn't exist")


def get_icons_dir():
    """Return the icons directory if it currently exists."""
    if Path.exists(icons_dir):
        return icons_dir
    else:
        raise NotADirectoryError(f"Required directory {icons_dir} doesn't exist")


def get_log_dir():
    """Return the log directory if it currently exists."""
    if Path.exists(log_dir):
        return log_dir
    else:
        raise NotADirectoryError(f"Required directory {log_dir} doesn't exist")


def dep_check(path):
    """Check that a file dependency exists and return true or false."""
    if Path.exists(path):
        return True
    else:
        raise FileExistsError(f"Required file {path} doesn't exist")
