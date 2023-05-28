import requests
import json

"""
Max Rohloff
3/14/2023
Purpose: Make changes to our VLANs, SVIs, HSRP, and OSPF with the given information
"""

def getCookie(url):
    # NX REST API Authen See REST API Reference for format of payload below

    # url = "https://"+ addr + "/api/aaaLogin.json"

    payload = {"aaaUser":
                   {"attributes":
                        {"name": "cisco",
                         "pwd": "cisco"}
                    }
               }

    response = requests.post(url, json=payload, verify=False)

    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]


#Gathers information to be used in our program
def getInfo(type):

    Verify = None


    if type == "svi":
        print("Next lets create a SVI")
        Verify = None
        while Verify != True:
            intip = input("Please enter the IP of the interface: ")
            Verify = verifyIP(intip)
            ipmask = input("Please enter the subnet mask: ")
            if int(ipmask) > 32:
                print("Subnet mask should be a number between 1 - 32")
                Verify = False
            intip = intip + "/24"
    else:
        intip = None


    if type == "hsrp":
        print("Next lets add HSRP to an interface")
        Verify = None
        hsrpint = input("Please enter the interface number: ")
        while Verify != True:
            hsrpip = input("Please enter the IP of the interface:")
            Verify = verifyIP(hsrpip)
        hsrpgroup = input("Please enter the group number for HSPF: ")
        return hsrpint, hsrpip, hsrpgroup


    if type == "ospf":
        print("Next lets add OSPF to an interface")
        Verify = None
        ospfInt = input("Please enter the interface number you would like to add OSPF to: ")
        ospfID = input("Please enter the ospf ID: ")
        while Verify != True:
            ospfArea = input("Please enter the ospf Area:")
            Verify = verifyIP(ospfArea)
        return ospfInt, ospfID, ospfArea


    if type == "svi" or type == "vlan":
        if type == "vlan":
            print("We will start by setting up a vlan on the specified device")
        intnum = input("Please enter the vlan number of the interface:")
        Verify = None
        while Verify != True:
            intname = input("Please enter a new interface name, it must start with a letter and must not having any special characters\n")
            Verify = checkName(intname)
        return intip,intnum,intname




# This function verifies that both the IP and subnet are valid
def verifyIP(IPadd):
    a = 0
    check = 0
    IPaddsplit = IPadd.split(".")


    # If statements for checking if IP address is valid
    if len(IPaddsplit) == 4:
        for c in range(4):
            if (int(IPaddsplit[c]) <= 255 and int(IPaddsplit[c]) >= 0):
                a += 1
        if a == 4:
            check += 1
            a = 0
            return True
        else:
            print("Your IP address is not valid, please review proper IP addressing configuration")

    else:
        print("Your IP address is not valid, please review proper IP addressing configuration")




#Checks if the hostname is correct
def checkName(name):
    if name[0].isalpha() == True and name.isalnum() == True:
        return True
    else:
        print("The provided name does not meet requirements, try again.")
        return False



#This function creates the vlan
def createInt(ip, intnum, intname, headers):


        url = "https://" + ip + "/api/node/mo/sys/intf.json?query-target=children"
        payload = {
            "sviIf": {
                "attributes": {
                    "adminSt": "up",
                    "id": "vlan" + intnum,
                    "vlanId": intnum,
                    "name": intname
                }
            }
        }
        response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload))

        ##

        url = "https://" + ip + "/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"
        payload = {
            "ipv4If": {
                "attributes": {
                    "dn": "sys/ipv4/inst/dom-default/if-[vlan" + intnum + "]",
                    "id": "vlan" + intnum

                }
            }
        }
        response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload))



#This function adds the given IP to the vlan
def addIPtoInt(ip, intip, intnum, headers):
    url = "https://" + ip + "/api/node/mo/sys/ipv4/inst/dom-default/if-[vlan" + intnum + "].json?query-target=children"

    payload = {
        "ipv4Addr": {
            "attributes": {
                "addr": intip
            }
        }
    }

    response = requests.request("POST", url, verify= False, headers=headers, data=json.dumps(payload))



