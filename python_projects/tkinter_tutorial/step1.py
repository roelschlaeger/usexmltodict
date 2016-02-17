#! C:\Python34\python34.EXE

import sys
if sys.version_info < (3, 0):
    raise DeprecationWarning("Only supported for Python 3.x")

########################################################################

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style

from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

# import urllib
# import json
# import pandas as pd
# import numpy as np

########################################################################

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

########################################################################

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)
# a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

########################################################################


def animate(i):
    """Fetch data from sampleData.txt and plot it"""
    pullData = open("sampleData.txt", "r").read()
    dataList = pullData.split("\n")
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(",")
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList, yList)

# Initial coding from
# Styling GUIs and windows in Python 3 - Tkinter tutorial Python 3.4
#
# https://www.youtube.com/watch?v=A0gaXfM1UN0 Video 2
# https://www.youtube.com/watch?v=Y6cir7P3YUk Video 3
# https://www.youtube.com/watch?v=jBUpjijYtCk Video 4
# https://www.youtube.com/watch?v=oV68QJJUXTU Video 5
# https://www.youtube.com/watch?v=Zw6M-BnAPP0 Video 6
# https://www.youtube.com/watch?v=JQ7QP5rPvjU&index=7&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk Video 7 & Playlist
# https://www.youtube.com/watch?v=eJRLftYo9A0&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=8 Video 8 & Playlist

########################################################################


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Sea of BTC Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage, PageOne, BTCePage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

########################################################################


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self,
                         text="""\
ALPHA Bitcoin Trading Application
Use at your own risk.
There is no promise of warranty.""",
                         font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(
            self,
            text="Agree",
            command=lambda: controller.show_frame(PageOne)
        )
        button1.pack()

        button2 = ttk.Button(
            self,
            text="Disagree",
            command=quit
        )
        button2.pack()

########################################################################


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()

        # button2 = ttk.Button(
        #     self,
        #     text="Visit Page 2",
        #     command=lambda: controller.show_frame(PageTwo)
        # )
        # button2.pack()

        button3 = ttk.Button(
            self,
            text="Visit Graph Page",
            command=lambda: controller.show_frame(BTCePage)
        )
        button3.pack()

########################################################################

# class PageTwo(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page Two", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#         button1 = ttk.Button(
#             self,
#             text="Back to Home",
#             command=lambda: controller.show_frame(StartPage)
#         )
#         button1.pack()
#
#         button2 = ttk.Button(
#             self,
#             text="Visit Page 1",
#             command=lambda: controller.show_frame(PageOne)
#         )
#         button2.pack()
#
#         button3 = ttk.Button(
#             self,
#             text="Visit Graph Page",
#             command=lambda: controller.show_frame(BTCePage)
#         )
#         button3.pack()

########################################################################


class BTCePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        NavigationToolbar2TkAgg(canvas, self)

########################################################################

app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()

########################################################################
