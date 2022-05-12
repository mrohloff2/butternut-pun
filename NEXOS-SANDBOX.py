

import requests
import json

"""
Max Rohloff
2/22/2022
Purpose: Pull information from our switch
"""

#Defining login credentials 
switchuser='cisco'
switchpassword='cisco'

#Send data to website and returns information from switch
def SendCLI():
    url='https://10.10.20.177/ins'
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

#Main

info = SendCLI()
print("Your hostname is: " + info["result"]["body"]["host_name"])
print("Your memory size is:", info["result"]["body"]["memory"], info["result"]["body"]["mem_type"])

