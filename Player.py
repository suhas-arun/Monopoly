import tkinter


class Player:
    def __init__(self, number, colour):
        self.number = number
        self.colour = colour
        self.position = 0
        self.noOfDoubles = 0
        self.properties_owned = []
        self.stations_owned = []
        self.utilities_owned = []
        self.inJail = False
        self.turnsInJail = 0
        self.balance = 1500
        self.label = None

    def payRent(self, rent, player):
        self.balance -= int(rent)
        player.balance += int(rent)

    def addProperty(self, property):
        self.properties_owned.append(property)
        self.balance -= int(property.price)

    def addStation(self, station):
        self.stations_owned.append(station)
        self.balance -= int(station.info[1])

    def addUtility(self, utility):
        self.utilities_owned.append(utility)
        self.balance -= int(utility.info[1])

    def sellProperty(self, property):
        self.properties_owned.remove(property)
        self.balance += int(property.price)
        self.balance += len(property.noOfHouses) * property.costOfHouse
        property.noOfHouses = 0
        property.isMonopoly = False