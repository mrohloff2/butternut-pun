import requests
import json

"""
Max Rohloff
4/3/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices then change the IP address information
"""

#Gets interface information
def getIntRest(ipAddr):
    url = "https://"+ipAddr+":443/restconf/data/ietf-interfaces:interfaces"
    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
    response = response.json()
    return response.get("ietf-interfaces:interfaces")


#Formats our list for printing
def combineList(intList):
    NewList = []

    intList = intList["interface"]

    for i in range(len(intList)):
        newDict = dict(intList[i])
        for x in newDict:
            try:
                if x == "ietf-ip:ipv4":
                    newIntdict = dict(newDict['ietf-ip:ipv4']['address'][0])
                    NewList.append({"Interface":newDict["name"],"IP": newIntdict["ip"]})
            except:
                print("")

    return NewList

#Prints the new list
def printList(combinedList):
    print("Int                  IP ")
    print("________________________________")
    for i in combinedList:
        print(i["Interface"],end="   ")
        print(i["IP"])


#Verifies that the new IP address is valid
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


#Updates the IP address for the given interface
def updateDevInt(ipAddr,intName,intIP):
    url = "https://"+ipAddr+":443/restconf/data/ietf-interfaces:interfaces/interface="+intName
    username = 'cisco'
    password = 'cisco'
    payload = {"ietf-interfaces:interface": {
        "name": intName,
        "description": "Configured by RESTCONF",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": "true",
        "ietf-ip:ipv4": {
            "address": [{
                "ip": intIP,
                "netmask": "255.255.255.252"

            }]
        }
    }
    }

    headers = {
        'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
        'Accept': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username, password), headers=headers, verify=False,
                                data=json.dumps(payload)
                                )


def main():
    test = False
    ipAddr = "10.10.20.175"
    intList = getIntRest(ipAddr)
    combinedList = combineList(intList)
    printList(combinedList)

    while test == False:
        intName = input("Which interface would you like to edit?\n")
        for i in combinedList:
            if intName == i["Interface"]:
                test = True
        if test == False:
            print("Invalid Interface")
    test = False
    while test == False:
        intIP = input("Please enter a valid IP address to change the interface to?\n")
        if verifyIP(intIP) == True:
            test = True
        else:
            print("Invalid IP")
    updateDevInt(ipAddr,intName,intIP)
    intList = getIntRest(ipAddr)
    combinedList = combineList(intList)
    printList(combinedList)

main()