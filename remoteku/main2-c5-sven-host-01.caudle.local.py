from tkinter import *
from tkinter import messagebox
from tkinter.constants import *
import api
import requests
import time

### This is a basic working reote for power control
stats_counter = 30
counter = 0
running = False
timing = 0
result = "NULL"
msg_box_text = ""
api_port = ":8060"
dadL = "http://192.168.0.111"
dadR = "http://192.168.0.203"
dadBOTH = [dadL, dadR]
lrTV = "http://192.168.0.200"
sisTV = "http://192.168.1.199"
parkTV = "http://192.168.1.198"
response = {}
devs = {}
    
api_calls = {
    "device_info": "/query/device-info",
    "get_apps": "/query/apps",
    "power_cycle": "/keypress/power",
    "active_app": "/query/active-app",
    "vol_up": "/keypress/volumeup",
    "vol_down": "/keypress/volumedown"
    }

alive_devs = []

def api_req(dev, api_call):
    import xmltodict
    try:
        r = requests.get(dev + api_port + api_call, timeout=10)
    except Exception as exc:
        response = "ERR"
    except ConnectionError as connerr:
        response = "ERR"
    except TimeoutError:
        response = "ERR"
    r_code = r.status_code
    if r_code == 200:
        print("REQUEST WAS A SUCCESS. DEVICE RETURNED: {} ".format(str(r)))
        r2 = r.text
        response = xmltodict.parse(r2, xml_attribs=False)
        return response
    else:
        response = "UnknownERR"
        dev.state(DISABLED)
        return response

def dadspwr():
    for item in dadBOTH:
        result = pwr(item)#requests.post(item + ":8060/keypress/power")
        global running
        global counter
        running = True
        counter = -1
        msg_box(result)

def pwr(dev):
    try:
        r = requests.post(dev + ":8060/keypress/power")
    except Exception as e:
        result = "Exception thrown"#: {}".format(e))
        return result
    else:
        if r.status_code == 200:
            result = "OK"
        else:
            result= "ERROR"
            return result

def pwrbtn_click(dev):
    result = pwr(dev)
    pwr_state_fg = pwr_status(dev)
    global running
    global counter
    running = True
    counter = -1
    msg_box(result)

def active_app(dev):
    api_call = api_calls.get("active_app")
    response = api_req(dev)
    act_app = response.get("active-app").get("app")
    return act_app

def pwr_status(dev):
        api_call = "/query/device-info"
        try:
            response = api_req(dev, api_call)
        except TimeoutError as to_err:
            response = "Timeout Error Occured on : {}".format(dev)
            pwr_status = "Unknown"
            pwr_color = "red"
            return pwr_color
        dev_info = response.get("device-info")
        pwr_state = dev_info.get("power-mode")
        if pwr_state == "Ready":
            pwr_status = "Ready"
            pwr_color = "orange"
            return pwr_color
        elif pwr_state == "PowerOn":
            pwr_status = "On"
            pwr_color = "green"
            return pwr_color
        else:
            pwr_status = "Unknown"
            pwr_color = "red"
            return pwr_color


def msg_box(msg_label):
    def count():
        if running:
            global counter

# To manage the intial delay.
            if counter==-1:
                display=msg_label
            elif counter > 20:
                display=""
            else:
                display=msg_label#str(counter)
                timing = display

            label['text']=display # Or label.config(text=display)

# label.after(arg1, arg2) delays by
# first argument given in milliseconds
# and then calls the function given as second argument.
# Generally like here we need to call the
# function in which it is present repeatedly.
# Delays by 1000ms=1 seconds and call count again.
            label.after(1000, count)
            counter += 10
        else:
            if counter >= 1:
                display = (counter)
                timing = display
                print("DEBUG: The timing var shows " + str(timing))
                print("DEBUG: Timer clocked  " + str(counter))
                label['text']=display
                
                print("DEBUG: sending " + str(display) + " to convert_time....")
                return convert_time(counter)
            else:
                print("Value to low")
# Triggering the start of the counter.
    count()

root = Tk()
root.title("RemoteKu C5dev--..")
root.minsize(width=250, height=70)
msg_frame = LabelFrame(root, text = "Message Box")
label = Label(msg_frame, text="Welcome")
button1 = Button(root, text="L Pwr", bg="white", fg=pwr_status(dadL), command=lambda: pwrbtn_click(dadL))  # , padx=50, pady=100)
button2 = Button(root, text="R Pwr", bg="white", fg=pwr_status(dadL), command=lambda: pwrbtn_click(dadR))
button5 = Button(root, text="LR TV Pwr", bg="white", fg=pwr_status(lrTV), command=lambda: pwrbtn_click(lrTV))
button3 = Button(root, text="Both Pwr", command=dadspwr)
button6 = Button(root, text="Park Pwr", bg="white", fg="red", command=lambda: pwrbtn_click(parkTV))
button7 = Button(root, text="Sis Pwr", bg="white", fg=pwr_status(sisTV), command=lambda: pwrbtn_click(sisTV))
button4 = Button(root, text="Exit", command=root.destroy)
button1.grid(row=1, column=0)
button2.grid(row=1, column=1)
button3.grid(row=1, column=2)
button5.grid(row=2, column=0)
button6.grid(row=2, column=1)
button7.grid(row=2, column=2)
button4.grid(row=4)
msg_frame.grid(row=3, columnspan=10)#fill="both", expand="yes")
#msg_frame_label.pack()
label.pack()

root.mainloop()
