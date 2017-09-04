#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import tkMessageBox
from PIL import ImageTk
import outfitRecommender


class OutfitRecommenderGUI(tk.Frame):
    buttonBackground = "#000000"
    fieldWidth = 25

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        # Initializing the buttons for the start-screen
        self.topButton = ImageTk.PhotoImage(file="data/top/" + outfitRecommender.filenamesTop[0])
        self.jacketButton = ImageTk.PhotoImage(file="data/jacket/" + outfitRecommender.filenamesJacket[0])
        self.trouserButton = ImageTk.PhotoImage(file="data/trousers/" + outfitRecommender.filenamesTrousers[0])
        self.shoeButton = ImageTk.PhotoImage(file="data/shoes/" + outfitRecommender.filenamesShoes[0])

        self.startScreenButtons = [self.topButton, self.jacketButton, self.trouserButton, self.shoeButton]

        # list for saving selected Outfit // unnecessary when the planed structure works out
        self.selectedPieces = []

        # overrides the behaviour of the X-button, the user now has to confirm the closing of the application
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

        # counts the number of pieces selected by the user (used to go for the right row and terminate the app)
        self.piecesSelected = 0  # ?

        # contains every button shown in the frame
        self.buttons = {}

        self.__initUI__()

    # setting up the menu-bar
    def __initUI__(self):
        # size of a 720p display
        self.root.minsize(width=1366, height=768)
        self.root.title("Outfit-Recommender")

        menu_main = tk.Menu(self.root)
        menu_file = tk.Menu(menu_main, tearoff=0)

        # menu entry: new recommendation
        menu_file.add_command(label="New Recommendation", underline=0, accelerator="Ctrl+N",
                              command=lambda: self.new_game(4, 1, 10))
        self.root.bind_all("<Control-n>", lambda event: self.new_game(4, 1, 10))  # ?

        # menu entry: quit recommender
        menu_file.add_command(label="Quit", underline=0, accelerator="Ctrl+Q", command=lambda: self.on_quit())
        self.root.bind_all("<Control-q>", lambda event: self.on_quit())

        menu_help = tk.Menu(menu_main, tearoff=0)
        menu_help.add_command(label="About", underline=0, command=lambda: tkMessageBox.showinfo("Outfit-Recommender",
                                                                                                "Informationssysteme SS17\nInformationswissenschaft\nUni Regensburg"))
        menu_main.add_cascade(label="Options", underline=0, menu=menu_file)
        menu_main.add_cascade(label="Help", underline=0, menu=menu_help)

        self.root.config(menu=menu_main)

    def new_game(self, r, c, mines):  # rows, columns
        # http://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
        for widget in self.winfo_children():
            widget.destroy()

        self.buttons.clear()
        self.__resize__(c * self.fieldWidth, r * self.fieldWidth)
        self.init_grid(r, c)

    # private function for window resizing
    def __resize__(self, width, height):
        root.geometry('{}x{}'.format(width, height))

    # initializes grid UI
    def init_grid(self, r, c):  # rows, columns
        # fills the grid with buttons
        for j in range(r):
            for k in range(c):
                self.buttons[(j, k)] = tk.Button(self, width=160, height=160, image=self.startScreenButtons[j],
                                                 state="normal")
                b = self.buttons[(j, k)]
                # b.image = self.startScreenButtons[0]
                b.grid(row=j, column=k, padx=(10, 10), pady=(10, 10))
                # b.bind('<Button-1>', lambda event, x=j, y=k: self.changeToLabel(x, y))  # Left-Click
                # b.bind('<Button-3>', lambda event, x=j, y=k: self.flagForMine(x, y))  # Right-Click

        self.pack()

    def on_quit(self):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            root.destroy()

            # def restart_recommender(self):
            #    if tkMessageBox.askokcancel("Game Over", "You clicked a mine!"):
            #        self.__init__(root)


root = tk.Tk()
mainWindow = OutfitRecommenderGUI(root)
mainWindow.mainloop()
