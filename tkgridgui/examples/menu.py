#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function

# NOTICE... this file is generated by TkGridGUI.
# Any code or comments added by the user must be in designated areas ONLY.
# User additions will be lost if they are placed in code-generated areas.
# (i.e. Saving from TkGridGUI will over-write code-generated areas.)

# TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "imports"

import sys

if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    from ttk import Combobox, Progressbar, Separator, Treeview, Notebook
else:
    from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Notebook

from tkinter import *
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu
from tkinter import _setit as set_command


# >>>>>>insert any user code below this comment for section "imports"
# Place any user import statements here

# TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "top_of_init"
class _menu:
    def __init__(self, master):
    
        grid_frame = Frame( master )
        self.grid_frame = grid_frame
        grid_frame.pack(expand=1, fill=BOTH)
        self.master = master
        
        self.x, self.y, self.w, self.h = 10, 10, 300, 200

        self.master.geometry("300x200")
        self.master.title("menu")

        self.make_Button_1( self.grid_frame )          #      Button:  at Main(1,1)
        self.make_Button_2( self.grid_frame )          #      Button:  at Main(2,1)


        
        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.master, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)



        self.menuBar = Menu(master, relief = "raised", bd=2)

        top_File = Menu(self.menuBar, tearoff=0)

        top_File.add("command", label = "New", command=self.menu_File_New, underline=0, accelerator="Ctrl+N")
        top_File.add("command", label = "Open", command=self.menu_File_Open, underline=0, accelerator="Ctrl+O")
        top_File.add("command", label = "Save", command=self.menu_File_Save, underline=0, accelerator="Ctrl+S")
        top_File.add_separator()
        top_File.add("command", label = "Exit", command=self.menu_File_Exit, underline=0, accelerator="Ctrl+E")
        self.menuBar.add("cascade", label="File", menu=top_File)

        top_Help = Menu(self.menuBar, tearoff=0)


        top_Sounds = Menu(self.menuBar, tearoff=0)

        top_Sounds.add("command", label = "Moo", command=self.menu_Sounds_Moo, underline=0, accelerator="Ctrl+M")
        top_Sounds.add("command", label = "Meow", command=self.menu_Sounds_Meow, underline=3, accelerator="Ctrl+W")
        top_Help.add("cascade", label="Sounds", menu=top_Sounds)
        self.menuBar.add("cascade", label="Help", menu=top_Help)

        master.config(menu=self.menuBar)




        # use both upper and lower characters for keyboard accelerator options.
        self.master.bind("<Control-N>", lambda event: self.menu_File_New())
        self.master.bind("<Control-n>", lambda event: self.menu_File_New())
        self.master.bind("<Control-O>", lambda event: self.menu_File_Open())
        self.master.bind("<Control-o>", lambda event: self.menu_File_Open())
        self.master.bind("<Control-S>", lambda event: self.menu_File_Save())
        self.master.bind("<Control-s>", lambda event: self.menu_File_Save())
        self.master.bind("<Control-E>", lambda event: self.menu_File_Exit())
        self.master.bind("<Control-e>", lambda event: self.menu_File_Exit())
        self.master.bind("<Control-M>", lambda event: self.menu_Sounds_Moo())
        self.master.bind("<Control-m>", lambda event: self.menu_Sounds_Moo())
        self.master.bind("<Control-W>", lambda event: self.menu_Sounds_Meow())
        self.master.bind("<Control-w>", lambda event: self.menu_Sounds_Meow())
        # >>>>>>insert any user code below this comment for section "top_of_init"
        self.statusMessage.set("Welcome to menu")

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_1"
    def make_Button_1(self, frame):
        """      Button:  at Main(1,1)"""
        self.Button_1 = Button( frame , text="Button_1", width="15")
        self.Button_1.grid(row=1, column=1)

        # >>>>>>insert any user code below this comment for section "make_Button_1"

        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_2"
    def make_Button_2(self, frame):
        """      Button:  at Main(2,1)"""
        self.Button_2 = Button( frame , text="Button_2", width="15")
        self.Button_2.grid(row=2, column=1)

        # >>>>>>insert any user code below this comment for section "make_Button_2"

        self.Button_2.bind("<ButtonRelease-1>", self.Button_2_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Button_1_Click"
    def Button_1_Click(self, event): #bind method for component ID=Button_1
        """      Button:  at Main(1,1)"""
        pass
        # >>>>>>insert any user code below this comment for section "Button_1_Click"
        # replace, delete, or comment-out the following
        print( "executed method Button_1_Click" )
        self.statusMessage.set("executed method Button_1_Click")

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Button_2_Click"
    def Button_2_Click(self, event): #bind method for component ID=Button_2
        """      Button:  at Main(2,1)"""
        pass
        # >>>>>>insert any user code below this comment for section "Button_2_Click"
        # replace, delete, or comment-out the following
        print( "executed method Button_2_Click" )
        self.statusMessage.set("executed method Button_2_Click")

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_New"
    def menu_File_New(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_New"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_New")
        print( "called menu_File_New" )


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_Open"
    def menu_File_Open(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_Open"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_Open")
        print( "called menu_File_Open" )


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_Save"
    def menu_File_Save(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_Save"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_Save")
        print( "called menu_File_Save" )


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_"
    def menu_File_(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_")
        print( "called menu_File_" )


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_Exit"
    def menu_File_Exit(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_Exit"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_Exit")
        print( "called menu_File_Exit" )


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "menu_Sounds_Moo"
    def menu_Sounds_Moo(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Sounds_Moo"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Sounds_Moo")
        print( "called menu_Sounds_Moo" )


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "menu_Sounds_Meow"
    def menu_Sounds_Meow(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Sounds_Meow"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Sounds_Meow")
        print( "called menu_Sounds_Meow" )


# TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "end"

def main():
    root = Tk()
    app = _menu(root)
    root.mainloop()

if __name__ == '__main__':
    main()
