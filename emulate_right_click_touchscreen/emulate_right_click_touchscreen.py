#!/usr/bin/env python3
from pynput.keyboard import Key, Controller as KeyController
from pynput.mouse import Listener
from pynput.mouse import Button, Controller
import time
import sys


def _read_vars(path):
  ret = {}
  with open(path, "r") as file:
    line = file.readline()
    while(line):
      line = line.strip()
      if(line != "" and line[0] != "#" and line.find("=") != -1):
        tokens = line.split("=")
        ret[tokens[0]] = "=".join(tokens[1:])
        print(tokens[0])
      line = file.readline()
          
  return ret


threshold_default = 5
timeout_default = 300

last_time = -1
last_pos = [-1, -1]
vars = _read_vars("/home/nulysses/.config/emulate_right_click_touchscreen/vars")
threshold = threshold_default
timeout = timeout_default

mouse_moved = 0


def on_click(x, y, button, pressed):
  global last_time
  global last_pos
  global mouse_moved
  if button == Button.left:
    if pressed is True:
      mouse_moved = 0
      last_pos = [x, y]
      last_time = time.time()
    if pressed is False:
      is_within_threshold = False
      is_within_timeout = True
      if threshold > abs(last_pos[0] - x) \
      and threshold > abs(last_pos[1] - y):
        is_within_threshold = True
      if (time.time() - last_time) * 1000 > timeout:
        is_within_timeout = False
      if is_within_timeout is False \
      and is_within_threshold is True \
      and mouse_moved == 0:
        key = KeyController()
        #key.press(Key.menu)
        #key.release(Key.menu)
        mouse = Controller()
        mouse.press(Button.right)
        mouse.release(Button.right)
      last_pos = [-1, -1]
      last_time = -1


def on_move(x, y):
  global mouse_moved, threshold, last_pos
  if last_pos[0] != -1 and last_pos[1] != -1:
    if abs(last_pos[0] - x) > threshold\
    or abs(last_pos[1] - y) > threshold:
      mouse_moved = 1


def run(_threshold = threshold_default, _timeout = timeout_default):
  global threshold, timeout
  threshold = _threshold
  timeout = _timeout
  with Listener(on_click=on_click, on_move=on_move) as listener:
    listener.join()


if __name__ == "__main__":
  import getpass
  print(getpass.getuser())
  exit(0)
  if len(sys.argv) < 3:
    _threshold = 5
    _timeout = 300
  else:
    _threshold = sys.argv[1]
    _timeout = sys.argv[2]
  run(_threshold, _timeout)
