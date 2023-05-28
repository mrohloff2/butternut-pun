'''
Max Rohloff
1/30/2023
Purpose: Introduction and testing input values
'''

def anameis(x, name):
    # Tests to confirm only two names were entered
    print(name)
    if len(name) != 2:
        print("Please enter a last name")
        return x
        # Tests to see if the two names are alpha characters or not
    if name[0].isalpha() != True or name[1].isalpha() != True:
        print("Please only enter letters")
        x = 0
        return x
    x = 2
    return x


# Variable used in while loop
x = 0

# List used for spliting the name that is inputted
splitname = ["", ""]

# While loop used for input and testing
while x != 2:
    name = input("Please enter your first and last name: ")
    splitname = name.split(" ")
    x = anameis(x, splitname)


# Print function to print names
print("Welcome to Python " + splitname[0] + ". " + splitname[
    1] + " is a really interesting surname! Are you related to the famous Victoria " \
      + splitname[1])
