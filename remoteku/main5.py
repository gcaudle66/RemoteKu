import tkinter
from collections import namedtuple
from tkinter import *
from tkinter.constants import *
from tkinter import ttk
from tkinter.ttk import *
import requests
import time
import datetime
import gui
import concurrent.futures
import logging
import json
import asyncio


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter  = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("RemoteKu_mainLog.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def logger_func(orig_func):
    import logging
    formatter2 = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
    file_handler2 = logging.FileHandler("RemoteKu.log")
    file_handler2.setFormatter(formatter2)
    logger.addHandler(file_handler2)
    def wrapper(*args, **kwargs):
        logger.debug("DEBUG log for Func {} with args:{} and kwargs:{}".format(orig_func, args, kwargs))
        return orig_func(*args, **kwargs)
    return wrapper

### This is basics such as variables and holders for devices
global cur_hdmi
stats_counter = 30
counter = 0
running = False
timing = 0
result = "NULL"
msg_box_text = ""
api_port = ":8060"
cur_hdmi = 1
devices_listing = []

root = tkinter.Tk()
root.wm_iconbitmap(default='wicon.ico')
#root.tk_setPalette(background='purple', activeBackground='white', foreground='green')

def toplevel_loading(devices_listing):
    t = 'loading...'
    toplevel2 = tkinter.Toplevel(root)
    toplevel2.title('Loading Devices...')
    label1 = ttk.LabelFrame(toplevel2)
    label1_1 = ttk.Label(label1, text=t)
    label1.place()
    label1_1.place()
    with open('devices.json', mode='r') as f:
        dev_in = json.load(f)
    for dev in dev_in.get('devices').items():
        devices_listing.append(dev)
    dev_states = generate_devs(devices_listing)
    toplevel2.destroy()
    return dev_states

def generate_devs(dev_in):
    dev_states = []
    for dev in dev_in:
        dev_url = 'http://{}'.format(dev[1].get('ip_address'))
        result = pwr_status(dev_url)
        dev_status = (result)
        dev_states.append(dev_status)
    return vals(dev_states)

dev_list = {
    "dadL": "http://192.168.0.111",
    "dadR": "http://192.168.0.203",
    "lrTV": "http://192.168.1.155",
    "sisTV": "http://192.168.1.199",
    "parkTV": "http://192.168.1.198"
    }

input_list = ['InputTuner', 'InputHDMI1','InputHDMI2', 'InputHDMI3', 'InputHDMI4']

dev_grps = {
    "dadBOTH": [dev_list.get("dadL"), dev_list.get("dadR")]
    }

api_calls = {
    "device_info": "/query/device-info",
    "get_apps": "/query/apps",
    "power_cycle": "/keypress/power",
    "active_app": "/query/active-app",
    "vol_up": "/keypress/volumeup",
    "vol_down": "/keypress/volumedown",
    "vol_mute": "/keypress/volumemute",
    "select": "/keypress/select",
    "home": "/keypress/home",
    "up": "/keypress/up",
    "down": "/keypress/down",
    "right": "/keypress/right",
    "left": "/keypress/left",
    "info": "/keypress/info",
    "input": "/keypress/inputhdmi{}".format(cur_hdmi)
    }

def inputs(input_list):
    inp_vals = []
    for value in input_list.values():
        inp_vals.append(value)
    return inp_vals


def dev_check(dev_list):
    dev_states = []
    dev_states = dev_status()
    return vals(dev_states)

def vals(dev_states):
    val_list = []
    for value in dev_states:
        if value[2] != 'red':
            val_list.append(value[0])
    return val_list

@logger_func
def api_post(dev, api_call):
    """
    Function for api POST calls
    """
    import xmltodict
    import pdb
    try:
        r = requests.post(dev + ':8060' + api_call, timeout=10)
    except Exception as exc:
        response = ["ERR", exc]
        return response[0]
    except ConnectionError as connerr:
        response = ["ERR", connerr]
        return response[0]
    except TimeoutError as toerr:
        response = ["ERR", toerr]
        return response[0], toerr
    r_code = r.status_code
    if r_code == 200:
        print("REQUEST WAS A SUCCESS. DEVICE {} RETURNED: {} ".format(n.get(), str(r)))
        r2 = r.text
        response = f'{r_code} - OK'
        return msg_box(response)

@logger_func    
def api_req(dev, api_call):
    """
    Function for api GET calls
    """
    import xmltodict
    import logging
    try:
        r = requests.get(dev + ':8060' + api_call, timeout=5)
    except Exception as exc:
        response = ["ERR", exc]
        return response[0]
    except ConnectionError as connerr:
        response = ["ERR", connerr]
        return response[0]
    except TimeoutError as toerr:
        response = ["ERR", toerr]
        return response[0], toerr
    r_code = r.status_code
    if r_code == 200:
        print("REQUEST WAS A SUCCESS. DEVICE RETURNED: {} ".format(str(r)))
        r2 = r.text
        response = xmltodict.parse(r2, xml_attribs=False)
        return response
    else:
        response = "UnknownERR"
        dev.state(DISABLED)
        return msg_box(response)
    

def active_app(dev):
    api_call = api_calls.get("active_app")
    response = api_req(dev, "get", api_call)
    act_app = response.get("active-app").get("app")
    return act_app

def dev_status():
    dev_states = []
    for key,value in dev_list.items():
        dev_url = value
        result = pwr_status(value)
        dev_status = (result)
        dev_states.append(dev_status)
    return dev_states

def dev_status_exec():
    dev_states = []
    for key,value in dev_list.items():
        dev_url = value
        with concurrent.futures.ProcessPoolExecutor() as executor:
            rslts = executor.map(pwr_status, dev_url)
            for r in rslts:
                print(r)
        dev_status = r
        dev_states.append(dev_status)
    return dev_states

def pwr_status(dev):
        api_call = "/query/device-info"
        try:
            response = api_req(dev, api_call)
        except TimeoutError as to_err:
            response = "Timeout Error Occured on : {}".format(dev)
            pwr_status = "Unknown"
            pwr_color = "red"
            return dev, pwr_status, pwr_color
        if response == 'ERR':
            response = "Timeout2 Error Occured on : {}".format(dev)
            pwr_status = "Unknown"
            pwr_color = "red"
            return dev, pwr_status, pwr_color
        dev_info = response.get("device-info")
        pwr_state = dev_info.get("power-mode")
        if pwr_state == "Ready":
            pwr_status = "Sleep"
            pwr_color = "orange"
            return dev, pwr_status, pwr_color
        elif pwr_state == "PowerOn":
            pwr_status = "On"
            pwr_color = "green"
            return dev, pwr_status, pwr_color
        else:
            pwr_status = "Unknown"
            pwr_color = "red"
            return dev, pwr_status, pwr_color



@logger_func
def input_hdmi_cycle(dev, cur_hdmi):
    import itertools
    hdmi_range = [1, 2, 3, 4]
    num = itertools.cycle(hdmi_range)
    cur_hdmi = num.__next__()
    response = api_post(dev, api_calls.get("input"), cur_hdmi)
    return response

def select_dev(eventObject):
    device = eventObject.get()
    label1["text"] = "OK"
    return device

## Toplevel window for sending api calls

apiPath_var = StringVar()
apiMethod_var = StringVar()
apiCall_var = StringVar()

@logger_func
def toplevel_apiCall():
    toplevel1 = Toplevel(root)
    toplevel1.title('RemoteKu-Send API Call')
    toplevel_label = Label(toplevel1, text="This window allows user to send API calls ").pack()
##                             "to the current device. Provide only the path below, the URL " \
##                             "and port auto-populate and the click the button to choose the " \
##                             "method for the call (GET or POST). ex. http://2.2.3.2:8060/query/device-info")
    path_label = Label(toplevel1, text="API Path:").pack()
    path_entry = Entry(toplevel1, textvariable=apiPath_var).pack()
    get_btn = Button(toplevel1, text="GET", command=lambda:build_apiCall("GET", apiPath_var)).pack()
    post_btn = Button(toplevel1, text="POST", command=lambda:build_apiCall("POST", apiPath_var)).pack()
    close_btn = Button(toplevel1, text="Close", command=toplevel1.destroy).pack()
##    return build_apiCall(apiPath_var)

##command=lambda:api_post(n.get(),api_calls.get("vol_mute"))
@logger_func
def build_apiCall(apiMethod, apiPath_var):
    dev = n.get()
    path = apiPath_var.get()
    if apiMethod == "POST":
        response =  api_post(dev, path)#requests.post(dev + ":8060" + path)
        print(response)
        return msg_box(response)
    elif apiMethod == "GET":
        response = api_req(dev, path)
        print(response)
        return msg_box(response)
    else:
        return msg_box("ERROR")
    
    
#### end toplevel

2##def toplevel_input():
##    ii = tkinter.StringVar()
##    toplevel1 = tkinter.Toplevel(root)
##    toplevel1.title('RemoteKu-Input Selector')
##    input_combobox = ttk.Combobox(toplevel1, textvariable=ii)
##    input_combobox['values'] = inputs(input_list)
##    input_combobox.grid()
##    toplevel1.bind('<<ComboboxSelected>>', select_input)
##    return toplevel1
##
##def select_input(eventObject):
####    ii = eventObject.get()
##    toplevel1.destroy()
##    return ii

def donothing():
    pass

def menu_close():
    root.destroy()
    
############## Below is GUI definitions
##root = Tk()
root.title("RemoteKu C5dev--..")
root.minsize(width=100, height=70)
font1 = ttk.Separator
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="New", command = donothing)
##filemenu.add_command(label = "Open", command = open_file)
filemenu.add_separator()
filemenu.add_command(label = "Close", command = menu_close)
menubar.add_cascade(label = "File", menu = filemenu)

