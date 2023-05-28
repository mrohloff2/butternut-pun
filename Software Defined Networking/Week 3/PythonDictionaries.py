"""
Max Rohloff
3/6/2022
Purpose: Learning Dictionaries
"""


router1 = {
    "hostname": "R1",
    "brand": "Cisco",
    "model": "1941",
    "mgmtIP" : "10.0.0.1",
    "interfaces":{
        
        "G0/0": "10.0.1.1",
        "G0/1": "10.0.2.1"
    }
}

#printing dictionary
print("Router keys")
print(router1.keys())
print("Router1[interfaces] keys")
print(router1["interfaces"].keys())
print("Router values")
print(router1.values())
print("Router1[interfaces] values")
print(router1["interfaces"].values())
print("Router items")
print(router1.items())
print("Router1[interfaces] items")
print(router1["interfaces"].items())

################################################################################################

#Dictionary for devices
devices = {
    "R1":{
        "type": "router",
        "hostname": "R1",
        "mgmtIP": "10.0.0.1"
        },
    "R2":{
        "type": "router",
        "hostname": "R2",
        "mgmtIP": "10.0.0.2"
        },
    "S1":{
        "type": "switch",
        "hostname": "S1",
        "mgmtIP": "10.0.0.3"
        },
    "S2":{
        "type": "switch",
        "hostname": "S2",
        "mgmtIP": "10.0.0.4"
        }
    }

#For loop to print IPs with ping
for i in devices.keys():
        print("ping " + devices[i]["mgmtIP"])
