import requests
import json

"""
Max Rohloff
3/6/2022
Purpose: Pull information from our switch and make an IP change to the choosen interface
"""


#Function used to properly print show interface brief command
def printIPbri():
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}

    payload=[
      {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show ip interface brief",
      "version": 1
        },
     "id": 1
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    Table = str(response["result"]['body']['TABLE_intf']['ROW_intf'])
    for i in "'",'{','}','[',']',"\"":
        Table = str(Table.replace(i,''))
    Table = str(Table.replace(',',':'))    
    Table = Table.split(':')
    print(" Name         Proto     Link      Address")
    print("--------------------------------------------")  
    for i in range(len(Table)):
        Table[i] = Table[i].strip()
        if Table[i] == 'intf-name':
            print(Table[i+1],"\t",end='')               
        if Table[i] == 'proto-state':
            print(Table[i+1],"\t",end='')
        if Table[i] == 'link-state':
            print(Table[i+1],"\t",end='')
        if Table[i] == 'prefix':
            print(Table[i+1],"\t",end='\n')
    return Table


#This function verfies the interface name is valid, it uses the Table produce in printIPbri()
def verifyInt(Interface,IPbrief):
    for i in range(len(IPbrief)):
        IPbrief[i] = IPbrief[i].strip()
        if IPbrief[i] == 'intf-name':
            if str(IPbrief[i+1]) == str(Interface):
                return 1
    print("Your interface name does not match any configured interfaces, review table above and try again.")
    

#This function verfies that both the IP and subnet are valid 
def verifyIP(IPadd,Subnet):
    a = 0
    check = 0
    IPaddsplit = IPadd.split(".")
    Subnetsplit = Subnet.split(".")
    
    #If statements for checking if IP address is valid
    if len(IPaddsplit) ==  4:
        for c in range(4):
            if (int(IPaddsplit[c]) <= 255 and int(IPaddsplit[c]) >= 0):
                a += 1
        if a == 4:
            check += 1
            a = 0
        else:
            print("Your IP address is not valid, please review proper IP addressing configuration")
            
    else:
        print("Your IP address is not valid, please review proper IP addressing configuration")
        
    #If statements for checking if subnet is valid        
    if len(Subnetsplit) ==  4:
        for c in range(4):
            if (int(Subnetsplit[c]) == 255 or int(Subnetsplit[c]) == 254 or int(Subnetsplit[c]) == 252  or int(Subnetsplit[c]) == 248\
                or int(Subnetsplit[c]) == 240 or int(Subnetsplit[c]) == 224 or int(Subnetsplit[c]) == 192 or int(Subnetsplit[c]) == 128\
                or int(Subnetsplit[c]) == 0):
                a += 1
        if a == 4:
            check += 1   
        else:
            print("Your subnet is not valid, please review proper subnetting configurations")
            return False
    else:
        print("Your subnet is not valid, please review proper subnetting configurations")
        return False
    

    if check == 2:
        return True
    else:
        check = 0
        return False


#Changes the IP address on the given interface
def changeAdd(Interface,IPadd,Subnet):

    switchuser='cisco'
    switchpassword='cisco'

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
          "cmd": "interface " + str(Interface),
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip address " + str(IPadd) + " " + str(Subnet),
          "version": 1
        },
        "id": 3
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()




#Main
CheckInt = 0
CheckIP = False

IPbrief = printIPbri()
Interface = input("What interface would you like to edit? ")
checkInt = verifyInt(Interface, IPbrief)

#Checking to confirm checkInt passed its tests before continuing 
if checkInt == 1:
    IPadd = input("Please enter the new IP address in the format x.x.x.x where x is a number between 0 and 255: ")
    Subnet = input("Please enter the subnet in the form of x.x.x.x, where x is a number between 0 and 255: ")
    checkIP = verifyIP(IPadd,Subnet)

#Checking to confirm checkInt and checkIP passed their tests before continuing
if checkInt == 1 and checkIP == True:
    changeAdd(Interface,IPadd,Subnet)
    printIPbri()
    
