from pynput.mouse import Listener
from pynput.mouse import Button, Controller
import threading
import time


last_pos = [-1, -1]

button_pressed = False

thread = -1

threshold = 30
timeout = 200


def check_conditions(first_time, first_pos):
  while True:
    time.sleep(0.05)
    global threshold, timeout, button_pressed, last_pos, thread
    is_within_threshold = False
    is_within_timeout = True
    if threshold > abs(last_pos[0] - first_pos[0])\
    or threshold > abs(last_pos[1] - first_pos[1]):
      is_within_threshold = True
    if (time.time() - first_time) * 1000 > timeout:
      is_within_timeout = False
    print(time.time())
    print(first_pos[0])
    print(last_pos[0])
    print(is_within_threshold)
    #print(button_pressed)
    if is_within_timeout is False and is_within_threshold is True:
      print("break1")
      mouse = Controller()
      #mouse.release(Button.left)
      #print("released")
      mouse.press(Button.right)
      mouse.release(Button.right)
      #thread.join()
      thread = -1
      break
    if not button_pressed:
      print("break2")
      #thread.join()
      thread = -1
      break


def on_click(x, y, button, pressed):
  global button_pressed, thread, last_pos
  # If thread is running don't use handler.
  if thread != -1:
    return
  print("onclick")
  if button == Button.left:
    if pressed is True and thread == -1:
      button_pressed = True
      first_pos = [x, y]
      last_pos = first_pos
      first_time = time.time()
      thread = threading.Thread(target=check_conditions,
                                args=[first_time, first_pos])
      thread.start()
    if pressed is False:
      button_pressed = False
      thread = -1


def on_move(x, y):
  global last_pos, button_pressed
  if button_pressed:
    last_pos = [x, y]


def run(_threshold = 30, _timeout = 200):
  global threshold, timeout
  threshold = _threshold
  timeout = _timeout
  with Listener(on_click=on_click) as listener:
    listener.join()


if __name__ == "__main__":
  run()
