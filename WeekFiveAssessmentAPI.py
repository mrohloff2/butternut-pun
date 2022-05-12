"""
Max Rohloff 2/16/2022
Parse data and print cisco information
"""


import requests
import json

"""
Be sure to run feature nxapi first on Nexus Switch

"""
switchuser='cisco'
switchpassword='cisco'


#Variables used to parse json data
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


#Function used to send cli and return dictionary
def sendCLI():
    responses = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()
    return dict(responses)


    
#main
#Calling sendCLI function and setting response
response = sendCLI()

#Printing out information needed
print("Name         Proto    Link         Address")
print("-----        ------  ------       --------")
for i in range(7):
    print(response['result']['body']['TABLE_intf']['ROW_intf'][i]['intf-name']+ "\t\t" + response['result']['body']['TABLE_intf']['ROW_intf'][i]['proto-state'] + "\t" +response['result']['body']['TABLE_intf']['ROW_intf'][i]['link-state'],"\t", response['result']['body']['TABLE_intf']['ROW_intf'][i]['prefix'])