#This function adds the given information into HSRP
def addHSRP(ip, hsrpinterface, hsrpgroup, hsrpip, headers):

    url = "https://" + ip + "/api/node/mo/sys/hsrp/inst/if-[vlan" + hsrpinterface + "].json?query-target=children"
    payload = {
        "hsrpIf": {
            "attributes": {
                "dn": "sys/hsrp/inst/if-[vlan" + hsrpinterface + "]",
                "adminSt": "enabled",
                "id": "vlan" + hsrpinterface
            }
        }
    }
    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload))


    url = "https://" + ip + "/api/node/mo/sys/hsrp/inst/if-[vlan" + hsrpinterface + "]/grp-" + hsrpgroup + "-ipv4.json?query-target=children"
    payload = {
        "hsrpGroup": {
            "attributes": {
                "af": "ipv4",
                "dn": "sys/hsrp/inst/if-[vlan" + hsrpinterface + "]/grp-" + hsrpgroup + "-ipv4",
                "id": hsrpgroup,
                "ip": hsrpip
            }
        }
    }
    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload))


#This function adds our OSPF ID, area, and interface to the configuration
def addOSPF(ip, ospfInt, ospfID, ospfArea, headers):

    url = "https://" + ip + "//api/node/mo/sys/ospf/inst-1/dom-default.json?query-target=children"

    payload = {
        "ospfIf": {
            "attributes": {
                "adminSt": "enabled",
                "area": ospfArea,
                "dn": "sys/ospf/inst-1/dom-default/if-[vlan" + ospfInt + "]",
                "helloIntvl": "10",
                "id": "vlan" + ospfInt,
                "prio": ospfID

            }
        }
    }
    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload))

def main():
    DictTest = True
    #Dictonary for testing
    devices = {
        1: {
            "ip": "10.10.20.177",
            "intip" : "172.16.110.2/24",
            "intnum" : "110",
            "intname": "testNXOS",
            "hsrpip":"172.16.110.1",
            "hsrpgroup": "10",
            "ospfID": "1",
            "ospfArea": "0.0.0.0"
        },
        2: {
            "ip" : "10.10.20.178",
            "intip": "172.16.110.3/24",
            "intnum": "110",
            "intname": "testNXOS",
            "hsrpip": "172.16.110.1",
            "hsrpgroup": "10",
            "ospfID": "1",
            "ospfArea": "0.0.0.0"
    }
    }

    #Comment out this if statement if you do not want to test with the dictonary
    if devices != None:
        DictTest = False



    x = 1
    for i in range(1,3,1):
        type = None
        interfaceip = None

        cookie = getCookie('https://' + devices[i]["ip"] + '/api/aaaLogin.json')

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'APIC-cookie=' + cookie
        }


        #Creating vlan

        if DictTest == True:
            type = "vlan"
            devices[i]["intip"], devices[i]["intnum"], devices[i]["intname"] = getInfo(type)
        createInt(devices[i]["ip"], devices[i]["intnum"], devices[i]["intname"], headers)

        #Creating SVI

        if DictTest == True:
            type = "svi"
            devices[i]["intip"], devices[i]["intnum"], devices[i]["intname"] = getInfo(type)
        createInt(devices[i]["ip"], devices[i]["intnum"], devices[i]["intname"], headers)
        addIPtoInt(devices[i]["ip"], devices[i]["intip"], devices[i]["intnum"], headers)

        #Adding HSRP
        if DictTest == True:
            type = "hsrp"
            devices[i]["intnum"], devices[i]["hsrpip"], devices[i]["hsrpgroup"] = getInfo(type)
        addHSRP(devices[i]["ip"], devices[i]["intnum"], devices[i]["hsrpgroup"], devices[i]["hsrpip"], headers)

        #Adding OSPF
        if DictTest == True:
            type = "ospf"
            devices[i]["intnum"], devices[i]["ospfID"], devices[i]["ospfArea"] = getInfo(type)
        addOSPF(devices[i]["ip"], devices[i]["intnum"], devices[i]["ospfID"], devices[i]["ospfArea"], headers)


main()