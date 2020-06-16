#!/usr/bin/python3

from pynput.mouse import Listener
from pynput.mouse import Button, Controller
import time

last_time = -1
last_pos = [-1, -1]

threshold = 15
timeout = 300


def on_click(x, y, button, pressed):
  global last_time
  global last_pos
  if button == Button.left:
    if pressed is True:
      last_pos = [x, y]
      last_time = time.time()
    if pressed is False:
      is_within_threshold = False
      is_within_timeout = True
      if threshold > abs(last_pos[0] - x) and threshold > abs(last_pos[1] - y):
        is_within_threshold = True
      if (time.time() - last_time) * 1000 > timeout:
        is_within_timeout = False
      if is_within_timeout is False and is_within_threshold is True:
        mouse = Controller()
        mouse.press(Button.right)
        mouse.release(Button.right)
      last_pos = [-1, -1]
      last_time = -1


def run(_threshold = 30, _timeout = 200):
  global threshold, timeout
  threshold = _threshold
  timeout = _timeout
  with Listener(on_click=on_click) as listener:
    listener.join()


if __name__ == "__main__":
  run()