style1 = ttk.Style()
style1.map("C.TButton", foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'purple')]
    )

top = ttk.Frame(root)
top.grid(columnspan=2, rowspan=2)

label1 = ttk.Label(top, text='Current Device').grid(column=0, row=1, pady=2)

n = tkinter.StringVar()
current_dev = ttk.Combobox(top, textvariable=n)
current_dev['values'] = toplevel_loading(devices_listing)#generate_devs(devices_listing)
current_dev.current()
current_dev.grid()
top.bind('<<ComboboxSelected>>', select_dev)

device = n.get()


sep1 = ttk.Separator(root, orient='horizontal').grid(row=2)

index = ttk.Frame(root).grid(columnspan=3, padx=0, pady=0)
##########Current Tab Config Btns etc
btn1Img = PhotoImage(file='images/pwr.png')
btn2Img = PhotoImage(file='images/nav_up.png')
btn3Img = PhotoImage(file='images/api.png')
btn4Img = PhotoImage(file='images/nav_left.png')
btn5Img = PhotoImage(file='images/nav_ok.png')
btn6Img = PhotoImage(file='images/nav_right.png')
btn7Img = PhotoImage(file='images/mute.png')
btn8Img = PhotoImage(file='images/nav_down.png')
btn9Img = PhotoImage(file='images/vol_up.png')
btn10Img = PhotoImage(file='images/home.png')
btn11Img = PhotoImage(file='images/info.png')
btn12Img = PhotoImage(file='images/vol_down.png')


