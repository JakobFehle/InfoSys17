#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import tkMessageBox
from PIL import ImageTk
import outfitRecommender


class OutfitRecommenderGUI(tk.Frame):
    buttonBackground = "#000000"
    fieldWidth = 25
    # used for dynamically accessing the four cloth lists
    filenamePrefixes = ["data/top/", "data/jacket/", "data/trousers/", "data/shoes/"]
    clothNames = ['top', 'jacket', 'trousers', 'shoes']
    buttonImages = {}

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initializing the buttons representing the cloth pieces
        for j in range(len(outfitRecommender.filenames)):
            for k in range(len(outfitRecommender.filenames[j])):
                print (outfitRecommender.filenames)
                self.buttonImages[(j, k)] = ImageTk.PhotoImage(
                    file=self.filenamePrefixes[j] + outfitRecommender.filenames[j][k])

        # The first four cloth pieces to be shown // buttons need to safe the path to the image for correct behaviour
        self.startScreenButtons = [self.buttonImages[(0, 0)], self.buttonImages[(1, 0)], self.buttonImages[(2, 0)],
                                   self.buttonImages[(3, 0)]]

        # list for saving selected Outfit // unnecessary when the planed structure works out
        self.selectedPieces = []

        # counts the number of pieces selected by the user // terminate the app when the last piece is selected
        self.piecesSelected = 0  # ?

        # overrides the behaviour of the X-button, the user now has to confirm the closing of the application
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

        # contains every button shown in the frame
        self.buttons = {}

        self.__initUI__()

    # sets up the window and its menu-bar
    def __initUI__(self):
        # size of a 720p display
        self.root.minsize(width=1366, height=768)
        self.root.title("Outfit-Recommender")

        menu_main = tk.Menu(self.root)
        menu_file = tk.Menu(menu_main, tearoff=0)

        # menu entry: new recommendation
        menu_file.add_command(label="New Recommendation", underline=0, accelerator="Ctrl+N",
                              command=lambda: self.new_recommendation(4, 1))
        self.root.bind_all("<Control-n>", lambda event: self.new_recommendation(4, 1))

        # menu entry: quit recommender
        menu_file.add_command(label="Quit", underline=0, accelerator="Ctrl+Q", command=lambda: self.on_quit())
        self.root.bind_all("<Control-q>", lambda event: self.on_quit())

        menu_help = tk.Menu(menu_main, tearoff=0)
        menu_help.add_command(label="About", underline=0, command=lambda: tkMessageBox.showinfo("Outfit-Recommender",
                                                                                                "Informationssysteme SS17\nInformationswissenschaft\nUni Regensburg"))
        menu_main.add_cascade(label="Options", underline=0, menu=menu_file)
        menu_main.add_cascade(label="Help", underline=0, menu=menu_help)

        self.root.config(menu=menu_main)

    def new_recommendation(self, row, col):
        # clears the frame without destroying the frame itself:
        # http://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
        for widget in self.winfo_children():
            widget.destroy()

        self.buttons.clear()
        self.__resize__(col * self.fieldWidth, row * self.fieldWidth)
        self.init_grid(row, col)

    # private function for window resizing // can only increase size?! -> needs testing?/doesnt matter?
    def __resize__(self, width, height):
        root.geometry('{}x{}'.format(width, height))

    # initializes grid UI and fills it with the cloth-buttons
    def init_grid(self, row, col):
        for j in range(row):
            for k in range(col):
                self.buttons[(j, k)] = tk.Button(self, width=160, height=160, image=self.startScreenButtons[j],
                                                 state="normal")
                b = self.buttons[(j, k)]
                b.grid(row=j, column=k, padx=(10, 10), pady=(10, 10))
                # Left-Click
                b.bind('<Button-1>', lambda event, x=j, y=k: self.show_all(x))

        self.pack()

    # needs to remove all buttons currently in the frame
    def show_all(self, cloth_name_index):
        for k in range(len(outfitRecommender.filenames[cloth_name_index])):
            self.buttons[(cloth_name_index, k)] = tk.Button(self, width=160, height=160,
                                                            image=self.buttonImages[(cloth_name_index, k)],
                                                            state="normal")
            b = self.buttons[(cloth_name_index, k)]
            b.grid(row=cloth_name_index, column=k, padx=(10, 10), pady=(10, 10))
            # Left-Click
            b.bind('<Button-1>', lambda event, x=cloth_name_index, y=k: self.show_recommendations(x, y))

        self.pack()

    def show_recommendations(self, r, c):
        if r != 3:
            next_cloth = outfitRecommender.getNextCloth(self.clothNames[r], outfitRecommender.filenames[r][c],
                                                        self.clothNames[r + 1])
            r = r + 1
        else:
            next_cloth = outfitRecommender.getNextCloth(self.clothNames[r], outfitRecommender.filenames[r][c],
                                                        self.clothNames[0])
            r = 0
        print (next_cloth)
        for k in range(len(next_cloth)):
            self.buttons[(r, k)] = tk.Button(self, width=160, height=160,
                                             image=ImageTk.PhotoImage(
                                                 file=self.filenamePrefixes[r] + next_cloth[k][0]),
                                             state="normal")
            b = self.buttons[(r, k)]
            b.grid(row=r, column=k, padx=(10, 10), pady=(10, 10))
            # Left-Click
            b.bind('<Button-1>', lambda event, x=r, y=k: self.show_recommendations(x, y))

        self.pack()

    def on_quit(self):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            root.destroy()


root = tk.Tk()
mainWindow = OutfitRecommenderGUI(root)
mainWindow.mainloop()
