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
        self.player1.label = tkinter.Label(self.parent, width=2, height=1, text=str(
            self.player1.number), bg=self.player1.colour, fg="white")
        self.player2.label = tkinter.Label(self.parent, width=2, height=1, text=str(
            self.player2.number), bg=self.player2.colour, fg="white")
        self.currentPlayer = self.player1
        self.die1 = "..."
        self.die2 = "..."

    def setupGame(self):
        self.board.drawBoard()
        self.board.drawPlayer(self.player1)
        self.board.drawPlayer(self.player2)

        self.board.displayPlayerInfo(self.player1)
        self.board.displayPlayerInfo(self.player2)

        self.board.displayPlayerOptions(
            self.currentPlayer, self.die1, self.die2, self)

        self.initialiseChances()

    def Game(self):
        self.board.roll_button.config(state="normal")

    def makeTurn(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.board.displayPlayerOptions(
            self.currentPlayer, self.die1, self.die2, self)  # refresh dice display
        # prevents the player from rolling again
        self.board.roll_button.config(state="disabled")
        total = self.die1 + self.die2

        if self.die1 != self.die2:  # if the player doesn't roll a double...
            self.move(total)
            self.noOfDoubles = 0
        else:
            self.currentPlayer.noOfDoubles += 1
            if self.currentPlayer.noOfDoubles == 3:
                self.currentPlayer.inJail = True
                self.popup("three doubles")
                self.currentPlayer.position = 10
                self.board.updatePlayer(self.currentPlayer)
            else:
                self.move(total)
                self.popup("double")
                # lets the player roll again
                self.board.roll_button.config(state="normal")

        self.board.displayPlayerInfo(self.currentPlayer)

        self.board.end_turn.config(state="normal")

    def move(self, total):
        self.currentPlayer.position += total  # moves player
        if self.currentPlayer.position > 39:  # checks if the player has passed GO
            self.currentPlayer.balance += 200  # get £200 for passing GO
            self.currentPlayer.position -= 39
            self.popup("go", 200)
        self.board.updatePlayer(self.currentPlayer)
        self.board.displayPlayerInfo(self.currentPlayer)
        current_place = self.board.places[self.currentPlayer.position]

        if current_place.type in ["property", "utility", "station"]:
            self.board.updateInfo("bruh", current_place)
            if current_place.owner == 0:  # if unowned, allow player to buy
                self.board.buy_button.config(state="normal")

            elif current_place.owner == self.getOtherPlayer():
                # pay rent
                self.popup("rent", current_place)
                otherPlayer = self.getOtherPlayer()
                self.currentPlayer.payRent(
                    current_place.getRent(total), otherPlayer)
                # updates the other player's on screen balance
                self.board.displayPlayerInfo(self.getOtherPlayer())

        elif current_place.type == "chance":
            chance = self.getChance()
            self.Chance()
            self.board.updatePlayer(self.currentPlayer)
            # updates the other player's on screen balance
            self.board.displayPlayerInfo(self.getOtherPlayer())

        elif current_place.type == "tax":
            self.popup("tax", 100)
            self.currentPlayer.balance -= 100

        self.board.updateInfo("bruh", current_place)

    def buy(self):
        current_place = self.board.places[self.currentPlayer.position]
        if current_place.type == "property":
            self.currentPlayer.addProperty(
                self.board.getProperty(current_place.getName()))
            current_place.owner = self.currentPlayer
        elif current_place.type == "station":
            self.currentPlayer.addStation(current_place)
            current_place.owner = self.currentPlayer
        else:
            self.currentPlayer.addUtility(current_place)
            current_place.owner = self.currentPlayer

        self.board.updateInfo("bruh", current_place)
        self.board.buy_button.config(state="disabled")
        self.board.displayPlayerInfo(self.currentPlayer)

    def buildHouse(self):
        return
        # check if property is part of a monopoly then build house

    def sellHouse(self):
        return

    def sellProperty(self):
        return

    def endTurn(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

        self.board.displayPlayerOptions(
            self.currentPlayer, self.die1, self.die2, self)
        self.board.roll_button.config(state="normal")

    def getOtherPlayer(self):
        if self.currentPlayer.number == 1:
            return self.player2
        else:
            return self.player1

    def initialiseChances(self):
        self.chances = []
        # I needed to use the csv module to change the encoding to UTF-8 as the £ sign was not showing up properly on the tkinter messagebox
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
        # print(self.currentPlayer.balance)
        if chance[1] == "move":
            self.currentPlayer.position = int(chance[2])
        elif chance[1] == "pay":
            self.currentPlayer.balance -= int(chance[2])
        elif chance[1] == "get":
            self.currentPlayer.balance += int(chance[2])
        elif chance[1] == "transfer":
            self.currentPlayer.balance += int(chance[2])
            self.getOtherPlayer().balance -= int(chance[2])

    def popup(self, popup_type, info=None):
        if popup_type == "rent":
            tkinter.messagebox.showinfo("Pay Rent!", message="You have landed on {} which is owned by Player {}.\nYou have to pay £{}".format(
                info.info[0], info.owner.number, info.getRent(self.die1+self.die2)))
        
        elif popup_type == "tax":
            tkinter.messagebox.showinfo("Tax", message="Pay £{}".format(info))
        
        elif popup_type == "go":
            tkinter.messagebox.showinfo(
                "GO", message="Collect £{} for passing GO!".format(info))

        elif popup_type == "double":
            tkinter.messagebox.showinfo(
                "Double", message="You have rolled a double so you get one more roll!")
            
        elif popup_type == "three doubles":
            tkinter.messagebox.showwarning("Jail",message="You rolled 3 doubles in a row. Go to jail!")