btn1 = ttk.Button(index, style='C.TButton', text="Pwr", image=btn1Img, command=lambda:api_post(n.get(),api_calls.get("power_cycle"))).grid(row=3, column=0)
btn2 = ttk.Button(index, text=" ^ ", image=btn2Img, command=lambda:api_post(n.get(),api_calls.get("up"))).grid(row=3, column=1)
btn3 = ttk.Button(index, text="API Call", image=btn3Img, command=toplevel_apiCall).grid(row=6, column=0)

btn4 = ttk.Button(index, text=" < ", image=btn4Img, command=lambda:api_post(n.get(),api_calls.get("left"))).grid(row=4, column=0)
btn5 = ttk.Button(index, text="Enter", image=btn5Img, command=lambda:api_post(n.get(),api_calls.get("select"))).grid(row=4, column=1)
btn6 = ttk.Button(index, text=" > ", image=btn6Img, command=lambda:api_post(n.get(),api_calls.get("right"))).grid(row=4, column=2)

btn7 = ttk.Button(index, text="Mute", image=btn7Img, command=lambda:api_post(n.get(),api_calls.get("vol_mute"))).grid(row=5, column=0)
btn8 = ttk.Button(index, text="\/", image=btn8Img, command=lambda:api_post(n.get(),api_calls.get("down"))).grid(row=5, column=1)
btn9 = ttk.Button(index, text="Vol Up", image=btn9Img, command=lambda:api_post(n.get(),api_calls.get("vol_up"))).grid(row=5, column=2)

btn10 = ttk.Button(index, text="Home", image=btn10Img, command=lambda:api_post(n.get(),api_calls.get("home"))).grid(row=3, column=2)
btn11= ttk.Button(index, text="Info", image=btn11Img, command=lambda:api_post(n.get(),api_calls.get("info"))).grid(row=6, column=1)
btn12 = ttk.Button(index, text="Vol Dn", image=btn12Img, command=lambda:api_post(n.get(),api_calls.get("vol_down"))).grid(row=6, column=2)


msg_frame1 = LabelFrame(root, text = "Message Box",)

msg_initial = "Welcome"
label1 = Label(msg_frame1)
label1['text'] = msg_initial
label1.grid()
msg_frame1.grid(sticky="s", columnspan=3)

def msg_box(msg_label):
    counter = 3
    label1['text'] = msg_label
    return label1

root.config(menu = menubar)

if __name__ == '__main__':
    root.mainloop()
