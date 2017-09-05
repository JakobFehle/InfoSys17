#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import tkMessageBox
from PIL import Image, ImageTk
import outfitRecommender


class OutfitRecommenderGUI(tk.Frame):
    # sizes of GUI related elements
    windowSize = [1366, 768]
    buttonSize = 160

    # used for dynamically accessing the four cloth lists
    filenamePrefixes = ["data/top/", "data/jacket/", "data/trousers/", "data/shoes/"]
    clothNames = ['top', 'jacket', 'trousers', 'shoes']

    # used to save all the default button images
    buttonImages = {}

    # used to save the recommended images, they won't be shown otherwise
    recommendedImages = {}

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.grid(sticky='nsew')

        # Initializing the images representing the cloth pieces
        self.__initButtonImages__()

        # contains every button shown in the frame
        self.buttons = {}

        self.__initUI__()

    # Initializes the images representing the cloth pieces
    def __initButtonImages__(self):
        for j in range(len(outfitRecommender.filenames)):
            for k in range(len(outfitRecommender.filenames[j])):
                image_path_prefix = self.filenamePrefixes[j]
                image_path = outfitRecommender.filenames[j][k]
                original = Image.open(image_path_prefix + image_path)
                resized = original.resize((self.buttonSize, self.buttonSize), Image.ANTIALIAS)
                self.buttonImages[(j, k)] = [ImageTk.PhotoImage(resized), image_path_prefix, image_path]

        # The first four cloth pieces to be shown (representing the four different cloth types)
        # Is needed, because buttons need to save the path to the image for correct behaviour
        self.startScreenButtonImages = [self.buttonImages[(0, 0)], self.buttonImages[(1, 0)], self.buttonImages[(2, 0)],
                                        self.buttonImages[(3, 0)]]

    # Sets up the window and its menu-bar
    def __initUI__(self):
        # size of a 720p display
        self.root.minsize(width=self.windowSize[0], height=self.windowSize[1])
        self.root.title("Outfit-Recommender")

        # overrides the behaviour of the X-button, the user now has to confirm the closing of the application
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

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

    # Shows a short dialogue asking the user, if he really wants to quit the application and closes the app on approval
    def on_quit(self):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            root.destroy()

    # Resets the frame without destroying it
    def new_recommendation(self, row, col):
        self.remove_all()
        self.__resize__()
        self.__initSelected__()
        self.init_grid(row, col)

    # Clears the frame without destroying the frame itself:
    # http://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    def remove_all(self):
        for widget in self.winfo_children():
            widget.destroy()

        # removes all buttons from the list
        self.buttons.clear()

    # Private function for keeping the size of the window // will be obsolete when show_all uses multiple rows
    def __resize__(self):
        root.geometry('{}x{}'.format(self.windowSize[0], self.windowSize[1]))

    # Sets the initial values for selectedPieces and piecesSelected
    def __initSelected__(self):
        # list for saving selected Outfit
        self.selectedPieces = [0, 0, 0, 0]

        # counts the number of pieces selected by the user
        # used to observe if the user already selected four pieces (one of each type)
        self.piecesSelected = 0

    # Initializes grid UI and fills it with the start-buttons
    def init_grid(self, row, col):
        for j in range(row):
            for k in range(col):
                self.buttons[(j, k)] = tk.Button(self, width=self.buttonSize, height=self.buttonSize,
                                                 image=self.startScreenButtonImages[j][0],
                                                 state="normal")
                b = self.buttons[(j, k)]
                b.grid(row=j, column=k, padx=(10, 10), pady=(10, 10))
                # Left-Click
                b.bind('<Button-1>', lambda event, x=j, y=k: self.show_all(x))

    # Shows all cloth of the chosen type
    def show_all(self, type_index):
        self.remove_all()
        for col in range(len(outfitRecommender.filenames[type_index])):
            if col < 7:
                row_offset = 0
            elif col < 14:
                row_offset = 1
            elif col < 21:
                row_offset = 2
            button_row = type_index + row_offset
            button_col = col - (row_offset * 7)
            self.buttons[(button_row, button_col)] = tk.Button(self, width=self.buttonSize,
                                                               height=self.buttonSize,
                                                               image=self.buttonImages[
                                                                   (type_index, col)][0],
                                                               state="normal")
            b = self.buttons[(button_row, button_col)]
            b.grid(row=button_row, column=button_col, padx=(10, 10), pady=(10, 10))
            # Left-Click
            b.bind('<Button-1>', lambda event, x=type_index, y=col: self.show_recommendations(x, self.buttonImages[(
                x, y)]))

    # Shows the recommendations for the selected piece
    def show_recommendations(self, r, selected_piece):
        self.remove_all()
        self.selectedPieces[r] = selected_piece[0]
        self.show_selected_pieces()
        if self.piecesSelected < 3:
            self.piecesSelected += 1
            if r != 3:
                next_cloth = outfitRecommender.getNextCloth(self.clothNames[r], selected_piece[2],
                                                            self.clothNames[r + 1])
                r = r + 1
            else:
                next_cloth = outfitRecommender.getNextCloth(self.clothNames[r], selected_piece[2],
                                                            self.clothNames[0])
                r = 0
            print (next_cloth)
            for k in range(len(next_cloth)):
                image_path_prefix = self.filenamePrefixes[r]
                image_path = next_cloth[k][0]
                original = Image.open(image_path_prefix + image_path)
                resized = original.resize((self.buttonSize, self.buttonSize), Image.ANTIALIAS)
                self.recommendedImages[(r, k)] = [ImageTk.PhotoImage(resized), image_path_prefix, image_path]
                self.buttons[(r, k)] = tk.Button(self, width=self.buttonSize, height=self.buttonSize,
                                                 image=self.recommendedImages[(r, k)][0],
                                                 state="normal")
                b = self.buttons[(r, k)]
                b.grid(row=r, column=k, padx=(10, 10), pady=(10, 10))
                # Left-Click
                b.bind('<Button-1>',
                       lambda event, x=r, y=k: self.show_recommendations(x, self.recommendedImages[(x, y)]))
        else:
            self.__showOutfitFinishedDialogue__()

    # Shows the user a dialogue telling him/her that the outfit is complete
    def __showOutfitFinishedDialogue__(self):
        if tkMessageBox.askyesno("Outfit completed", "Your outfit is completed!\nDo you want to create another one?"):
            self.new_recommendation(4, 1)

    # Shows all the pieces selected by the user
    def show_selected_pieces(self):
        for row in range(len(self.selectedPieces)):
            if self.selectedPieces[row] != 0:
                self.buttons[(row, 0)] = tk.Button(self, width=self.buttonSize, height=self.buttonSize,
                                                   image=self.selectedPieces[row],
                                                   state="normal")
                b = self.buttons[(row, 0)]
                b.grid(row=row, column=0, padx=(10, 10), pady=(10, 10))


root = tk.Tk()
mainWindow = OutfitRecommenderGUI(root)
mainWindow.mainloop()
