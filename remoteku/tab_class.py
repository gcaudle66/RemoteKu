import tkinter
from tkinter import *
from tkinter.constants import *
from tkinter import ttk
from tkinter.ttk import *
import requests
import time

class Tab:
    def __init__(self, name, url, status, msgbox, state, index):
        self.tab_title = name
        self.url = url
        self.status = dev_status
        self.msgbox = msgbox
        self.state = state

        tab = ttk.Frame(notebook1)
        notebook1.add(self.index, text=self.name)
        ##########Current Tab Config Btns etc

        btn1 = ttk.Button(self.index, text="Pwr", command=lambda:api_post(self.url,api_calls.get("power_cycle"))).grid(row=1, column=1)
        btn2 = ttk.Button(self.index, text=" ^ ").grid(row=1, column=2)
        btn3 = ttk.Button(self.index, text="Input", command=lambda:input_hdmi_cycle(self.url,cur_hdmi)).grid(row=1, column=3)

        btn4 = ttk.Button(self.index, text=" < ").grid(row=2, column=1)
        btn5 = ttk.Button(self.index, text="Enter").grid(row=2, column=2)
        btn6 = ttk.Button(self.index, text=" > ").grid(row=2, column=3)

        btn7 = ttk.Button(self.index, text=" ").grid(row=3, column=1)
        btn8 = ttk.Button(self.index, text="\/").grid(row=3, column=2)
        btn9 = ttk.Button(self.index, text="Vol Up", command=lambda:api_post(self.url,api_calls.get("vol_up"))).grid(row=3, column=3)

        btn10 = ttk.Button(self.index, text="Pwr L+R ", command=dadspwr).grid(row=4, column=1)
        btn11= ttk.Button(self.index, text="Stat").grid(row=4, column=2)
        btn12 = ttk.Button(self.index, text="Vol Dn", command=lambda:api_post(self.url,api_calls.get("vol_down"))).grid(row=4, column=3)


        msg_frame1 = LabelFrame(self.index, text = "Message Box")

        
        self.msgbox = Label(msg_frame1, text="Welcome").pack()

        msg_frame1.grid(sticky="s", columnspan=10)
