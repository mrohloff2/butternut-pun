import requests
import json

"""
Max Rohloff
4/3/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices
"""



#Pulls unformatted information from our IOS XE devices
def getInts(ip):

    url = "https://"+ip+":443/restconf/data/ietf-interfaces:interfaces"
    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
    ints = response.json()
    return (ints.get("ietf-interfaces:interfaces"))



#Prints the interfaces
def printInts(Interfaces):
    Interfaces = Interfaces['interface']

    for i in range(len(Interfaces)):
        newDict = dict(Interfaces[i])
        for x in newDict:

            if x == "name" and newDict["name"]!="Loopback0":
                print(newDict["name"]+"      ",end="")
            try:
                if x == "ietf-ip:ipv4" :
                    newIntdict = dict(newDict['ietf-ip:ipv4']['address'][0])
                    print(newIntdict["ip"]+"  ",end="")
                    print(newIntdict["netmask"])
            except:
                print("")




def main():

    ip = input("Please enter the IP address of a IOSXE device: ")
    try:
        Interfaces = getInts(ip)  #This gets the interfaces model
        printInts(Interfaces)  # This iterates the dictionary that is returned
    except:
        print("The provided IP address was not valid")


main()
