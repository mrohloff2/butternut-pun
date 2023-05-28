'''
Max Rohloff
1/30/2023
Purpose: Introduction and testing input values
'''

#devices variable that holds information for our fuctions

devices = {
	"R1": {
		"type" : "router",
		"hostname" : "R1",
		"mgmtIP" : "10.0.0.1"
	},
	"R2" :{
		"type" : "router",
		"hostname" : "R2",
		"mgmtIP" : "10.0.0.2"
	},
	"S1": {
		"type" : "switch",
		"hostname" : "S1",
		"mgmtIP" : "10.0.0.3"
	},
	"S2": {
		"type" : "switch",
		"hostname" : "S2",
		"mgmtIP" : "10.0.0.4"
}
}

#Checking if the IP given is valid
def checkIP(IPaddsplit):
	a = 0
	print(IPaddsplit)
	if len(IPaddsplit) == 4:
		for c in range(4):
			if IPaddsplit[c].isnumeric():
				if int(IPaddsplit[c]) <= 255 and int(IPaddsplit[c]) >= 0:
					a += 1
				if a == 4:
					return True
			else:
				print(IPaddsplit[c], "is not a number")
				return False
	else:
		return False

#Adding ping to mgmtIP value
def pingList(devices):
	for Keys in devices.keys():
		mot = devices[Keys]
		for Next in mot.keys():
			if Next == "mgmtIP":
				devices[Keys][Next] = "Ping:" + devices[Keys][Next]
	print(devices)
	return devices

IP = False

#Asking if they would like to add a device and logic behind it
Question = input("\nWould you like to add a new device?\n")
if Question == "yes" or Question == "Yes":
	Type = input("What will the type of device be? (R, r, S, s)\n")
	if Type == "R" or Type == "r":
		devicestype = "Router"
	else:
		devicestype = "Switch"
	deviceshostname = input("What will the name of the device be?\n")
	while IP == False:
		devicesIP = input("Please enter the IP address in the format x.x.x.x where x is a number between 0 and 255\n")

		IPaddsplit = devicesIP.split(".")
		IP = checkIP(IPaddsplit)

#If statements for router and switch selection
if devicestype == "Router":
	devices["R3"] = {
		"type" : devicestype,
		"hostname" : deviceshostname,
		"mgmtIP" : devicesIP
	}
if devicestype == "Switch":
	devices["S3"] = {
		"type" : devicestype,
		"hostname" : deviceshostname,
		"mgmtIP" : devicesIP
	}
print(devices)
pingList(devices)
		

