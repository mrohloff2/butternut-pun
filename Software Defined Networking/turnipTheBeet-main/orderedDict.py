from collections import OrderedDict

interface = OrderedDict([('name', 'GigabitEthernet1'),
                         ('description', 'to port6.sandbox-backend'),
                         ('type',OrderedDict([
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
