import time
from pynput.mouse import Button, Controller


if __name__ == '__main__':
    mouse = Controller()
    while True:
        time.sleep(299)  # sleep 299 sec
        mouse.move(1, 0)  # Move pointer to keep session alive
        mouse.move(-1, 0)  # Move pointer back to last position
