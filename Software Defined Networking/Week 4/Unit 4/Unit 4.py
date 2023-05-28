"""
Max Rohloff 2/10/2023
Purpose: Draw a number of decks and cards and determine who wins by adding card values

"""

import requests
playerval = 0
compval = 0
vals = False

#validates is the number of decks they give us is a valid input
def validate(count):
    if count.isalpha():
        print("Please only enter a number between 1 and 5")
        return False
    if count.isnumeric():
        count = int(count)
        if count > 0 and count <=5:
            return True
        else:
            return False
    else:
        return False

#This gets the deck of cards we are going to draw from
def getCards(count):
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    deck1 = response.json()
    id = deck1["deck_id"]
    url = ("https://deckofcardsapi.com/api/deck/" + id + "/draw/?count=" + count)
    response = requests.request("GET", url, headers=headers, data=payload)
    cardsDrawn = response.json()
    return cardsDrawn

#This determines would the winner will be based on the total value of the cards
def findWinner(playerval,compval):
    if playerval > compval:
        print("The player has won")

    if playerval < compval:
        print("The computer has won")

    if playerval == compval:
        print("The game resulted in a draw")

#This converts face cards to ints and adds all cards to send the value to findWinner
def addCards(Cards):
    val = 0

    for number in Cards["cards"]:
        if number["value"] == 'JACK':
            val += 11
        if number["value"] == 'QUEEN':
            val += 12
        if number["value"] == 'KING':
            val += 13
        if number["value"] == 'ACE':
            val += 14
        if number["value"] != 'KING' and number["value"] != 'QUEEN' and number["value"] != 'JACK' and number["value"] != 'ACE':
            val += int(number["value"])
    return val


#Checks to make sure value of count is an int between 1 and 5
while vals == False:
    count = input("How many cards would you like to draw, please choose between 1 and 5?")
    vals = validate(count)


playerCards = getCards(count)
CompCards = getCards(count)

playerval = addCards(playerCards)
compval = addCards(CompCards)

print("The computer drew the following cards")
for cards in CompCards["cards"]:
    print(cards["value"] + " of " + cards["suit"])
print("The computer has a total score of ", compval)

print("The player drew the following cards")
for cards in playerCards["cards"]:
    print(cards["value"] + " of " + cards["suit"])
print("The player has a total score of ", playerval)

findWinner(playerval,compval)


