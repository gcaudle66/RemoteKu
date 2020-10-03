import requests
import json
import xmltodict

disco_mcast = "http://239.255.255.250:1900"
api_port = ":8060"
#Sapi_url = dev_url + api_port


## below api_call var is for test and dev initially
api_call = ""

dad_devices = [
    {
    "dadleftTV_url": "http://192.168.0.111",
    "dadrightTV_url": "http://192.168.0.203"
    }
    ]

static_devices = [
    {
    "dadleftTV_url": "http://192.168.0.111",
    "dadrightTV_url": "http://192.168.0.203",
    "LivingroomTV": "http://192.168.0.200"
    }
    ]

device_groups = [dad_devices, static_devices]

devices = [static_devices, dad_devices]

api_calls = {
    "device_info": "/query/device-info",
    "get_apps": "/query/apps",
    "power_cycle": "/keypress/power"
    }

def list_calls():
    index = 1
    call_list = []
    print("## List of Roku API Calls ##")
    for key in api_calls:
        print("#{} : {}".format(index, key))
        entry = call_list.insert(index, key)
        index = index + 1
    print("############################")
    choice = int(input("Input Call # to Proceed or Ctrl-C to Exit : "))
    call = call_list[choice - 1]
    api_call = api_calls.get(call)
    return api_call

def list_devs():
    """
    """
    dev_list = []
    index = 1
    print("## List of Roku Devices and Groups ##")
    print("Static Devices List------")
    for item in static_devices[0].items():
        print("#{} : {} ".format(index, str(item)))
        entry = dev_list.insert(index, item)
        index = index + 1
    print("Device Group List------")
    print("#{} : {} ".format(index, str("dad_devices")))
    entry = dev_list.insert(index, dad_devices)
    print("###########################")
    choice = int(input("Select Device or Group # to Proceed or Ctrl-C to Exit"))
    dev = dev_list[choice - 1]
    return dev

def gather():
    """
    """
    data = []
    print("#### Gathering data to run task ####")
    dev = list_devs()
    print(" Device selected is : {} ".format(dev))
    print("Gathering API Call info")
    api_call = list_calls()
    print("API Call Selected : {} ".format(api_call))
    if api_call == "/keypress/power":
        print("#### Power Cycle Chosen ####")
        result = power_cycle(dev[1])
    return data

def dev_data():
    """
    unfinished will do later
    """
    print("Using Static Dict DB..." \
          "{} Devices Total to Check...".format(len(static_devices)))
    print("Checking devices state.......")
    for item in static_devices:
        alive = requests.get(api_url)

def api_req(api_url, api_call):
    full_api_req = api_url + api_port + api_call
    r = requests.get(full_api_req)
    r_code = r.status_code
    if r_code == 200:
        print("REQUEST WAS A SUCCESS. DEVICE RETURNED: {} ".format(str(r)))
        r2 = r.text
        response = xmltodict.parse(r2, xml_attribs=False)
        return response
    
## Below is working key press for power on/off
###### r3 = requests.post(device_url + api_port + "/keypress/power")
def power_cycle(dev_url):
    """
    """
    import xmltodict
    import time
    while True:
        api_url = dev_url
        api_call = "/query/device-info"
        response = api_req(api_url, api_call)
        dev_info = response.get("device-info")
        pwr_state = dev_info.get("power-mode")
        if pwr_state == "Ready":
            print("Device is currently sleeping...sending wake up...")
            rOn = requests.post(api_url + api_port + "/keypress/power")
            time.sleep(3)
            break
        elif pwr_state == "PowerOn":
            print("Device is currently powered on...powering off")
            rOff = requests.post(api_url + api_port + "/keypress/power")
            time.sleep(3)
            result = "Power Turned off. Exiting."
            return result


if __name__ == "__main__":
    gather()
