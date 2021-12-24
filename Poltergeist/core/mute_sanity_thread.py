import time
import threading
from Poltergeist.core import mic_controls


class MuteSanityThread (threading.Thread):
    """Establishes a thread to check and fix the mic state ensuring the mic is always in the state expected."""

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.parent_app = app
        self.kill = False

    def mute_sanity_check_fix(self):
        """Fixes the mic state by muting or un-muting the mic to gain the applications expected state."""
        mode = self.parent_app.settings.setting['mode']
        if mode == 'ptt':
            # as long as the button is not pushed ensure the mic is muted in_case of external changes
            if not self.parent_app.ptt_key_pushed and self.parent_app.input_level > 0:
                mic_controls.basic_mute()
        elif mode == 'toggle':
            if self.parent_app.toggle_state == 'muted' and self.parent_app.input_level > 0:
                mic_controls.basic_mute()
            elif self.parent_app.toggle_state == 'unmuted' and self.parent_app.input_level == 0:
                mic_controls.basic_unmute()

    def run(self):
        """Runs the mute_sanity_check_fix function on a 1 second loop."""
        while not self.kill:
            time.sleep(1)
            self.mute_sanity_check_fix()

    def stop(self):
        self.kill = True
