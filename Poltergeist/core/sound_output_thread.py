import threading
from Poltergeist.core import audio_player


class SoundOutputThread (threading.Thread):
    """Establishes a thread to output notification sounds."""

    def __init__(self, filepath, volume, parent_app):
        threading.Thread.__init__(self)
        self.parent_app = parent_app
        self.filepath = filepath
        self.volume = volume

    def play_sound(self):
        """Creates a new Player object, sets the volume level, and plays the sound for this threads filename."""
        player = audio_player.Player(self.filepath)
        player.set_volume(self.volume)
        player.play(block=True)

    def run(self):
        """Runs the play_sound function once."""
        try:
            self.play_sound()
        except Exception as s_e:
            self.parent_app.logger.error("Error playing sound, " + str(s_e), exc_info=True)

