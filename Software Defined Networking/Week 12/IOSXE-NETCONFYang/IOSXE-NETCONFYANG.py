from collections import OrderedDict

"""
Max Rohloff
4/3/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices and print Mac Addresses
"""

def script1():
    router1 = {
        "brand": "Cisco",
        "model": "1941",
        "mgmtIP": "10.0.0.1",
        "G0 / 0": "10.0.1.1",
        "G0 / 1": "10.0.2.1",
        "G0 / 2": "10.1.0.1"
    }

    router1 = OrderedDict(router1)
    for i in router1.keys():
        print("Key = " + i,end="     ")
        print("Value = " + router1[i])

def main():
    #Uncomment the following code to run the first part of the assignment
    #script1()
    interface = OrderedDict([('name', 'GigabitEthernet1'),
                             ('description', 'to port6.sandbox-backend'),
                             ('type', OrderedDict([
                                 ('@xmlns:ianaift', 'urn:ietf:params:xml:ns:yang:iana-if-type'),
                                 ('#text', 'ianaift:ethernetCsmacd')
                             ])
                              ),
                             ('enabled', 'true'),
                             ('ipv4', OrderedDict([
                                 ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip'),
                                 ('address', OrderedDict([
                                     ('ip', '10.10.20.175'),
                                     ('netmask', '255.255.255.0')
                                 ])
                                  )]
                             )
                              ),
                             ('ipv6', OrderedDict([
                                 ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip')]
                             )
                              )
                             ])

    print(interface['ipv4']['address']['ip'] + "\t" + interface['ipv4']['address']['netmask'])



main()