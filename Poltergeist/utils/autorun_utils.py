from pathlib import Path
from win32com import client
from win32comext.shell import shell, shellcon
from Poltergeist.utils import dir_util


app_data = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0)


def add_autorun(logger):
    """Attempt to add a shortcut for the exe to the startup folder so it will autorun on startup."""
    try:
        target = files_util.get_cwd().joinpath('Poltergeist.exe')
        path = Path(app_data + '/Microsoft/Windows/Start Menu/Programs/Startup/Poltergeist.exe.lnk')
        shll = client.Dispatch('WScript.Shell')
        shortcut = shll.CreateShortCut(str(path))
        shortcut.TargetPath = str(target)
        shortcut.WorkingDirectory = str(files_util.get_cwd())
        shortcut.Save()
    except Exception as e:
        logger.error("Failed to add startup item, " + str(e), exc_info=True)


def remove_autorun(logger):
    """Attempt to remove the shortcut from the startup folder so it will not autorun on startup."""
    try:
        rpath = Path(app_data + '/Microsoft/Windows/Start Menu/Programs/Startup/Poltergeist.exe.lnk')
        rpath.unlink(missing_ok=True)
    except Exception as e:
        logger.error("Failed to delete startup item, " + str(e), exc_info=True)
