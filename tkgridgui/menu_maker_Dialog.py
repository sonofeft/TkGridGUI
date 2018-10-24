#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals

# tk_happy generated code. DO NOT EDIT THE FOLLOWING. section top

from future import standard_library
standard_library.install_aliases()
from builtins import object
import sys

if sys.version_info < (3,):
    from tkSimpleDialog import Dialog
else:
    from tkinter.simpledialog import Dialog

from tkinter import *

class _Dialog(Dialog):
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptions=None):
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class Menumaker(_Dialog):

    def buttonbox(self):
        pass
        # this dummy routine overrides the standard "OK" and "Cancel" buttons
        # REMEMBER!!! to call self.ok() and self.cancel() in User Code

    def body(self, master):
        dialogframe = Frame(master, width=300, height=500)
        dialogframe.pack()

        self.Button_1 = Button(dialogframe,text="Save Menu", relief="raised", width="15")
        self.Button_1.place(x=24, y=12)
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

        self.Button_2 = Button(dialogframe,text="Exit Without Saving", relief="raised", width="15")
        self.Button_2.place(x=173, y=12)
        self.Button_2.bind("<ButtonRelease-1>", self.Button_2_Click)

        self.Label_1 = Label(dialogframe,pady="1", text="Be Consistent with Indents", width="30")
        self.Label_1.place(x=60, y=72)

        self.ctrl_keyChkBox_StringVar = StringVar()
        self.ctrl_keyChkBox = Checkbutton(dialogframe, text="Create ctrl-key shortcuts", width="30")
        self.ctrl_keyChkBox.place(x=24 ,y=90 )
        self.ctrl_keyChkBox.configure( onvalue="yes", offvalue="no", variable=self.ctrl_keyChkBox_StringVar)
        self.ctrl_keyChkBox_StringVar.set("yes")

        self.Message_1 = Message(dialogframe,text="Indent Text To Show Menu Structure", aspect="1000", relief="flat")
        self.Message_1.place(x=57, y=46)

        self.Text_1 = Text(dialogframe,padx="1", width="35", height="30")
        self.Text_1.place(x=12, y=120)
        # >>>>>>insert any user code below this comment for section top
        if self.dialogOptions:
            self.Text_1.insert(END, self.dialogOptions )


    def Master_Configure(self, event):
        if event.widget != self.master:
            if self.w != -1:
                return
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        if (self.x, self.y, self.w, self.h) == (-1,-1,-1,-1):
            self.x, self.y, self.w, self.h = x,y,w,h
        #if self.w!=w or self.h!=h:
        #    print( "Master reconfigured... make resize adjustments" )
        #print( "executed method Master_Configure" )

    def Button_1_Click(self, event): #click method for component ID=1
        #print( "executed method Button_1_Click" )
        self.ok()

    def Button_2_Click(self, event): #click method for component ID=2
        #print( "executed method Button_2_Click" )
        self.cancel()

    def validate(self):
        self.result = {} # return a dictionary of results
        # >>>>>>insert any user code below this comment for section dialog_validate
        # set values in "self.result" dictionary for return
        # for example...
        # self.result["age"] = self.Entry_2_StringVar.get() 

        self.result["test"] = "test message" 
        #self.result["menu"] = ascii( self.Text_1.get(1.0, END) )
        self.result["menu"] =  self.Text_1.get(1.0, END) 
        
        self.result["add_menu_ctrl_keys"] = self.ctrl_keyChkBox_StringVar.get()
        
        if sys.version_info >= (3,):
            #self.result["menu"] = self.result["menu"].encode( 'utf-8' )
            #self.result["menu"] = bytes(self.result["menu"], 'ascii')
            pass
        
        #print('menu = ', self.result["menu"] )
        #print('repr(menu) = ', repr(self.result["menu"]))
        return 1
# tk_happy generated code. DO NOT EDIT THE FOLLOWING. section end


    def apply(self):
        #print( 'apply called in menu_maker_Dialog' )
        pass

class _Testdialog(object):
    def __init__(self, master):
        frame = Frame(master, width=300, height=300)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        self.Button_1 = Button(text="Test Dialog", relief="raised", width="15")
        self.Button_1.place(x=84, y=36)
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    def Button_1_Click(self, event): #click method for component ID=1
        dialog = Menumaker(self.master, "Test Dialog",'File\n  New\n  Save')
        print( '===============Result from Dialog====================' )
        print( dialog.result )
        print( '=====================================================' )

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
