import requests
import json

import xmltodict
from ncclient import manager

"""
Max Rohloff
4/17/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices then change the IP address information
"""
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


#Prints the dictionary in a nice manner
def printInts(interfaces):
    print("Int                  IP               Subnet Mask                  Description")
    print("_________________________________________________________________________________")
    for i in interfaces:
        if i["name"] != "Loopback0":
            print(i["name"], end="   ")
            print(i["ipv4"]["address"]["ip"], end="   ")
            print(i["ipv4"]["address"]["netmask"], end="   ")
            print(i["description"])


def main():
    test = False
    ips = {"10.10.20.175":"dist-rtr01","10.10.20.176":"dist-rtr02"}
    ipAddr = ""
    for i in ips:
        ipAddr = i
        host = ips[ipAddr]
        print("Host name: ", host)
        interfaces = getInts()
        printInts(interfaces)

main()