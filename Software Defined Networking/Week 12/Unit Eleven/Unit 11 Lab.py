import ipaddress
from collections import OrderedDict

"""
Max Rohloff
4/3/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices and print Mac Addresses
"""
import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict
import ipaddr

def getInts():
    router = {"host": "10.10.20.175", "port" : "830",
              "username":"cisco","password":"cisco"}

    netconf_filter = """

    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>

    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter))

    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

    interfaces = netconf_data["interfaces"]["interface"]

    return interfaces

def printInts(interfaces):
    print("Int                  IP               Subnet Mask                  Description")
    print("_________________________________________________________________________________")
    for i in interfaces:
        if i["name"] != "Loopback0":
            print(i["name"], end="   ")
            print(i["ipv4"]["address"]["ip"], end="   ")
            print(i["ipv4"]["address"]["netmask"], end="   ")
            print(i["description"])



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
            return False
    else:
        print("Your IP address is not valid, please review proper IP addressing configuration")
        return False
def changeInt(interfaces,intName,intIP,ipmask,description):
    c = 0
    for i in interfaces:
        if i["name"] == intName:
            interfaces[c]["description"] = description
            interfaces[c]["ipv4"]["address"]["ip"] = intIP
            interfaces[c]["ipv4"]["address"]["netmask"] = ipmask
        c += 1
    return interfaces



def main():
    test = False
    Verify = False
    interfaces = getInts()
    printInts(interfaces)

    while test == False:
        intName = input("Which interface would you like to edit?\n")
        for i in interfaces:
            if intName == i["name"]:
                test = True
                oneinterface = i
        if test == False:
            print("Invalid Interface")

    test = False
    while test == False:
        intIP = input("Please enter a valid IP address to change the interface to?\n")
        test = verifyIP(intIP)
        if test == True:
            while Verify == False:
                ipmask = input("Please enter the subnet mask: \n")
                if (int(ipmask)) <= 32 and (int(ipmask)) > 0:
                    Verify = True
                    combintIP = intIP + "/" + ipmask
                    add = ipaddress.IPv4Interface(combintIP)
                    add = (str(add.with_netmask)).split("/")
                    ipmask = add[1]
                else:
                    print("Subnet mask should be a number between 1 - 32")



    description = input("What would you like the description to be?\n")

    interfaces = changeInt(interfaces, intName, intIP, ipmask,description)
    printInts(interfaces)




main()