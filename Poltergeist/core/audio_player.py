from ctypes import windll


win_lib = windll.winmm


class PlayerError(Exception):
    """Basic exception for errors raised by Player."""
    pass


class Player:
    """Establishes and controls a sound player in windows.

        Attributes:
            alias: A string to be a reference to the windows player.
            filepath: A string representing the full file path.
            volume: An integer representing the volume level.
    """
    def __init__(self, filepath):
        self.alias = str(id(self))
        self.filepath = filepath
        self.volume = 100
        self.loaded = -1
        self.load_player()

    def __del__(self):
        if self.loaded == 0:  # close on delete if successfully loaded previously
            self.close()

    @staticmethod
    def mci_send_string(command):
        return win_lib.mciSendStringW(command, 0, 0, 0)

    def get_filename(self):
        return self.filepath

    def get_volume(self):
        return self.volume

    def load_player(self):
        """
        Establishes a sound player on windows based on this Players alias and filepath.

        Returns:
            ret(int): A status code from the call to windll.winmm.mciSendStringW().
        """
        ret = self.mci_send_string(f'open "{self.filepath}" type mpegvideo alias {self.alias}')
        self.loaded = ret
        if ret != 0:
            raise PlayerError(f'Failed to load player for {self.filepath}, Error code {ret}')
        return ret

    def set_volume(self, value):
        """
        Sets the volume level of the windows player.

        Parameters:
            value(int): The volume level as an integer.
        """
        value = max(min(value, 100), 0)  # clamp to [0..100]
        self.volume = int(value * 10)  # MCI volume: 0...1000
        ret = self.mci_send_string(f'setaudio {self.alias} volume to {self.volume}')
        if ret != 0:
            raise PlayerError(f'Failed to set_volume for alias "{self.alias}", Error code {ret}')

    def play(self, loop=False, block=False):
        """
        Starts audio playback.

        Parameters:
            loop(bool): Sets whether to repeat the track automatically when finished.
            block(bool): If true, blocks the thread until playback ends.
        """
        sloop = 'repeat' if loop else ''
        swait = 'wait' if block else ''
        ret = self.mci_send_string(f'play {self.alias} from 0 {sloop} {swait}')
        if ret != 0:
            raise PlayerError(f'Failed to play alias "{self.alias}", Error code {ret}')

    def close(self):
        """Closes device, releasing resources. Can't play again."""
        ret = self.mci_send_string(f'close {self.alias}')
        if ret != 0:
            raise PlayerError(f'Failed to close alias "{self.alias}", Error code {ret}')
