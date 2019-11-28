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
        if self.currentPlayer.inJail:
            self.Jail()
            return

        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        self.board.displayPlayerOptions(
            self.currentPlayer, self.die1, self.die2, self)  # refresh dice display
        self.board.flashDiceBox()
        # prevents the player from rolling again
        self.board.roll_button.config(state="disabled")
        total = self.die1 + self.die2

        if self.die1 != self.die2:  # if the player doesn't roll a double...
            self.move(total)
            self.currentPlayer.noOfDoubles = 0
        else:
            self.currentPlayer.noOfDoubles += 1
            if self.currentPlayer.noOfDoubles == 3:
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

        self.board.end_turn.config(state="normal")

    def move(self, total):
        if self.currentPlayer.inJail:
            return

        self.currentPlayer.position += total  # moves player
        if self.currentPlayer.position > 39:  # checks if the player has passed GO
            self.currentPlayer.balance += 200  # get £200 for passing GO
            self.currentPlayer.position -= 39
            self.board.updatePlayer(self.currentPlayer)
            self.popup("go", 200)

        self.board.updatePlayer(self.currentPlayer)
        self.board.displayPlayerInfo(self.currentPlayer)
        current_place = self.board.places[self.currentPlayer.position]

        if current_place.type in ["property", "utility", "station"]:
            self.board.updateInfo("event", current_place)
            if current_place.owner == 0:  # if unowned, allow player to buy
                self.board.buy_button.config(state="normal")

            elif current_place.owner == self.getOtherPlayer(): #if place is owned by the other player
                # pay rent
                self.popup("rent", current_place)
                otherPlayer = self.getOtherPlayer()
                self.currentPlayer.payRent(
                    current_place.getRent(total), otherPlayer)
                # updates the other player's on-screen balance
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

        elif current_place.getName() == "Go To Jail":
            self.currentPlayer.inJail = True
            self.currentPlayer.position = 10
            self.popup("go to jail")
            self.board.updatePlayer(self.currentPlayer)

        if self.currentPlayer.position == 10: #jail
            info = (self.currentPlayer.inJail,self.currentPlayer.turnsInJail) 
            self.board.updateInfo("event",current_place,info)
        else:
            self.board.updateInfo("event", current_place)

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

        self.board.updateInfo("event", current_place)
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
        self.currentPlayer = self.getOtherPlayer()
        self.board.displayPlayerOptions(
            self.currentPlayer, self.die1, self.die2, self)
        if not self.currentPlayer.inJail:
            self.board.roll_button.config(state="normal")
        else:
            self.makeTurn()

    def Jail(self):
        self.currentPlayer.turnsInJail += 1
        current_place = self.board.places[self.currentPlayer.position]
        info = (self.currentPlayer.inJail,self.currentPlayer.turnsInJail)
        self.board.updateInfo("event",current_place,info)

        if self.currentPlayer.turnsInJail == 3:
            tkinter.messagebox.showinfo("Jail","You have been in jail for 3 turns. Roll to move out of jail")
            self.currentPlayer.inJail = False
            self.currentPlayer.turnsInJail = 0
            self.board.updatePlayer(self.currentPlayer)
            self.board.roll_button.config(state="normal")
        elif tkinter.messagebox.askquestion("You are in Jail","Would you like to pay £50 to get out of jail?") == "yes":
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
                self.currentPlayer, self.die1, self.die2, self)  # refresh dice display
            self.board.flashDiceBox()
            
            
            if self.die1 == self.die2:
                self.currentPlayer.turnsInJail = 0
                self.currentPlayer.inJail = False
                tkinter.messagebox.showinfo("Well done!","You rolled a double so you are now out of jail!\nRoll to move")
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
            if place == 10: #jail
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
            info = (self.currentPlayer.inJail,self.currentPlayer.turnsInJail)
            self.board.updateInfo("event",self.board.getPlace("Jail"),info)


        elif popup_type == "go to jail":
            tkinter.messagebox.showwarning("Jail",message="Go to Jail!")
            info = (self.currentPlayer.inJail,self.currentPlayer.turnsInJail)
            self.board.updateInfo("event",self.board.getPlace("Jail"),info)

