from tkinter import *
from tkinter import messagebox
from tkinter.constants import *
import api
import requests

api_port = ":8060"
dadL = "http://192.168.0.111"
dadR = "http://192.168.0.203"
dad_devices = [dadL, dadR]
lrTV = "http://192.168.0.200"

api_calls = {
    "device_info": "/query/device-info",
    "get_apps": "/query/apps",
    "power_cycle": "/keypress/power"
    }


tk = Tk()
frame = Frame(tk, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
label1 = Label(frame, text="RemoteKu")
label.pack(fill=X, expand=1)
def power_cycle(dev):
    url = dev + api_port + api_calls.get("power_cycle")
    r = requests.post(url)
    result = dev + f" : {str(r.status_code)}"
    msg = messagebox.showinfo("Pwr Result", result)


button1 = Button(frame,text="L Pwr",
button2 = Button(frame,text="R Pwr",command=tk.destroy)
button3 = Button(frame,text="Both Pwr",command=tk.destroy)
button4 = Button(frame,text="Exit",command=tk.destroy)
button1.place()
#button1.pack(side=BOTTOM)
button2.pack(side=BOTTOM)
button3.pack(side=BOTTOM)
button4.pack(side=BOTTOM)
tk.mainloop()
