"""
Max Rohloff 2/2/2022
Gets input of first and last name, splits it and spits it back out
"""


#Variable used in while loop
x = 0

#List used for spliting the name that is inputted
splitname = ["",""]

#While loop used for input and testing
while x != 2:
    name = input("Please enter your first and last name: ")
    splitname = name.split(" ")

#Tests to confirm only two names were entered
    if len(splitname) != 2:
        print("Please enter a last name")
        x = 0
        continue
    
#Tests to see if the two names are alpha characters or not
    if splitname[0].isalpha() != True or splitname[1].isalpha() != True:
        print("Please only enter letters")
        x = 0
        continue
    x = 2

#Print function to print names        
print("Welcome to Python " + splitname[0] + ". " + splitname[1] + " is a really interesting surname! Are you related to the famous Victoria "\
      + splitname[1])
