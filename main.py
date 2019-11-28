# work on ending the game

import tkinter
import Place
import Board
import Player
import Game

window = tkinter.Tk()
window.title("Monopoly")
WIDTH = 1280
HEIGHT = 675
# sets the window to 1280x675
window.geometry("{}x{}".format(str(WIDTH), str(HEIGHT)))

canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT, bg="#ccffcc")

places = Place.places
properties = Place.properties

board = Board.Board(window, canvas, places, properties)

player1 = Player.Player(1, "red")
player2 = Player.Player(2, "blue")

Monopoly = Game.Game(window, board, player1, player2)
Monopoly.setupGame()
board.roll_button.config(state="normal")

window.mainloop()
