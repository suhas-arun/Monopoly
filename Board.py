import tkinter

class Board:
    def __init__(self, parent, canvas, places, properties):
        self.places = places
        self.parent = parent
        self.properties = properties
        self.canvas = canvas
        self.default_colour = self.parent.cget("bg")
        self.background_colour = "#ccffcc"

    def getProperty(self, name):
        for properties in self.properties.values():
            for property in properties:
                if property.getName() == name:
                    return property

    def getPlace(self,name):
        for place in self.places:
            if place.getName() == name:
                return place

    def drawPlayer(self, player):
        player_label = player.label
        player_label.lift()
        player_position = self.places[player.position].getPosition()
        player_position_x, player_position_y = player_position[0], player_position[1]
        player_label.place(x=player_position_x,
                           y=player_position_y, anchor="center")

    def updatePlayer(self, player):
        # removes previous player label from the screen (otherwise the player is in multiple places at once)
        player.label.destroy()
        player.label = tkinter.Label(self.parent, width=2, height=1, text=str(
            player.number), bg=player.colour, fg="white")
        new_player_label = player.label
        if player.position == 10 and player.inJail: #jail:
            player_position_x, player_position_y, = 50, 615
        else:
            player_position = self.places[player.position].getPosition()
            player_position_x, player_position_y = player_position[0], player_position[1]
        new_player_label.place(x=player_position_x,
                               y=player_position_y, anchor="center")

    def drawBoard(self):
        self.canvas.place(x=0, y=0)
        # shows the title
        title_label = tkinter.Label(
            text="MONOPOLY", bg="red", fg="white", font=("Helvetica", 40))
        title_label.place(x=327.5, y=180, anchor="center")

        # draw info box
        self.canvas.create_rectangle(
            227.5, 275, 427.5, 525, width=5, fill=self.default_colour)
        self.place_name_label = tkinter.Label(text="WELCOME TO\n MONOPOLY!", font=(
            "Helvetica", 14), bg=self.default_colour)
        self.place_name_label.place(x=327.5, y=320, anchor="center")

        self.info_label = tkinter.Label(text="Press Roll to start the game.", font=(
            "Helvetica", 10), bg=self.default_colour)
        self.info_label.place(x=327.5, y=400, anchor="center")

        self.owner_label = tkinter.Label(font=("Helvetica", 10, "bold"))

        # top row
        for i in range(9):
            place = self.places[21+i]
            if place.type == "property":
                place_frame = tkinter.Frame(
                    self.parent, width=54, height=69)
                place_frame.place(x=81 + 55*i, y=0)
                self.canvas.create_rectangle(80 + 55*i, 0, 80+55*(i+1), 80)
                self.canvas.create_rectangle(
                    80+55*i, 70, 80+55*(i+1), 80, fill=place.info[1])

                price_label = tkinter.Label(place_frame, text="£{}".format(
                    place.info[2]), font=("Helvetica", 8))
                price_label.place(x=27, y=10, anchor="center")
                info_button = tkinter.Button(place_frame, text="\n".join(
                    place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                info_button.place(x=27, y=40, anchor="center")
                info_button.bind("<Button-1>", lambda event,
                                 current_place=place: self.updateInfo(event, current_place))

            else:
                place_frame = tkinter.Frame(
                    self.parent, width=54, height=79)
                place_frame.place(x=81 + 55*i, y=0)
                self.canvas.create_rectangle(80 + 55*i, 0, 80+55*(i+1), 80)

                if place.type in ["utility", "station"]:
                    info_button = tkinter.Button(place_frame, text="\n".join(
                        place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                    info_button.place(x=27, y=40, anchor="center")
                    info_button.bind(
                        "<Button-1>", lambda event, current_place=place: self.updateInfo(event, current_place))

                    price_label = tkinter.Label(place_frame, text="£{}".format(
                        place.info[1]), font=("Helvetica", 8))
                    price_label.place(x=27, y=10, anchor="center")

                else:
                    tkinter.Label(place_frame, text="\n".join(place.getName().upper().split()), font=(
                        "Helvetica", 6)).place(x=27, y=40, anchor="center")

        # left column
        for i in range(9):
            place = self.places[19-i]
            if place.type == "property":
                place_frame = tkinter.Frame(
                    self.parent, width=69, height=54)
                place_frame.place(y=81 + 55*i, x=0)
                self.canvas.create_rectangle(0, 80 + 55*i, 80, 90+55*(i+1))
                self.canvas.create_rectangle(
                    70, 80+55*i, 80, 80+55*(i+1), fill=place.info[1])

                price_label = tkinter.Label(place_frame, text="£{}".format(
                    place.info[2]), font=("Helvetica", 8))
                price_label.place(x=35, y=45, anchor="center")

                info_button = tkinter.Button(place_frame, text="\n".join(
                    place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                info_button.place(x=35, y=27, anchor="center")
                info_button.bind("<Button-1>", lambda event,
                                 current_place=place: self.updateInfo(event, current_place))

            else:
                place_frame = tkinter.Frame(
                    self.parent, width=79, height=54)
                place_frame.place(y=81 + 55*i, x=0)
                self.canvas.create_rectangle(0, 80 + 55*i, 80, 90+55*(i+1))

                if place.type in ["utility", "station"]:
                    info_button = tkinter.Button(place_frame, text="\n".join(
                        place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                    info_button.place(x=35, y=27, anchor="center")
                    info_button.bind(
                        "<Button-1>", lambda event, current_place=place: self.updateInfo(event, current_place))

                    price_label = tkinter.Label(place_frame, text="£{}".format(
                        place.info[1]), font=("Helvetica", 8))
                    price_label.place(x=35, y=45, anchor="center")
                else:
                    tkinter.Label(place_frame, text="\n".join(place.getName().upper().split()), font=(
                        "Helvetica", 6)).place(x=40, y=27, anchor="center")

        # bottom row
        for i in range(9):
            place = self.places[9-i]
            if place.type == "property":
                place_frame = tkinter.Frame(
                    self.parent, width=54, height=69)
                place_frame.place(x=81 + 55*i, y=586)
                self.canvas.create_rectangle(80 + 55*i, 575, 80+55*(i+1), 655)
                self.canvas.create_rectangle(
                    80+55*i, 575, 80+55*(i+1), 585, fill=place.info[1])

                price_label = tkinter.Label(place_frame, text="£{}".format(
                    place.info[2]), font=("Helvetica", 8))
                price_label.place(x=27, y=60, anchor="center")

                info_button = tkinter.Button(place_frame, text="\n".join(
                    place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                info_button.place(x=27, y=35, anchor="center")
                info_button.bind("<Button-1>", lambda event,
                                 current_place=place: self.updateInfo(event, current_place))

            else:
                place_frame = tkinter.Frame(
                    self.parent, width=54, height=79)
                place_frame.place(x=81 + 55*i, y=576)
                self.canvas.create_rectangle(80 + 55*i, 575, 80+55*(i+1), 655)

                if place.type == "station":
                    info_button = tkinter.Button(place_frame, text="\n".join(
                        place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                    info_button.place(x=27, y=40, anchor="center")
                    info_button.bind(
                        "<Button-1>", lambda event, current_place=place: self.updateInfo(event, current_place))

                    price_label = tkinter.Label(
                        place_frame, text="£200", font=("Helvetica", 8))
                    price_label.place(x=27, y=70, anchor="center")
                else:
                    tkinter.Label(place_frame, text="\n".join(place.getName().upper().split()), font=(
                        "Helvetica", 6)).place(x=27, y=40, anchor="center")

        # right column
        for i in range(9):
            place = self.places[31+i]
            if place.type == "property":
                place_frame = tkinter.Frame(
                    self.parent, width=69, height=54)
                place_frame.place(y=81 + 55*i, x=586)
                self.canvas.create_rectangle(575, 80 + 55*i, 655, 80+55*(i+1))
                self.canvas.create_rectangle(
                    575, 80+55*i, 585, 80+55*(i+1), fill=place.info[1])
                price_label = tkinter.Label(place_frame, text="£{}".format(
                    place.info[2]), font=("Helvetica", 8))
                price_label.place(x=35, y=45, anchor="center")

                info_button = tkinter.Button(place_frame, text="\n".join(
                    place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                info_button.place(x=35, y=27, anchor="center")
                info_button.bind("<Button-1>", lambda event,
                                 current_place=place: self.updateInfo(event, current_place))

            else:
                place_frame = tkinter.Frame(
                    self.parent, width=79, height=54)
                place_frame.place(y=81 + 55*i, x=576)
                self.canvas.create_rectangle(575, 80 + 55*i, 655, 80+55*(i+1))

                if place.type == "station":
                    info_button = tkinter.Button(place_frame, text="\n".join(
                        place.getName().upper().split()), font=("Helvetica", 6), relief="flat")
                    info_button.place(x=40, y=20, anchor="center")
                    info_button.bind(
                        "<Button-1>", lambda event, current_place=place: self.updateInfo(event, current_place))

                    price_label = tkinter.Label(place_frame, text="£{}".format(
                        place.info[1]), font=("Helvetica", 8))
                    price_label.place(x=35, y=45, anchor="center")
                else:
                    tkinter.Label(place_frame, text="\n".join(place.getName().upper().split()), font=(
                        "Helvetica", 6)).place(x=40, y=27, anchor="center")


        # draws corner places
        corner1 = tkinter.Frame(self.parent, width=79,
                                height=79).place(x=0, y=0)  # top left corner
        self.canvas.create_rectangle(0, 0, 80, 80)
        tkinter.Label(corner1, text="\n".join(
            self.places[20].getName().upper().split())).place(x=40, y=40, anchor="center")

        corner2 = tkinter.Frame(self.parent, width=79,
                                height=79).place(x=576, y=0)  # top right corner
        self.canvas.create_rectangle(575, 0, 655, 80)
        tkinter.Label(corner2, text="GO TO\nJAIL").place(
            x=615, y=40, anchor="center")

        # bottom left corner
        self.canvas.create_rectangle(0, 575, 80, 655, fill=self.default_colour)
        tkinter.Label(text="\n".join(
            self.places[10].getName().upper().split())).place(x=50, y=605, anchor="center")
        self.canvas.create_line(20,575,20,635)
        self.canvas.create_line(20,635,80,635)
        tkinter.Label(text="J\nU\nS\nT",font=("Helvetica",8)).place(x=10,y=610,anchor="center")
        tkinter.Label(text="VISITING",font=("Helvetica",7)).place(x=50,y=645,anchor="center")

        corner4 = tkinter.Frame(
            self.parent, width=79, height=79).place(x=576, y=576)  # bottom right corner
        self.canvas.create_rectangle(575, 575, 655, 655)
        tkinter.Label(corner4, text=self.places[0].getName().upper(), font=("Helvetica", 32)).place(
            x=615, y=615, anchor="center")

    # updates info box in the middle of the board
    def updateInfo(self, ignore, place,jail_info=None):
        place_info = place.getInfo()
        place_type = place_info[0]
        info = place_info[1]
        owner = place_info[2]
        name = info[0]
        if place_type == "property":
            colour = info[1]
            self.canvas.create_rectangle(230, 277.5, 425, 322.5, fill=colour)
            self.place_name_label.config(
                text=name.upper(), font=("Helvetica", 10), bg=colour)
            self.place_name_label.place(x=327.5, y=300, anchor="center")
            price, rent0, rent1, rent2, rent3, rent4, rent5, cost_of_house = info[
                2], info[3], info[4], info[5], info[6], info[7], info[8], info[9]
            if owner == 0:
                self.info_label.config(text="Price: £{0}\nRent: £{1}\n\nWith 1 House: £{2}\nWith 2 Houses: £{3}\nWith 3 Houses: £{4}\nWith 4 Houses: £{5}\nWith Hotel: £{6}\n\nHouses cost £{7} each\nA Hotel costs £{7}".format(
                    price, rent0, rent1, rent2, rent3, rent4, rent5, cost_of_house), font=("Helvetica", 9))
                self.info_label.place(x=327.5, y=410, anchor="center")

        elif place_type == "station":
            self.canvas.create_rectangle(
                230, 277.5, 425, 322.5, fill=self.default_colour)
            self.place_name_label.config(text=name.upper(), font=(
                "Helvetica", 10), bg=self.default_colour)
            self.place_name_label.place(x=327.5, y=300, anchor="center")
            price = info[1]
            self.info_label.config(text="Price: £{0}\nRent: £25\n\nIf 2 stations are owned: £50\nIf 3 stations are owned: £100\nIf 4 stations are owned: £200".format(
                price), font=("Helvetica", 10))
            self.info_label.place(x=327.5, y=400, anchor="center")

        elif place_type == "utility":
            self.canvas.create_rectangle(
                230, 277.5, 425, 322.5, fill=self.default_colour)
            self.place_name_label.config(text=name.upper(), font=(
                "Helvetica", 10), bg=self.default_colour)
            self.place_name_label.place(x=327.5, y=300, anchor="center")
            price = info[1]
            self.info_label.config(text="Price: £{0}\n\nIf one \"Utility\" is owned,\nrent is 4 times amount\nshown on dice.\n\nIf both \"Utilities\" are owned,\nrent is 10 times amount\nshown on dice.".format(
                price), font=("Helvetica", 10))
            self.info_label.place(x=327.5, y=420, anchor="center")

        elif place_type == "jail":
            self.canvas.create_rectangle(
                230, 277.5, 425, 322.5, fill=self.default_colour)
            self.place_name_label.config(text="JAIL",font=("Helvetica",16),bg=self.default_colour)
            self.place_name_label.place(x=327.5, y=300, anchor="center")
            inJail, turnsInJail = jail_info
            if inJail:
                self.info_label.config(text="You have been in jail for\n{} turn(s).\n\nYou can leave jail by either:\n-Paying £50\n-Rolling a double\n-Waiting 3 turns".format(turnsInJail))
            else:
                self.info_label.config(text="Just Visiting",font=("Helvetica",12))

        owner = "Unowned" if place.owner == 0 else "Owned by Player " + \
            str(place.owner.number)
        self.owner_label.config(text=owner)
        if place.type in ["property", "utility", "station"]:
            self.owner_label.config(text=owner)
        else:
            self.owner_label.config(text="")
        self.owner_label.place(x=327.5, y=510, anchor="center")
        
    def displayPlayerInfo(self, player):
        player_frame = tkinter.Frame(
            self.parent, width=400, height=300, bg=self.background_colour, relief="ridge", bd=3)
        if player.number == 1:
            player_frame.place(x=680, y=25)
        else:
            player_frame.place(x=680, y=330)

        player_number_label = tkinter.Label(player_frame, text="Player {}:".format(
            str(player.number)), bg=self.background_colour, fg=player.colour, font=("Helvetica", 28, "bold"))
        player_number_label.place(x=20, y=5)

        balance_label = tkinter.Label(player_frame, text="Balance: £{}".format(
            player.balance), font=("Helvetica", 18), bg=self.background_colour)
        balance_label.place(x=190, y=15)

        properties_label = tkinter.Label(
            player_frame, text="Properties owned:", bg=self.background_colour)
        properties_label.place(x=25, y=60)

        # displays properties owned grouped by colour
        y_coord = 80
        for colour in self.properties.keys():
            props_of_colour = [
                prop for prop in player.properties_owned if prop.colour == colour]
            if colour == "yellow":  # yellow properties have a different background colour for visibility
                properties_info = tkinter.Label(player_frame, text="    ".join(
                    prop.getName() for prop in props_of_colour), fg=colour, bg="grey")
            else:
                properties_info = tkinter.Label(player_frame, text="    ".join(
                    prop.getName() for prop in props_of_colour), fg=colour, bg=self.background_colour)

            # checks if player has monopoly
            if len(self.properties[colour]) == len(props_of_colour):
                for prop in props_of_colour:
                    prop.isMonopoly = True

            # only displays the able if the label has text (so that there isn't a grey box where the yellow properties should be)
            if properties_info.cget("text"):
                properties_info.place(x=25, y=y_coord)
            y_coord += 20

        # displays stations owned without the word "station" so it fits
        stations_info = tkinter.Label(player_frame, text="    ".join(" ".join(station.getName().split()[
                                      :-1]) for station in player.stations_owned), bg=self.background_colour)
        stations_info.place(x=25, y=240)

        # displays utilities owned
        utilities_info = tkinter.Label(player_frame, text="    ".join(
            utility.getName() for utility in player.utilities_owned), bg=self.background_colour)
        utilities_info.place(x=25, y=260)

    def displayPlayerOptions(self, currentPlayer, die1, die2, game):
        # roll, buy, build house, sell house, sell property,end turn
        options_frame = tkinter.Frame(
            self.parent, width=194, height=675, bg=self.background_colour)
        options_frame.place(x=1086, y=0)

        currentplayer_label = tkinter.Label(options_frame, text="Player {}'s turn".format(
            currentPlayer.number), bg=self.background_colour, font=("Helvetica", 16, "bold"), fg=currentPlayer.colour)
        currentplayer_label.place(x=97, y=60, anchor="center")

        dice_total = die1 + die2
        self.dice_box = tkinter.Label(options_frame, text="Dice 1: {}\nDice2: {}\nTotal: {}".format(
            die1, die2, dice_total), bg="white", borderwidth=2, relief="raised", font=("Helvetica", 12), padx=8, pady=8, justify="left")
        self.dice_box.place(x=97, y=130, anchor="center")

        self.roll_button = tkinter.Button(options_frame, text="Roll", bg="white", font=(
            "Helvetica", 16, "bold"), state="disabled", command=game.makeTurn)
        self.roll_button.place(x=97, y=220, anchor="center")

        self.buy_button = tkinter.Button(options_frame, text="Buy", bg="white", font=(
            "Helvetica", 16, "bold"), state="disabled", command=game.buy)
        self.buy_button.place(x=97, y=280, anchor="center")

        self.build_house = tkinter.Button(options_frame, text="Build House", bg="white", font=(
            "Helvetica", 16, "bold"), state="disabled", command=game.buildHouse)
        self.build_house.place(x=97, y=340, anchor="center")

        self.sell_house = tkinter.Button(options_frame, text="Sell House", bg="white", font=(
            "Helvetica", 16, "bold"), state="disabled", command=game.sellHouse)
        self.sell_house.place(x=97, y=400, anchor="center")

        self.sell_property = tkinter.Button(options_frame, text="Sell Property", bg="white", font=(
            "Helvetica", 16, "bold"), state="disabled", command=game.sellProperty)
        self.sell_property.place(x=97, y=460, anchor="center")

        self.end_turn = tkinter.Button(options_frame, text="End Turn", bg="white", font=(
            "Helvetica", 18, "bold"), state="disabled", command=game.endTurn)
        self.end_turn.place(x=97, y=600, anchor="center")

    #when the dice are rolled, a border appears around the dice box to make it more obvious
    def flashDiceBox(self):
        self.dice_box.config(bd=5,font=("Helvetica",12,"bold"))
        self.parent.after(1000, lambda: self.dice_box.config(bd=2,font=("Helvetica",12,)))
        
