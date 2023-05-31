import json
from time import sleep
import pandas as pd
import requests

"""
Max Rohloff
4/24/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices then change the IP address information by asking the user which interface and IP they would like to change
"""

net_controller = {"name": "localhost:58000",
                  "username": "student",   # Change the username to match the username set up in lab
                  "password": "cisco"  #Change password to match password set up in lab
                  }


 #Gets ticket info
def get_ticket(controller,username,password):
    api_url = "http://{}/api/v1/ticket".format(controller)

    headers = {
        "content-type": "application/json"
        }

    body_json = {
        "username": username,
        "password": password
        }

    response = requests.post(api_url,json.dumps(body_json),headers=headers,verify=False)

    # print("Ticket request status: ",response.status_code)

    response_json = response.json()

    ticket = response_json["response"]["serviceTicket"]
    #print("The service ticket number is: ", ticket)

    return ticket

#Gets information about hosts
def get_hosts(cont, auth_ticket):
    host_url = "http://{}/api/v1/host".format(cont)

    headers = {"X-Auth-Token": auth_ticket}

    response = requests.get(host_url, headers=headers, verify=False)

    # print("Request status: ",response.status_code)

    hosts = response.json()["response"]
    return hosts

#Gets information about devices
def get_devices(cont, auth_ticket):
    host_url="http://{}/api/v1/network-device".format(cont)

    headers = {"X-Auth-Token":auth_ticket}

    response = requests.get(host_url,headers=headers,verify=False)

    #print("Request status: ",response.status_code)

    devices=response.json()["response"]
    return devices


#Gets flow analysis
def run_flow_analysis(cont,auth_ticket,source_ip, destination_ip):
    base_url = "http://{}/api/v1/flow-analysis".format(cont)
    headers = {"X-Auth-Token":auth_ticket}

    # initiate flow analysis
    body = {"destIP": destination_ip, "sourceIP": source_ip}
    initiate_response = requests.post(base_url, headers=headers, verify=False,
                                      json=body)
    flowAnalysisId = initiate_response.json()["response"]["flowAnalysisId"]
    detail_url = base_url + "/{}".format(flowAnalysisId)
    detail_response = requests.get(detail_url, headers=headers, verify=False)
    while not detail_response.json()["response"]["request"]["status"] == "COMPLETED":  # noqa: E501
        print("Flow analysis not complete yet, waiting 5 seconds")
        sleep(5)
        detail_response = requests.get(detail_url, headers=headers,
                                       verify=False)

    # Return the flow analysis details
    return detail_response.json()["response"]

#Verifies that the give IPs are valid
def verifyHosts(hosts, devices, endpoint1,endpoint2):
    check = 0
    for i in hosts:
        #print(endpoint1)
        if i["hostIp"] == str(endpoint1):
            check = check + 1
        if i["hostIp"] == str(endpoint2):
            check = check + 1
    for i in devices:
        if i['managementIpAddress'] == str(endpoint1):
            check = check + 1
        if i['managementIpAddress'] == str(endpoint2):
            check = check + 1

        for x in i['ipAddresses']:
            if x == str(endpoint1):
                check = check + 1
            if x == str(endpoint2):
                check = check + 1
    if check >= 2:
        return True
    else:
        print("One or both of the IP addresses were incorrect, please try again:\n")
        return False

#Gathers information about single devices
def get_single_device(cont,auth_ticket,dev_id):
    host_url="http://{}/api/v1/network-device/{}".format(cont,dev_id)
    headers = {"X-Auth-Token":auth_ticket}
    response = requests.get(host_url,headers=headers,verify=False)
    return response.json()


#Prints information about flow
def printFlow(flow,devices,tablelist,hosts, endpoint1, endpoint2):
    if endpoint1 == hosts[0]["hostIp"]:
        tablelist[0] = [hosts[0]["hostName"], "Pc", "", "", endpoint1, ""]
    if endpoint1 == hosts[1]["hostIp"]:
        tablelist[0] = [hosts[1]["hostName"], "Pc", "", "", endpoint1, ""]

    for i in devices:
        if flow["request"]["sourceIP"] == i['managementIpAddress']:
            tablelist[0] = [i["hostname"], i["type"], i["productId"], i["reachabilityStatus"],
                            flow["request"]["sourceIP"], i["upTime"]]
        for x in i['ipAddresses']:
            if flow["request"]["sourceIP"] == x:
                tablelist[0] = [i["hostname"], i["type"], i["productId"], i["reachabilityStatus"], flow["request"]["sourceIP"], i["upTime"]]

    for i in devices:
        devicelist = [i["hostname"], i["type"], i["productId"], i["reachabilityStatus"], i["managementIpAddress"], i["upTime"]]
        tablelist.append(devicelist)

    for i in devices:
        for x in i['ipAddresses']:
            if flow["request"]["destIP"] == x:
                   devicelist = [i["hostname"], i["type"], i["productId"], i["reachabilityStatus"], flow["request"]["sourceIP"], i["upTime"]]

    if endpoint2 == hosts[0]["hostIp"]:
        devicelist = [hosts[0]["hostName"], "Pc", "", "",endpoint2, ""]

    if endpoint2 == hosts[1]["hostIp"]:
        devicelist = [hosts[1]["hostName"], "Pc", "", "",endpoint2, ""]

    tablelist.append(devicelist)
    table = pd.DataFrame(tablelist, columns = ["Name", "Type", "Platform", "status", "MgmtIP","Uptime"])
    print(table.to_string())



#Main
def main():
    c = 0
    tablelist = [[""]]
    test = False
    endpoint1 = ""
    endpoint2 = ""
    singledevices = []

    controller = net_controller["name"]  # URL from Dictionary defined above
    username = net_controller["username"]  # Username from Dictionary defined above
    password = net_controller["password"]  # Password from Dictionary defined above

    serviceTicket = get_ticket(controller, username, password)

    hosts = get_hosts(controller, serviceTicket)
    devices = get_devices(controller, serviceTicket)

    while test == False:
        endpoint1 = input("Please enter the first endpoint (source IP): \n")
        endpoint2 = input("Please enter the second endpoint (destination IP): \n")
        test = verifyHosts(hosts, devices, endpoint1, endpoint2)

    source_ip = endpoint1
    destination_ip = endpoint2
    flow = run_flow_analysis(controller, serviceTicket, source_ip, destination_ip)

    printFlow(flow, devices, tablelist, hosts, endpoint1, endpoint2)

main()