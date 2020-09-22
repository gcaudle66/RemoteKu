from tkinter import *
from tkinter.ttk import *
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
devs = {
    "dadL": "http://192.168.0.111",
    "dadR": "http://192.168.0.203",
    "lrTV": "http://192.168.0.200",
    "sisTV": "http://192.168.1.199",
    "parkTV": "http://192.168.1.198"
    }
    
api_calls = {
    "device_info": "/query/device-info",
    "get_apps": "/query/apps",
    "power_cycle": "/keypress/power"
    }

alive_devs = []

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

def pwr_status(dev):
        api_call = ":8060/query/device-info"
        try:
            r = requests.get(dev, api_call, timeout=5)
        except TimeoutError as to_err:
            print("Timeout Error Occured on : {}".format(dev))
            pwr_status = "Unknown"
            pwr_color = "red"
            return pwr_color
        except requests.exceptions.ConnectTimeout as tout_err:
            print("ConnectTimeout Error Occured on : {}".format(dev))
            pwr_status = "Unknown"
            pwr_color = "red"
            return pwr_color
        except requests.exceptions.ConnectionError as conn_err:
            print("Connect Error -No Route to Host- Occured on : {}".format(dev))
            pwr_status = "Unknown"
            pwr_color = "red"
            return pwr_color
        else:
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

values = ["None"]
def list_devs():
    index = 1
    for key, value in devs.items():
        entry = "#{} : {}".format(index, key)
        values.insert(index, entry)
        index = index + 1
    return values
values = list_devs()

root = Tk()
root.title("RemoteKu C5dev--..")
root.minsize(width=250, height=70)
top_frame = Frame(root).pack()
btm_frame = Frame(root).pack(side="bottom")
combo1 = Combobox(top_frame)
combo1["values"]=values
combo1.current(0)
combo1.pack()

##button1 = Button(root, text="L Pwr", bg="white", command=lambda: pwrbtn_click(dadL))  # , padx=50, pady=100)
##button2 = Button(root, text="R Pwr", bg="white", command=lambda: pwrbtn_click(dadR))
##button5 = Button(root, text="LR TV Pwr", bg="white", command=lambda: pwrbtn_click(lrTV))
##button3 = Button(root, text="Both Pwr", command=dadspwr)
##button6 = Button(root, text="Park Pwr", bg="white", command=lambda: pwrbtn_click(parkTV))
##button7 = Button(root, text="Sis Pwr", bg="white", command=lambda: pwrbtn_click(sisTV))
##button4 = Button(root, text="Exit", command=root.destroy)
##button1.grid(row=1, column=0)
##button2.grid(row=1, column=1)
##button3.grid(row=1, column=2)
##button5.grid(row=2, column=0)
##button6.grid(row=2, column=1)
##button7.grid(row=2, column=2)
##button4.grid(row=4)
##msg_frame.grid(row=3, columnspan=10)#fill="both", expand="yes")
##label.pack()

root.mainloop()
