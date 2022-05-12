import requests
import json


"""
Max Rohloff
2/22/2022
Purpose: Gather information from our switches
"""


devices ={

   "dist-sw01" : {
    "hostname": "dist-sw01",
    "deviceType": "switch",
    "mgmtIP": "10.10.20.177"
    },

    "dist-sw02" : {
    "hostname": "dist-sw02",
    "deviceType": "switch",
    "mgmtIP": "10.10.20.178",
    }  
    }



#Prints dictionary
def printDict(devices):
    localDevice = devices
    print("Host      Type      MgmtIP",end="")
    for keys in localDevice.keys():
        print("\n")
        for keys2 in localDevice[keys].keys():
            print(localDevice[keys][keys2],end="  ")

#Sends show ver command to switches           
def sendCLI(mgmtIP):
    switchuser='cisco'
    switchpassword='cisco'
    url='https://'+mgmtIP+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show version",
          "version": 1
        },
        "id": 1
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    return response

#Prints data for the switches
def printVer(Answer):
    print("Your hostname is: " + Answer["result"]["body"]["host_name"])
    print("Your memory size is:", Answer["result"]["body"]["memory"], Answer["result"]["body"]["mem_type"])
    print("Your chassis is:", Answer["result"]["body"]["chassis_id"])
    print("Your boot file name is:", Answer["result"]["body"]["kick_file_name"])


#Sends show ospf command to switches                    
def getOSPFNeighbor(mgmtIP):
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+mgmtIP+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show ip ospf neighbor",
          "version": 1
        },
        "id": 1
      }
    ]
    
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    return response

#Takes variable from getospf function and formats it to look as it should and prints
def printOSPFNeighbor(OSPFAnswer):
    OSPFA = OSPFAnswer
    Table = str(OSPFA["result"]['body']['TABLE_ctx']['ROW_ctx']['TABLE_nbr']['ROW_nbr'])
    for i in "'",'{','}','[',']',"\"":
        Table = str(Table.replace(i,''))
    Table = str(Table.replace(',',':'))    
    Table = Table.split(':')
    print("Router-ID        Neighbor IP        Int")
    print("----------------------------------------")               
    for i in range(len(Table)):
        Table[i] = Table[i].strip()
        if Table[i] == 'rid':
            print(Table[i+1],"\t",end='')               
        if Table[i] == 'addr':
            print(Table[i+1],"\t",end='')
        if Table[i] == 'intf':
            print(Table[i+1],"\t",end='\n') 




#Main
printDict(dict(devices))
for key in devices.keys():
    Answer = sendCLI(devices[key]["mgmtIP"])
    printVer(Answer)
for key in devices.keys():
    OSPFAnswer = getOSPFNeighbor(devices[key]["mgmtIP"])
    printOSPFNeighbor(OSPFAnswer)
