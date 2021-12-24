import threading
import sounddevice as sd
import numpy as np


class MicInputReadThread (threading.Thread):
    """Establishes a thread to read the input level of the mic."""

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.parent_app = app
        self.kill = False

    def get_sound_level(self, indata, o, f, t, s):
        """Reads the sound level and updates the input_level of the parent application."""
        volume_norm = np.linalg.norm(indata) * 10
        self.parent_app.input_level = int(volume_norm)

    def run(self):
        """Runs the get_sound_level function on a 1 second loop."""
        with sd.Stream(callback=self.get_sound_level):
            while not self.kill:
                sd.sleep(1)

    def stop(self):
        self.kill = True
