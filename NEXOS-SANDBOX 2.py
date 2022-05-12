
#################### I wrote both scripts in the same file, I have commented out the second part to this script
import requests
import json

"""
Max Rohloff
2/22/2022
Purpose: Pull information from our switch, changing the hostname. Second script asks for IP address and changes it by two
"""


#Defining login credentials 
switchuser='cisco'
switchpassword='cisco'

#Testing to see if variable is okay for a hostname for a switch
def Check(host):
    if host[0].isalpha() == True and host.isalnum() == True:
        return True
    else:
        print("Hostname does not meet requirements, try again.")
        return False
    

#Send data to website and returns information from switch
def SendCLI(host):
    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "configure terminal",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "hostname " + str(host),
          "version": 1
        },
        "id": 2
      }
    ]


    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    print(response)
    return response

#Main

host = input("Please enter a new hostnam, it must start with a letter and must not having any special characters\n")
Verify = Check(host)
if Verify == True:
    info = SendCLI(host)



#########################################################################################################################################

'''
#Check IP address is formatted correctly
def Check(IPadd):
    a = 0
    IPaddsplit = IPadd.split(".")
    
#If statements for checking if IP address is valid
    if len(IPaddsplit) ==  4:
        for c in range(4):
            if (int(IPaddsplit[c]) <= 255 and int(IPaddsplit[c]) >= 0):
                a += 1
        if a == 4:
            IPaddsplit[2] = str(int(IPaddsplit[2]) + 2)


            ####An easier way to join a list to show in the assignment would be just to join the list using the join command like below
            return ".".join(IPaddsplit)

#Main
    
IPadd = input("Please enter the new IP address in the format x.x.x.x where x is a number between 0 and 255\n")
NewIP = Check(IPadd)
print("The new IP is:", NewIP)
'''
