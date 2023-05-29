"""
Max Rohloff
4/17/2023
Purpose: Pull information with YANG, using the xml style we gather info from the user and change the interface"""

import ipaddress
from ncclient import manager

def getInfo():
    router = {"host": "10.10.20.175", "port": "830",
              "username": "cisco", "password": "cisco"}

    ### xmlns:xc added for ios xe 17.x and greater

    xmlInt = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">  
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <interface>
                                <%intName%>
                    <name>%intNum%</name>
    
                    <ip>                                    
                                        <address>
                                            <primary>
                                                <address>%addr%</address>
                                                <mask>%mask%</mask>
                                             </primary>
                                        </address>                                   
                    </ip>				
                    </GigabitEthernet>
                </interface>
    
                    </native>
            </config>"""


    return xmlInt, router

#Checks the IP address
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
            return False
    else:
        print("Your IP address is not valid, please review proper IP addressing configuration")
        return False

#Checks the subnet mask and converts it to cidr notation
def checkMask(intIP, ipmask):

    if (int(ipmask)) <= 32 and (int(ipmask)) > 0:
        Verify = True
        combintIP = intIP + "/" + ipmask
        add = ipaddress.IPv4Interface(combintIP)
        add = (str(add.with_netmask)).split("/")
        ipmask = str(add[1])
        return Verify, ipmask
    else:
        print("Subnet mask should be a number between 1 - 32")
        return False


#Changes the IP interface
def changeInt(interface, deviceinfo, intIP, mask):

    interface = interface.replace("%addr%", intIP)
    interface = interface.replace("%intName%", "GigabitEthernet")
    interface = interface.replace("%intNum%", "2")
    interface = interface.replace("%mask%", mask)

    with manager.connect(host=deviceinfo['host'], port=deviceinfo['port'], username=deviceinfo['username'], password=deviceinfo['password'],hostkey_verify=False) as m:
        netconf_reply = m.edit_config(target='running', config=interface)


def main():
    Verify = False
    test = False
    interface, deviceinfo = getInfo()
    while test == False:
        intIP = input("Please enter a valid IP address to change the interface to?\n")
        test = verifyIP(intIP)
        if test == True:
            while Verify == False:
                ipmask = input("Please enter the subnet mask: \n")
                Verify, mask = checkMask(intIP, ipmask)
    changeInt(interface, deviceinfo, intIP, mask)


main()