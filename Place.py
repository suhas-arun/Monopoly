import tkinter
import csv
places = []


class Place:
    # coords store the coordinates of the centre of the place on the board so that the players can move to the place easily
    def __init__(self, typeOfPlace, info, coords):
        self.type = typeOfPlace
        self.info = info
        self.coords = coords
        self.owner = None

    def getInfo(self):
        return (self.type, self.info, self.owner)

    def getPosition(self):
        return self.coords

    def getPrice(self):
        return int(self.info[1])

    def getName(self):
        return self.info[0]

    def getRent(self, dice_total):
        if self.owner is None:  # if unowned
            return

        if self.type == "station":
            noOfStations = len(self.owner.stations_owned)
            if noOfStations == 1:
                return 25
            elif noOfStations == 2:
                return 50
            elif noOfStations == 3:
                return 100
            else:
                return 200

        if self.type == "utility":
            if len(self.owner.utilities_owned) == 2:
                return 10 * dice_total
            else:
                return 4 * dice_total


class Property(Place):
    def __init__(self, Place):
        self.info = Place.info
        self.type = ""
        self.owner = Place.owner
        self.coords = Place.coords
        self.name = self.info[0]
        self.colour = self.info[1]
        self.price = int(self.info[2])
        self.rent = self.info[3:9]
        self.costOfHouse = int(self.info[9])
        self.isMonopoly = False
        self.noOfHouses = 0

    def getRent(self):
        rent = self.rent[self.getNoOfHouses()]
        if self.isMonopoly and self.getNoOfHouses() == 0:
            rent = rent
        return rent

    def getNoOfHouses(self):
        return self.noOfHouses

    def addHouse(self):
        self.noOfHouses += 1


properties: dict = {}

with open("places.csv") as csvfile:
    f = csv.reader(csvfile, delimiter=",")
    for place in f:
        place[-1] = place[-1].rstrip("\n")  # strips newline char
        typeOfPlace = place[0]

        if typeOfPlace == "property":
            info = place[1:11]
            coords = place[11:13]
            new_place = Place(typeOfPlace, info, coords)
            new_property = Property(new_place)
            colour = info[1]
            # making a dictionary of properties, grouped by colour
            if colour in properties.keys():
                properties[colour].append(
                    Property(Place(typeOfPlace, info, coords)))
            else:
                properties[colour] = [
                    Property(Place(typeOfPlace, info, coords))]

        elif typeOfPlace in ["station", "utility"]:
            info = place[1:3]
            coords = place[3:5]

        else:
            info = place[1:2]
            coords = place[2:4]
        # makes a list of all the place objects
        places.append(Place(typeOfPlace, info, coords))
