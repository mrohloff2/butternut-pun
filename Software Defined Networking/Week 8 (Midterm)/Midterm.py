import requests
import json

"""
Max Rohloff
3/12/2022
Purpose: Pull information from our switchs and increase IP addressing for our vlans
"""


#Function used to properly print show interface brief command
def printIPbri(otherIP):
    #Changing IP address to what is needed
    if otherIP == '10.10.20.177':
        print("Switch 1: 10.10.20.177\n")
    else:
        if otherIP == '10.10.20.178':
            print("Switch 2: 10.10.20.178\n")
    FS = otherIP

    
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+FS+'/ins'
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

#This gets the vlans and IP addresses into an a list for our api to easily access

def getVlansandIPs(IPbrief):
    IPadd = IPbrief

    Mylist = ['','','','','','','','','','','','']
    a = -1
    p = 0
    
    for i in range(len(IPadd)):
        new = str(IPadd[i])
        more = new
        if new[0] == "V":
            a += 1
            p = 1
            Mylist[a] = new
        if IPadd[i] == 'prefix':
            String = IPadd[i+1].split(".")
            String[3] = str(int(String[3]) + 5)
            String = str(".".join(String))
            a +=1
            Mylist[a] = String

    #My list a list I created to make it easier for me to parse data to changeAdd
    return Mylist
    

#Changes the IP addresses based on the given interface
def changeAdd(NewIP,Vlan,IP,otherIP):
    switchuser='cisco'
    switchpassword='cisco'
    

    url='https://'+otherIP+'/ins'
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
          "cmd": "int " + str(Vlan),
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip address " + str(IP) + " 255.255.255.0",
          "version": 1
        },
        "id": 3
      }
    ]
    
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    




#Main

#Other IP is the first IP, more can be added in first function    
otherIP = '10.10.20.177'

#Counter for while loop
h = 0

#While loop to make changes to both interfaces
while h != 2:
    a = -1
    b = 0
    IPbrief = printIPbri(otherIP)
    NewIP = getVlansandIPs(IPbrief)
    for q in range(len(NewIP)-1):
        a += 1
        b += 1

        ###UNCOMMENT THESE STATEMENTS TO RESET IPS TO DEFAULT VALUES
        """
        NewIP = ['Vlan101', '172.16.101.2', 'Vlan102', '172.16.102.2', 'Vlan103', '172.16.103.2', 'Vlan104', '172.16.104.2', 'Vlan105', '172.16.105.2', '172.16.252.1', '172.16.252.5']
        if h == 1:
            NewIP = ['Vlan101', '172.16.101.3', 'Vlan102', '172.16.102.3', 'Vlan103', '172.16.103.3', 'Vlan104', '172.16.104.3', 'Vlan105', '172.16.105.3', '172.16.252.9', '172.16.252.13']
        """

        Vlan = NewIP[a]
        IP = NewIP[b]
        changeAdd(NewIP,Vlan,IP,otherIP)
        
    printIPbri(otherIP)   
    h = h + 1
    otherIP = '10.10.20.178'

