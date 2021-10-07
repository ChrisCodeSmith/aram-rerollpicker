import tkinter as tk
import time
import threading
import logging

import pyscreeze as psc
import win32api
import win32con
import pygetwindow as pgw

import os

# relative on lolcli with res 1600x900:
# win reroll region: (x+420, y, width+840, height-820)
# selected champs: (x+20,y+120,width-1300,height-400)

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
        self.run.grid(row=len(fields), column=1, sticky=tk.W, pady=10)
        self.stop.grid(row=len(fields), column=2,
                       sticky=tk.W, pady=10)

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
        win_rr = rel_reroll(win)
        win_rs = rel_selected(win)
        while True:
            try:
                for champ in champs:
                    rr = psc.locateOnScreen(os.path.join(
                        champ_dir, champ+".png"), region=win_rr, confidence=0.8, grayscale=True)
                    rs = psc.locateOnScreen(os.path.join(
                        champ_dir, champ+".png"), region=win_rs, confidence=0.8, grayscale=True)
                    logging.info(
                        f"{champ}: #DEBUG: Reroll:{win_rr}:{rr}, Selected:{win_rs}:{rs}")
                    if rr != None and rs == None:
                        click(rr.left + rr.width/2, rr.top + rr.height/2)
                time.sleep(0.1)
            except psc.PyScreezeException:
                logging.error("Thread: League of Legends is not running.")
            if stop_picking:
                break
        logging.info(f"Thread: stopping")


def rel_reroll(win):
    # production aram return
    return (win.left+420, win.top, win.width-840, win.height-820)
    # debug return for training matches:
    # return (win.left, win.top, win.width-1300, win.height-200)


def rel_selected(win):
    return (win.left+20, win.top+120, win.width-1300, win.height-400)


def click(x, y):
    win32api.SetCursorPos(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
