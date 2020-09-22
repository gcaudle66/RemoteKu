import requests
ip  = "192.168.0.111"
url = "http://{}:8060".format(ip)
dads = ["192.168.0.111", "192.168.0.203"]

def pwr():
	for item in dads:
		r = requests.post("http://" + item + ":8060/keypress/power")
		print(item + str(r.status_code))

if __name__ == "__main__":
	pwr()
