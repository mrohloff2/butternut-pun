ntpServer = {"Server1" : "221.100.250.75",
             "Server2": "201.0.113.22",
             "Server3": "58.23.191.6"}
def PingPrep(ipList):
    for valued in ipList.keys():
        ipList[valued] = ("Ping:" + ipList[valued])
    for prints in ipList.values():
        print(prints)

def printDict():
    for Keys in ntpServer.keys():
        print(Keys , "    ", ntpServer[Keys])

#Question 2
printDict()
#Question 3
PingPrep(ntpServer)