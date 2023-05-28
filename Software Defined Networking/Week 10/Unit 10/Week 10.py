import requests
import json

"""
Max Rohloff
3/14/2023
Purpose: Make changes to our VLANs, SVIs, HSRP, and OSPF with the given information
"""

def getCookie(url):
    # NX REST API Authen See REST API Reference for format of payload below

    # url = "https://"+ addr + "/api/aaaLogin.json"

    payload = {"aaaUser":
                   {"attributes":
                        {"name": "cisco",
                         "pwd": "cisco"}
                    }
               }

    response = requests.post(url, json=payload, verify=False)

    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]



#Uses a get request to import the data into a readable list which is converted to a dictionary and iterated through

def getInterfaces(headers):
    payload = None
    url = "https://10.10.20.177/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"
    response = requests.get(url, verify=False, headers=headers)

    interfaces = response.json()
    interfaces = interfaces.get('imdata')
    for i in range(len(interfaces)):
        intdict = dict(interfaces[i])
        s intdict['ipv4If']['attributes']:
            if x == "id" or x =="dn":
                print(intdict['ipv4If']['attributes'][x] + "  ",end="")
        print("")




#Main function

def main():

    cookie = getCookie('https://10.10.20.177/api/aaaLogin.json')

    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'APIC-cookie=' + cookie
    }

    getInterfaces(headers)


main()

