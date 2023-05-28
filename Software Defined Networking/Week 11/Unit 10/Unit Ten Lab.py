import requests
import json

"""
Max Rohloff
4/3/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices and print Mac Addresses
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


#Gets interface state information which we pull the Mac Address from
def getIntRestMAC(ipAddr):
    url = "https://"+ipAddr+":443/restconf/data/interfaces-state"
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
    return response.get("ietf-interfaces:interfaces-state")


#Combines the seperate lists and returns the newly created list
def combineList(intStateList, intList):
    NewList = []

    intList = intList["interface"]
    intStateList = intStateList["interface"]
    for i in range(len(intList)):
        newDict = dict(intList[i])
        newDict2 = dict(intStateList[i])
        for x in newDict:
            try:
                if x == "ietf-ip:ipv4":
                    newIntdict = dict(newDict['ietf-ip:ipv4']['address'][0])
                    NewList.append({"Interface":newDict["name"],"IP": newIntdict["ip"], "MacAddress":newDict2["phys-address"]})
            except:
                print("")

    return NewList


#Prints the newly combined list
def printList(combinedList):
    print("Int                  IP               Physical")
    print("_____________________________________________________")
    for i in combinedList:
        print(i["Interface"],end="   ")
        print(i["IP"], end="   ")
        print(i["MacAddress"])



def main():
    ipAddr = "10.10.20.175"
    intList = getIntRest(ipAddr)
    intStateList = getIntRestMAC(ipAddr)
    combinedList = combineList(intStateList, intList)
    printList(combinedList)


main()