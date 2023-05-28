

from ncclient import manager


router = {"host": "10.10.20.175", "port" : "830",
          "username":"cisco","password":"cisco"}

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




print(xmlInt)

xmlInt = xmlInt.replace("%addr%", "172.16.1.2")
xmlInt = xmlInt.replace("%intName%", "GigabitEthernet")
xmlInt = xmlInt.replace("%intNum%", "2")
xmlInt = xmlInt.replace("%mask%", "255.255.255.0")
print(xmlInt)



with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

    netconf_reply = m.edit_config(target = 'running', config = xmlInt)
    print(netconf_reply)

