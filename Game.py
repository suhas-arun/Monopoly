import random
import tkinter
from tkinter import messagebox
import csv


class Game:
    def __init__(self, parent, board, player1, player2):
        self.parent = parent
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.player1.label = tkinter.Label(
            self.parent,
            width=2,
            height=1,
            text=str(self.player1.number),
            bg=self.player1.colour,
            fg="white",
        )
        self.player2.label = tkinter.Label(
            self.parent,
            width=2,
            height=1,
            text=str(self.player2.number),
            bg=self.player2.colour,
            fg="white",
        )
        self.currentPlayer = self.player1
        self.die1 = "..."
        self.die2 = "..."

    def setupGame(self):
        self.board.drawBoard()
        self.board.drawPlayer(self.player1)
        self.board.drawPlayer(self.player2)

        self.board.displayPlayerInfo(self.player1)
        self.board.displayPlayerInfo(self.player2)

        self.board.displayPlayerOptions(self.currentPlayer, self.die1, self.die2, self)

        self.initialiseChances()

    def makeTurn(self):
        if self.currentPlayer.inJail:
            self.Jail()
            return

        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.board.displayPlayerOptions(
            self.currentPlayer, self.die1, self.die2, self
        )  # refresh dice display
        self.board.flashDiceBox()

        # prevents the player from rolling again
        self.board.roll_button.config(state="disabled")
        total = self.die1 + self.die2

        if self.die1 != self.die2:  # if the player doesn't roll a double...
            self.move(total)
            self.currentPlayer.noOfDoubles = 0
        else:
            self.currentPlayer.noOfDoubles += 1
            if (
                self.currentPlayer.noOfDoubles == 3
            ):  # if the player rolls three doubles in a row, they go to jail
                self.currentPlayer.inJail = True
                self.popup("three doubles")
                self.currentPlayer.position = 10
                self.board.updatePlayer(self.currentPlayer)
            else:
                if not self.currentPlayer.inJail:
                    self.move(total)
                    self.popup("double")
                    # lets the player roll again
                    self.board.roll_button.config(state="normal")

        self.board.displayPlayerInfo(self.currentPlayer)

        self.checkEndGame()
        self.board.end_turn.config(state="normal")

    def move(self, total):
        if self.currentPlayer.inJail:  # player can't move if they are in jail
            return

        self.currentPlayer.position += total  # moves player
        if self.currentPlayer.position > 39:  # checks if the player has passed GO
            self.currentPlayer.balance += 200  # get £200 for passing GO
            self.currentPlayer.position -= 39
            self.board.updatePlayer(self.currentPlayer)
            self.popup("go", 200)

        self.board.displayPlayerInfo(self.currentPlayer)
        self.board.updatePlayer(self.currentPlayer)
        current_place = self.board.places[self.currentPlayer.position]

        if current_place.type in ["property", "utility", "station"]:
            if current_place.type == "property":
                self.board.updateInfo(
                    "event", self.board.getProperty(current_place.getName())
                )
            else:
                self.board.updateInfo("event", current_place)
            if current_place.owner is None:  # if unowned, allow player to buy
                self.board.buy_button.config(state="normal")

            elif (
                current_place.owner == self.getOtherPlayer()
            ):  # if place is owned by the other player
                # pay rent
                self.popup("rent", current_place)
                otherPlayer = self.getOtherPlayer()
                if current_place.type == "property":
                    rent = self.board.getProperty(current_place.getName()).getRent()
                else:
                    rent = current_place.getRent(total)
                self.currentPlayer.payRent(rent, otherPlayer)
                # updates the other player's on-screen balance
                self.board.displayPlayerInfo(self.getOtherPlayer())

        elif current_place.type == "chance":
            self.Chance()
            self.board.updatePlayer(self.currentPlayer)
            # updates the other player's on screen balance
            self.board.displayPlayerInfo(self.getOtherPlayer())

        elif current_place.type == "tax":
            self.popup("tax", 100)
            self.currentPlayer.balance -= 100

        elif current_place.getName() == "Go To Jail":
            self.currentPlayer.inJail = True
            self.currentPlayer.position = 10
            self.popup("go to jail")
            self.board.updatePlayer(self.currentPlayer)

        if self.currentPlayer.position == 10:  # jail
            info = (self.currentPlayer.inJail, self.currentPlayer.turnsInJail)
            self.board.updateInfo("event", current_place, info)
        else:
            self.board.updateInfo("event", current_place)

        self.checkEndGame()

    def buy(self):
        current_place = self.board.places[self.currentPlayer.position]
        if current_place.type == "property":
            prop = self.board.getProperty(current_place.getName())
            self.currentPlayer.addProperty(prop)
            current_place.owner = self.currentPlayer

            self.board.updateInfo("event", current_place)
            self.board.buy_button.config(state="disabled")
            self.board.displayPlayerInfo(self.currentPlayer)
        else:
            if current_place.type == "station":
                self.currentPlayer.addStation(current_place)
                current_place.owner = self.currentPlayer
            else:
                self.currentPlayer.addUtility(current_place)
                current_place.owner = self.currentPlayer

            self.board.updateInfo("event", current_place)
            # prevents the same place being bought more than once
            self.board.buy_button.config(state="disabled")
            self.board.displayPlayerInfo(self.currentPlayer)
        self.checkEndGame()

    def buildHouse(self):
        prop = self.board.current_property
        prop.noOfHouses += 1
        self.board.drawHouses(prop)  # displays houses on the board
        if prop.noOfHouses == 5:
            self.board.build_house.config(state="disabled")
        self.currentPlayer.balance -= prop.costOfHouse
        self.board.displayPlayerInfo(self.currentPlayer)
        self.board.sell_house.config(state="normal")

        self.checkEndGame()

    def sellHouse(self):
        prop = self.board.current_property
        prop.noOfHouses -= 1
        self.board.drawHouses(prop)  # displays houses on the board
        if prop.noOfHouses == 0:
            self.board.sell_house.config(state="disabled")
        self.currentPlayer.balance += prop.costOfHouse
        self.board.displayPlayerInfo(self.currentPlayer)
        self.board.build_house.config(state="normal")

    def sellProperty(self, place=None):
        if not place:
            place = self.board.current_place
        if place.type == "property":
            prop = self.board.getProperty(place.getName())
            self.currentPlayer.sellProperty(prop)
            self.board.displayPlayerInfo(self.currentPlayer)
            self.board.drawHouses(prop)
            self.board.updateInfo("event", prop)

            # the other properties of the same colour
            for prop in self.board.properties[prop.colour]:
                prop.isMonopoly = False
            prop.owner = None

        elif place.type == "station":
            self.currentPlayer.sellStation(place)
        elif place.type == "utility":
            self.currentPlayer.sellUtility(place)

        place.owner = None

        self.board.displayPlayerInfo(self.currentPlayer)
        self.board.updateInfo("event", place)

        self.board.sell_property.config(state="disabled")
        self.board.build_house.config(state="disabled")
        self.board.sell_house.config(state="disabled")

    def endTurn(self):
        self.currentPlayer = self.getOtherPlayer()
        self.board.displayPlayerOptions(self.currentPlayer, self.die1, self.die2, self)
        if not self.currentPlayer.inJail:
            self.board.roll_button.config(state="normal")
        else:
            self.makeTurn()

    def Jail(self):
        self.currentPlayer.turnsInJail += 1
        current_place = self.board.places[self.currentPlayer.position]
        info = (self.currentPlayer.inJail, self.currentPlayer.turnsInJail)
        self.board.updateInfo("event", current_place, info)

        if self.currentPlayer.turnsInJail == 3:
            tkinter.messagebox.showinfo(
                "Jail", "You have been in jail for 3 turns. Roll to move out of jail"
            )
            self.currentPlayer.inJail = False
            self.currentPlayer.turnsInJail = 0
            self.board.updatePlayer(self.currentPlayer)
            self.board.roll_button.config(state="normal")

        elif (
            tkinter.messagebox.askquestion(
                "You are in Jail", "Would you like to pay £50 to get out of jail?"
            )
            == "yes"
        ):
            self.currentPlayer.turnsInJail = 0
            self.currentPlayer.inJail = False
            self.currentPlayer.balance -= 50
            self.board.displayPlayerInfo(self.currentPlayer)
            self.board.updatePlayer(self.currentPlayer)
            self.board.roll_button.config(state="normal")

        else:
            self.die1 = random.randint(1, 6)
            self.die2 = random.randint(1, 6)
            self.board.displayPlayerOptions(
                self.currentPlayer, self.die1, self.die2, self
            )  # refresh dice display
            self.board.flashDiceBox()

            if self.die1 == self.die2:
                self.currentPlayer.turnsInJail = 0
                self.currentPlayer.inJail = False
                tkinter.messagebox.showinfo(
                    "Well done!",
                    "You rolled a double so you are now out of jail!\nRoll to move",
                )
                self.board.updatePlayer(self.currentPlayer)
                self.board.roll_button.config(state="normal")

        self.board.end_turn.config(state="normal")

    def getOtherPlayer(self):
        if self.currentPlayer.number == 1:
            return self.player2
        else:
            return self.player1

    def initialiseChances(self):
        self.chances = []
        with open("chances.csv", encoding="utf8") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            for line in csvreader:
                self.chances.append(line)

    def getChance(self):
        chance = random.choice(self.chances)
        return chance

    def Chance(self):
        chance = self.getChance()
        place = self.board.places[self.currentPlayer.position]
        tkinter.messagebox.showinfo(place.getName(), message=chance[0])
        if chance[1] == "move":
            place = int(chance[2])
            if place == 10:  # jail
                self.currentPlayer.inJail = True
            self.currentPlayer.position = place
        elif chance[1] == "pay":
            self.currentPlayer.balance -= int(chance[2])
        elif chance[1] == "get":
            self.currentPlayer.balance += int(chance[2])
        elif chance[1] == "transfer":
            self.currentPlayer.balance += int(chance[2])
            self.getOtherPlayer().balance -= int(chance[2])

    def popup(self, popup_type, info=None):

        if popup_type == "rent":
            current_place = info
            if current_place.type == "property":
                rent = self.board.getProperty(current_place.getName()).getRent()
            else:
                rent = current_place.getRent(self.die1 + self.die2)
            tkinter.messagebox.showinfo(
                "Pay Rent!",
                message="You have landed on {} which is owned by Player {}.\nYou have to pay £{}".format(
                    current_place.info[0], current_place.owner.number, rent
                ),
            )

        elif popup_type == "tax":
            tkinter.messagebox.showinfo("Tax", message="Pay £{}".format(info))

        elif popup_type == "go":
            tkinter.messagebox.showinfo(
                "GO", message="Collect £{} for passing GO!".format(info)
            )

        elif popup_type == "double":
            tkinter.messagebox.showinfo(
                "Double", message="You have rolled a double so you get one more roll!"
            )

        elif popup_type == "three doubles":
            tkinter.messagebox.showwarning(
                "Jail", message="You rolled 3 doubles in a row. Go to jail!"
            )
            info = (self.currentPlayer.inJail, self.currentPlayer.turnsInJail)
            self.board.updateInfo("event", self.board.getPlace("Jail"), info)

        elif popup_type == "go to jail":
            tkinter.messagebox.showwarning("Jail", message="Go to Jail!")
            info = (self.currentPlayer.inJail, self.currentPlayer.turnsInJail)
            self.board.updateInfo("event", self.board.getPlace("Jail"), info)

    def checkEndGame(self):
        if self.currentPlayer.balance <= 0:
            self.board.roll_button.config(state="disabled")
            self.board.end_turn.config(state="disabled")
            tkinter.messagebox.showwarning(
                "Bankrupt!",
                "Your balance has gone below £0! Some properties will be automatically sold.",
            )

            # if the player is in debt, the player's utilities are automatically sold to make some money
            sold_properties = []

            for i in range(len(self.currentPlayer.utilities_owned)):
                if self.currentPlayer.balance > 0:
                    break
                utility = self.currentPlayer.utilities_owned[i]
                self.sellProperty(utility)
                sold_properties.append(utility.getName())

            # if the player's balance is still less than 0, their stations are automatically sold.
            if self.currentPlayer.balance <= 0:
                for i in range(len(self.currentPlayer.stations_owned)):
                    if self.currentPlayer.balance > 0:
                        break
                    station = self.currentPlayer.stations_owned[i]
                    self.sellProperty(station)
                    sold_properties.append(station.getName())

            # if the player's balance is still less than 0, their properties are automatically sold.
            if self.currentPlayer.balance <= 0:
                properties = self.currentPlayer.properties_owned
                for _ in range(len(properties)):
                    if self.currentPlayer.balance > 0:
                        break
                    prop = self.board.getPlace(properties[-1].getName())
                    self.sellProperty(prop)
                    sold_properties.append(prop.getName())

            # if properties were sold:
            if sold_properties:
                tkinter.messagebox.showinfo(
                    "Bankrupt",
                    "The following properties were automatically sold:\n{}".format(
                        ", ".join(sold_properties)
                    ),
                )
            else:
                tkinter.messagebox.showinfo(
                    "Bankrupt",
                    "Player {} has no properties to sell!".format(
                        self.currentPlayer.number
                    ),
                )

            # if the player's balance is still less than 0, the game is over
            if self.currentPlayer.balance <= 0:
                tkinter.messagebox.showwarning(
                    "Game Over!",
                    "Player {} has gone bankrupt!".format(self.currentPlayer.number),
                )
                tkinter.messagebox.showinfo(
                    "Player {} Wins!".format(self.getOtherPlayer().number),
                    "Well done Player {}! You win!".format(
                        self.getOtherPlayer().number
                    ),
                )
                self.endGame()
            else:
                self.board.end_turn.config(state="normal")

    def endGame(self):
        self.parent.destroy()
