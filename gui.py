import tkinter as tk
import time
import threading
import logging

import pyscreeze as psc
import win32api
import win32con
import pygetwindow as pgw

import os

champ_dir = 'champions/'
champs = [x.rstrip('.png') for x in os.listdir(champ_dir)]

stop_picking = False


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        # logging
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(
            format=format, level=logging.INFO, datefmt="%H:%M:%S")

        self.title("Aram Reroll Picker")
        self.geometry("200x400+10+10")

        fields = ["First", "Second", "Third"]
        labels = [tk.Label(self, text=f) for f in fields]
        vars = [tk.StringVar(self) for _ in fields]
        print(vars)
        optMenus = [tk.OptionMenu(self, var, *champs) for var in vars]
        self.widgets = list(zip(labels, optMenus))
        self.run = tk.Button(self, text="Run Picker",
                             command=self.start)
        self.stop = tk.Button(self, text="Stop", command=self.stop)

        for i, (label, optMenu) in enumerate(self.widgets):
            label.grid(row=i, column=0, padx=10, sticky=tk.W)
            optMenu.grid(row=i, column=1, padx=10, pady=5)
        self.run.grid(row=len(fields), column=1, sticky=tk.E, padx=10, pady=10)
        self.stop.grid(row=len(fields)+1, column=1,
                       sticky=tk.E, padx=10, pady=10)

    def start(self):
        global stop_picking
        stop_picking = False
        logging.info("Main: starting Thread")
        self.picker = threading.Thread(target=self.picker_runner)
        self.picker.start()
        logging.info("Main: Thread started")

    def stop(self):
        global stop_picking
        stop_picking = True
        self.picker.join()

    def picker_runner(self):
        global stop_picking
        logging.info(f"Thread: starting")
        win = pgw.getWindowsWithTitle('League')[0]
        win = precise_hey(win)
        while True:
            try:
                for champ in champs:
                    val = psc.locateOnScreen(os.path.join(
                        champ_dir, champ+".png"), region=win, confidence=0.8, grayscale=True)
                    logging.info(f"{champ}: {val} #DEBUG: {win}")
                    click(val.left + val.width/2, val.top + val.height/2)
                time.sleep(0.1)
            except psc.PyScreezeException:
                logging.error("Thread: League of Legends is not running.")
            if stop_picking:
                break
        logging.info(f"Thread: stopping")


def precise_hey(win):
    # production aram return
    return (win.left+200, win.top+20, win.width-200, win.height-600)
    # debug return for training matches:
    # return (win.left, win.top, win.width-1300, win.height-200)


def click(x, y):
    win32api.SetCursorPos(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
