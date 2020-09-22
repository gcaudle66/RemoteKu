from tkinter import *
from tkinter import messagebox
from tkinter.constants import *
import api
import requests
import time

### This is a basic working reote for power control

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

api_calls = {
    "device_info": "/query/device-info",
    "get_apps": "/query/apps",
    "power_cycle": "/keypress/power"
    }

def dadspwr():
    for item in dadBOTH:
        result = pwr(item)#requests.post(item + ":8060/keypress/power")
        global running
        global counter
        running = True
        counter = -1
        msg_box(result)

def pwr(dev):
    r = requests.post(dev + ":8060/keypress/power")
    if r.status_code == 200:
        result = "OK"
    else:
        result= "ERROR"
    return result

def pwrbtn_click(dev):
    result = pwr(dev)
    global running
    global counter
    running = True
    counter = -1
    msg_box(result)
    #label = Label(root, text="Result: {}".format((result)))


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
#msg_frame_label = Label(msg_frame, text="Welcome")
button1 = Button(root, text="L Pwr", command=lambda: pwrbtn_click(dadL))  # , padx=50, pady=100)
button2 = Button(root, text="R Pwr", command=lambda: pwrbtn_click(dadR))
button5 = Button(root, text="LR TV Pwr", command=lambda: pwrbtn_click(lrTV))
button3 = Button(root, text="Both Pwr", command=dadspwr)
button4 = Button(root, text="Exit", command=root.destroy)
button1.grid(row=1, column=0)
button2.grid(row=1, column=1)
button3.grid(row=1, column=2)
button4.grid(row=2)
msg_frame.grid(row=3, columnspan=2)#fill="both", expand="yes")
#msg_frame_label.pack()
label.pack()

root.mainloop()
