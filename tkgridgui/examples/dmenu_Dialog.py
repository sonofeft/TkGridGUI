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

if sys.version_info < (3,):
    from tkSimpleDialog import Dialog
else:
    from tkinter.simpledialog import Dialog


class _Dialog(Dialog):
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptions=None):
    
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class _dmenu(_Dialog):

    def buttonbox(self):
        pass
        # this dummy routine overrides the standard "OK" and "Cancel" buttons
        # REMEMBER!!! to call self.ok() and self.cancel() in User Code

    def body(self, master):
        dialogframe = Frame(master, width=384, height=184)
        self.dialogframe = dialogframe
        dialogframe.pack()


        self.make_Button_1( self.dialogframe )         #      Button:  at Main(1,1)
        self.make_Button_2( self.dialogframe )         #      Button:  at Main(1,3)
        self.make_Button_3( self.dialogframe )         #      Button: OK : at Main(5,1)
        self.make_Button_4( self.dialogframe )         #      Button: Cancel : at Main(5,3)
        self.make_Entry_1( self.dialogframe )          #       Entry:  at Main(3,1)
        self.make_Entry_2( self.dialogframe )          #       Entry:  at Main(3,3)
        self.make_Label_1( self.dialogframe )          #       Label:  at Main(4,1)
        self.make_Label_2( self.dialogframe )          #       Label:  at Main(5,0)
        self.make_Label_3( self.dialogframe )          #       Label:  at Main(5,4)
        self.make_Label_4( self.dialogframe )          #       Label:  at Main(5,2)
        self.make_Label_5( self.dialogframe )          #       Label:  at Main(6,1)
        self.make_Label_6( self.dialogframe )          #       Label:  at Main(0,1)
        self.make_Label_7( self.dialogframe )          #       Label:  at Main(2,1)

        self.dialogframe.rowconfigure(3, weight=1)
        self.dialogframe.columnconfigure(0, weight=1)
        self.dialogframe.columnconfigure(3, weight=1)

        
        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.dialogframe, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.grid(row=99, column=0, columnspan=99, sticky='ew')



        self.menuBar = Menu(self, relief = "raised", bd=2)

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

        self.config(menu=self.menuBar)




        # use both upper and lower characters for keyboard accelerator options.
        self.bind("<Control-N>", lambda event: self.menu_File_New())
        self.bind("<Control-n>", lambda event: self.menu_File_New())
        self.bind("<Control-O>", lambda event: self.menu_File_Open())
        self.bind("<Control-o>", lambda event: self.menu_File_Open())
        self.bind("<Control-S>", lambda event: self.menu_File_Save())
        self.bind("<Control-s>", lambda event: self.menu_File_Save())
        self.bind("<Control-E>", lambda event: self.menu_File_Exit())
        self.bind("<Control-e>", lambda event: self.menu_File_Exit())
        self.bind("<Control-M>", lambda event: self.menu_Sounds_Moo())
        self.bind("<Control-m>", lambda event: self.menu_Sounds_Moo())
        self.bind("<Control-W>", lambda event: self.menu_Sounds_Meow())
        self.bind("<Control-w>", lambda event: self.menu_Sounds_Meow())
        # >>>>>>insert any user code below this comment for section "top_of_init"
        self.statusMessage.set("Welcome to dmenu")

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_1"
    def make_Button_1(self, frame):
        """      Button:  at Main(1,1)"""
        self.Button_1 = Button( frame , text="Button_1", width="15")
        self.Button_1.grid(row=1, column=1)

        # >>>>>>insert any user code below this comment for section "make_Button_1"

        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_2"
    def make_Button_2(self, frame):
        """      Button:  at Main(1,3)"""
        self.Button_2 = Button( frame , text="Button_2", width="15")
        self.Button_2.grid(row=1, column=3)

        # >>>>>>insert any user code below this comment for section "make_Button_2"

        self.Button_2.bind("<ButtonRelease-1>", self.Button_2_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_3"
    def make_Button_3(self, frame):
        """      Button: OK : at Main(5,1)"""
        self.Button_3 = Button( frame , text="OK", width="15")
        self.Button_3.grid(row=5, column=1)

        # >>>>>>insert any user code below this comment for section "make_Button_3"

        self.Button_3.bind("<ButtonRelease-1>", self.Button_3_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_4"
    def make_Button_4(self, frame):
        """      Button: Cancel : at Main(5,3)"""
        self.Button_4 = Button( frame , text="Cancel", width="15")
        self.Button_4.grid(row=5, column=3)

        # >>>>>>insert any user code below this comment for section "make_Button_4"

        self.Button_4.bind("<ButtonRelease-1>", self.Button_4_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Entry_1"
    def make_Entry_1(self, frame):
        """       Entry:  at Main(3,1)"""
        self.Entry_1 = Entry( frame , width="15")
        self.Entry_1.grid(row=3, column=1)
        self.Entry_1_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Entry_1"

        self.Entry_1.configure(textvariable=self.Entry_1_StringVar)
        self.Entry_1_StringVar_traceName = self.Entry_1_StringVar.trace_variable("w", self.Entry_1_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Entry_2"
    def make_Entry_2(self, frame):
        """       Entry:  at Main(3,3)"""
        self.Entry_2 = Entry( frame , width="15")
        self.Entry_2.grid(row=3, column=3)
        self.Entry_2_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Entry_2"

        self.Entry_2.configure(textvariable=self.Entry_2_StringVar)
        self.Entry_2_StringVar_traceName = self.Entry_2_StringVar.trace_variable("w", self.Entry_2_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_1"
    def make_Label_1(self, frame):
        """       Label:  at Main(4,1)"""
        self.Label_1 = Label( frame , text="", width="15")
        self.Label_1.grid(row=4, column=1, sticky="ns")

        # >>>>>>insert any user code below this comment for section "make_Label_1"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_2"
    def make_Label_2(self, frame):
        """       Label:  at Main(5,0)"""
        self.Label_2 = Label( frame , text="", width="1")
        self.Label_2.grid(row=5, column=0, sticky="ew")

        # >>>>>>insert any user code below this comment for section "make_Label_2"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_3"
    def make_Label_3(self, frame):
        """       Label:  at Main(5,4)"""
        self.Label_3 = Label( frame , text="", width="1")
        self.Label_3.grid(row=5, column=4, sticky="ew")

        # >>>>>>insert any user code below this comment for section "make_Label_3"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_4"
    def make_Label_4(self, frame):
        """       Label:  at Main(5,2)"""
        self.Label_4 = Label( frame , text="", width="1")
        self.Label_4.grid(row=5, column=2, sticky="ew")

        # >>>>>>insert any user code below this comment for section "make_Label_4"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_5"
    def make_Label_5(self, frame):
        """       Label:  at Main(6,1)"""
        self.Label_5 = Label( frame , text="", width="15")
        self.Label_5.grid(row=6, column=1)

        # >>>>>>insert any user code below this comment for section "make_Label_5"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_6"
    def make_Label_6(self, frame):
        """       Label:  at Main(0,1)"""
        self.Label_6 = Label( frame , text="", width="15")
        self.Label_6.grid(row=0, column=1)

        # >>>>>>insert any user code below this comment for section "make_Label_6"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_7"
    def make_Label_7(self, frame):
        """       Label:  at Main(2,1)"""
        self.Label_7 = Label( frame , text="", width="15")
        self.Label_7.grid(row=2, column=1)

        # >>>>>>insert any user code below this comment for section "make_Label_7"


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
        """      Button:  at Main(1,3)"""
        pass
        # >>>>>>insert any user code below this comment for section "Button_2_Click"
        # replace, delete, or comment-out the following
        print( "executed method Button_2_Click" )
        self.statusMessage.set("executed method Button_2_Click")

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Button_3_Click"
    def Button_3_Click(self, event): #bind method for component ID=Button_3
        """      Button: OK : at Main(5,1)"""
        pass
        # >>>>>>insert any user code below this comment for section "Button_3_Click"
        # replace, delete, or comment-out the following
        print( "executed method Button_3_Click" )
        self.statusMessage.set("executed method Button_3_Click")
        self.ok()

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Button_4_Click"
    def Button_4_Click(self, event): #bind method for component ID=Button_4
        """      Button: Cancel : at Main(5,3)"""
        pass
        # >>>>>>insert any user code below this comment for section "Button_4_Click"
        # replace, delete, or comment-out the following
        print( "executed method Button_4_Click" )
        self.statusMessage.set("executed method Button_4_Click")
        self.cancel()

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Entry_1_StringVar_traceName"
    def Entry_1_StringVar_Callback(self, varName, index, mode):
        """       Entry:  at Main(3,1)"""
        pass

        # >>>>>>insert any user code below this comment for section "Entry_1_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Entry_1_StringVar_Callback varName, index, mode",varName, index, mode )
        self.statusMessage.set("    Entry_1_StringVar = "+self.Entry_1_StringVar.get())
        print( "    new StringVar value =",self.Entry_1_StringVar.get() )



    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Entry_2_StringVar_traceName"
    def Entry_2_StringVar_Callback(self, varName, index, mode):
        """       Entry:  at Main(3,3)"""
        pass

        # >>>>>>insert any user code below this comment for section "Entry_2_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Entry_2_StringVar_Callback varName, index, mode",varName, index, mode )
        self.statusMessage.set("    Entry_2_StringVar = "+self.Entry_2_StringVar.get())
        print( "    new StringVar value =",self.Entry_2_StringVar.get() )



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


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "dialog_validate"
    def validate(self):
        self.result = {} # return a dictionary of results
    

        self.result["Entry_1"] = self.Entry_1_StringVar.get()
        self.result["Entry_2"] = self.Entry_2_StringVar.get()

        # >>>>>>insert any user code below this comment for section "dialog_validate"
        # set values in "self.result" dictionary for return
        # for example...
        # self.result["age"] = self.Entry_2_StringVar.get() 


        self.result["test"] = "test message" 
        return 1
# TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "end"


    def apply(self):
        print( 'apply called' )

class _Testdialog:
    def __init__(self, master):
        frame = Frame(master, width=300, height=300)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        self.Button_1 = Button(text="Test Dialog", relief="raised", width="15")
        self.Button_1.place(x=84, y=36)
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    def Button_1_Click(self, event): #click method for component ID=1
        dialog = _dmenu(self.master, "Test Dialog")
        print( '===============Result from Dialog====================' )
        print( dialog.result )
        print( '=====================================================' )

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
