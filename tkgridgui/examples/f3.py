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
class _f3:
    def __init__(self, master):
    
        grid_frame = Frame( master )
        self.grid_frame = grid_frame
        grid_frame.pack(expand=1, fill=BOTH)
        self.master = master
        
        self.x, self.y, self.w, self.h = 10, 10, 328, 150

        self.master.title("f3")

        self.make_Button_3( self.grid_frame )          #      Button:  at Main(1,1)
        self.make_Button_4( self.grid_frame )          #      Button:  at Main(2,1)
        self.make_Frame_1( self.grid_frame )           #       Frame:  at Main(2,2)
        self.make_Frame_2( self.grid_frame )           #       Frame:  at Main(1,2)
        self.make_Checkbutton_1( self.Frame_1 )        # Checkbutton:  at Frame_1(1,1)
        self.make_Checkbutton_2( self.Frame_1 )        # Checkbutton:  at Frame_1(2,1)
        self.make_Checkbutton_3( self.Frame_1 )        # Checkbutton:  at Frame_1(3,1)
        self.make_Entry_1( self.Frame_2 )              #       Entry:  at Frame_2(1,1)
        self.make_Entry_2( self.Frame_2 )              #       Entry:  at Frame_2(2,1)
        self.make_Entry_3( self.Frame_2 )              #       Entry:  at Frame_2(3,1)
        self.make_Frame_3( self.Frame_2 )              #       Frame:  at Frame_2(1,2)
        self.make_Label_1( self.Frame_3 )              #       Label:  at Frame_3(1,2)
        self.make_Label_2( self.Frame_3 )              #       Label:  at Frame_3(2,2)
        self.make_Label_3( self.Frame_3 )              #       Label:  at Frame_3(3,2)


        # >>>>>>insert any user code below this comment for section "top_of_init"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_3"
    def make_Button_3(self, frame):
        """      Button:  at Main(1,1)"""
        self.Button_3 = Button( frame , text="Button_3", width="15")
        self.Button_3.grid(row=1, column=1)

        # >>>>>>insert any user code below this comment for section "make_Button_3"

        self.Button_3.bind("<ButtonRelease-1>", self.Button_3_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Button_4"
    def make_Button_4(self, frame):
        """      Button:  at Main(2,1)"""
        self.Button_4 = Button( frame , text="Button_4", width="15")
        self.Button_4.grid(row=2, column=1)

        # >>>>>>insert any user code below this comment for section "make_Button_4"

        self.Button_4.bind("<ButtonRelease-1>", self.Button_4_Click)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Frame_1"
    def make_Frame_1(self, frame):
        """       Frame:  at Main(2,2)"""
        self.Frame_1 = Frame( frame , width="60", height="50")
        self.Frame_1.grid(row=2, column=2)

        # >>>>>>insert any user code below this comment for section "make_Frame_1"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Frame_2"
    def make_Frame_2(self, frame):
        """       Frame:  at Main(1,2)"""
        self.Frame_2 = Frame( frame , width="60", height="50")
        self.Frame_2.grid(row=1, column=2)

        # >>>>>>insert any user code below this comment for section "make_Frame_2"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Checkbutton_1"
    def make_Checkbutton_1(self, frame):
        """ Checkbutton:  at Frame_1(1,1)"""
        self.Checkbutton_1 = Checkbutton( frame , text="Checkbutton_1", width="15")
        self.Checkbutton_1.grid(row=1, column=1)
        self.Checkbutton_1_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Checkbutton_1"

        self.Checkbutton_1.configure(variable=self.Checkbutton_1_StringVar, onvalue="yes", offvalue="no")
        self.Checkbutton_1_StringVar.set("no")
        self.Checkbutton_1_StringVar_traceName = self.Checkbutton_1_StringVar.trace_variable("w", self.Checkbutton_1_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Checkbutton_2"
    def make_Checkbutton_2(self, frame):
        """ Checkbutton:  at Frame_1(2,1)"""
        self.Checkbutton_2 = Checkbutton( frame , text="Checkbutton_2", width="15")
        self.Checkbutton_2.grid(row=2, column=1)
        self.Checkbutton_2_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Checkbutton_2"

        self.Checkbutton_2.configure(variable=self.Checkbutton_2_StringVar, onvalue="yes", offvalue="no")
        self.Checkbutton_2_StringVar.set("no")
        self.Checkbutton_2_StringVar_traceName = self.Checkbutton_2_StringVar.trace_variable("w", self.Checkbutton_2_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Checkbutton_3"
    def make_Checkbutton_3(self, frame):
        """ Checkbutton:  at Frame_1(3,1)"""
        self.Checkbutton_3 = Checkbutton( frame , text="Checkbutton_3", width="15")
        self.Checkbutton_3.grid(row=3, column=1)
        self.Checkbutton_3_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Checkbutton_3"

        self.Checkbutton_3.configure(variable=self.Checkbutton_3_StringVar, onvalue="yes", offvalue="no")
        self.Checkbutton_3_StringVar.set("no")
        self.Checkbutton_3_StringVar_traceName = self.Checkbutton_3_StringVar.trace_variable("w", self.Checkbutton_3_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Entry_1"
    def make_Entry_1(self, frame):
        """       Entry:  at Frame_2(1,1)"""
        self.Entry_1 = Entry( frame , width="15")
        self.Entry_1.grid(row=1, column=1)
        self.Entry_1_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Entry_1"

        self.Entry_1.configure(textvariable=self.Entry_1_StringVar)
        self.Entry_1_StringVar_traceName = self.Entry_1_StringVar.trace_variable("w", self.Entry_1_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Entry_2"
    def make_Entry_2(self, frame):
        """       Entry:  at Frame_2(2,1)"""
        self.Entry_2 = Entry( frame , width="15")
        self.Entry_2.grid(row=2, column=1)
        self.Entry_2_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Entry_2"

        self.Entry_2.configure(textvariable=self.Entry_2_StringVar)
        self.Entry_2_StringVar_traceName = self.Entry_2_StringVar.trace_variable("w", self.Entry_2_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Entry_3"
    def make_Entry_3(self, frame):
        """       Entry:  at Frame_2(3,1)"""
        self.Entry_3 = Entry( frame , width="15")
        self.Entry_3.grid(row=3, column=1)
        self.Entry_3_StringVar = StringVar()

        # >>>>>>insert any user code below this comment for section "make_Entry_3"

        self.Entry_3.configure(textvariable=self.Entry_3_StringVar)
        self.Entry_3_StringVar_traceName = self.Entry_3_StringVar.trace_variable("w", self.Entry_3_StringVar_Callback)

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Frame_3"
    def make_Frame_3(self, frame):
        """       Frame:  at Frame_2(1,2)"""
        self.Frame_3 = Frame( frame , width="60", height="50")
        self.Frame_3.grid(row=1, column=2, rowspan="3")

        # >>>>>>insert any user code below this comment for section "make_Frame_3"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_1"
    def make_Label_1(self, frame):
        """       Label:  at Frame_3(1,2)"""
        self.Label_1 = Label( frame , text="Label_1", width="15")
        self.Label_1.grid(row=1, column=2)

        # >>>>>>insert any user code below this comment for section "make_Label_1"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_2"
    def make_Label_2(self, frame):
        """       Label:  at Frame_3(2,2)"""
        self.Label_2 = Label( frame , text="Label_2", width="15")
        self.Label_2.grid(row=2, column=2)

        # >>>>>>insert any user code below this comment for section "make_Label_2"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "make_Label_3"
    def make_Label_3(self, frame):
        """       Label:  at Frame_3(3,2)"""
        self.Label_3 = Label( frame , text="Label_3", width="15")
        self.Label_3.grid(row=3, column=2)

        # >>>>>>insert any user code below this comment for section "make_Label_3"


    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Button_3_Click"
    def Button_3_Click(self, event): #bind method for component ID=Button_3
        """      Button:  at Main(1,1)"""
        pass
        # >>>>>>insert any user code below this comment for section "Button_3_Click"
        # replace, delete, or comment-out the following
        print( "executed method Button_3_Click" )

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Button_4_Click"
    def Button_4_Click(self, event): #bind method for component ID=Button_4
        """      Button:  at Main(2,1)"""
        pass
        # >>>>>>insert any user code below this comment for section "Button_4_Click"
        # replace, delete, or comment-out the following
        print( "executed method Button_4_Click" )

    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Checkbutton_1_StringVar_traceName"
    def Checkbutton_1_StringVar_Callback(self, varName, index, mode):
        """ Checkbutton:  at Frame_1(1,1)"""
        pass

        # >>>>>>insert any user code below this comment for section "Checkbutton_1_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Checkbutton_1_StringVar_Callback varName, index, mode",varName, index, mode )
        print( "    new StringVar value =",self.Checkbutton_1_StringVar.get() )



    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Checkbutton_2_StringVar_traceName"
    def Checkbutton_2_StringVar_Callback(self, varName, index, mode):
        """ Checkbutton:  at Frame_1(2,1)"""
        pass

        # >>>>>>insert any user code below this comment for section "Checkbutton_2_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Checkbutton_2_StringVar_Callback varName, index, mode",varName, index, mode )
        print( "    new StringVar value =",self.Checkbutton_2_StringVar.get() )



    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Checkbutton_3_StringVar_traceName"
    def Checkbutton_3_StringVar_Callback(self, varName, index, mode):
        """ Checkbutton:  at Frame_1(3,1)"""
        pass

        # >>>>>>insert any user code below this comment for section "Checkbutton_3_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Checkbutton_3_StringVar_Callback varName, index, mode",varName, index, mode )
        print( "    new StringVar value =",self.Checkbutton_3_StringVar.get() )



    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Entry_1_StringVar_traceName"
    def Entry_1_StringVar_Callback(self, varName, index, mode):
        """       Entry:  at Frame_2(1,1)"""
        pass

        # >>>>>>insert any user code below this comment for section "Entry_1_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Entry_1_StringVar_Callback varName, index, mode",varName, index, mode )
        print( "    new StringVar value =",self.Entry_1_StringVar.get() )



    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Entry_2_StringVar_traceName"
    def Entry_2_StringVar_Callback(self, varName, index, mode):
        """       Entry:  at Frame_2(2,1)"""
        pass

        # >>>>>>insert any user code below this comment for section "Entry_2_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Entry_2_StringVar_Callback varName, index, mode",varName, index, mode )
        print( "    new StringVar value =",self.Entry_2_StringVar.get() )



    # TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "Entry_3_StringVar_traceName"
    def Entry_3_StringVar_Callback(self, varName, index, mode):
        """       Entry:  at Frame_2(3,1)"""
        pass

        # >>>>>>insert any user code below this comment for section "Entry_3_StringVar_traceName"
        # replace, delete, or comment-out the following
        print( "Entry_3_StringVar_Callback varName, index, mode",varName, index, mode )
        print( "    new StringVar value =",self.Entry_3_StringVar.get() )



# TkGridGUI generated code. DO NOT EDIT THE FOLLOWING. section "end"

def main():
    root = Tk()
    app = _f3(root)
    root.mainloop()

if __name__ == '__main__':
    main()
