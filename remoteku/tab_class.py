import tkinter
from tkinter import *
from tkinter.constants import *
from tkinter import ttk
from tkinter.ttk import *
import requests
import time
import gui
import concurrent.futures

class Tab:
    def __init__(self, name, url, status, msgbox, state):
        self.tab_title = name
        self.url = url
        self.status = dev_status
