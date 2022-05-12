"""
Max Rohloff 2/2/2022
Purpose: Add IP to an interface

"""
x = 0
y = 0
t = 0
IPaddsearch = ""

#Dictionary to be used in our program
router1 = {
    "brand": "Cisco",
    "model": "1941",
    "mgmtIP" : "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.0.3.1 /24",
    "hostname": "r1"
    }

router1["G0/2"] = "10.1.3.1 /24"
router1["model"] = "2901"


#Function for printing router1 dictionary
def PrintDict(router1):
    x = 0
    for Keys in router1.keys():
    
        x = x+1
        if x <= 2:
            print(Keys, end = "\t")
        else:    
            print(Keys, end = "\t\t")
    print("\n--------------------------------------------------------------------------------------------------------------------")
    for Values in router1.values():
        Values1 = Values.split(" ")
        print(Values1[0], end = "\t")
    

#main
PrintDict(router1)
Question = input("\nDo you want to change the management IP address? ")

if Question == "No" or Question == "no": exit()

if Question == "yes" or Question == "Yes":
    while t == 0:
        a = 0
        q = 0
        #Getting input
        IPadd = input("Please enter the new IP address in the format x.x.x.x where x is a number between 0 and 255:\n")
        IPaddsplit = IPadd.split(".")

        #If statements for checking if IP address is valid
        if len(IPaddsplit) ==  4:
            t = 0
            for c in range(4):
                if (int(IPaddsplit[c]) <= 255 and int(IPaddsplit[c]) >= 0):
                    a += 1
            if a == 4:
                router1["mgmtIP"] = str(IPadd)
                t = 1
                PrintDict(router1)
        if t == 0:
            print("Please enter only 4 numbers between 0 and 255 in the format x.x.x.x\n")
            
        
