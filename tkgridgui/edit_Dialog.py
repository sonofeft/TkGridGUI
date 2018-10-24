#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function

import sys

if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    import tkMessageBox
    from ttk import Combobox, Progressbar, Separator, Treeview, Notebook
    from tkSimpleDialog import Dialog
    import tkColorChooser
    from ttk import Combobox
else:
    import tkinter.messagebox as tkMessageBox
    from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Notebook
    from tkinter.simpledialog import Dialog
    import tkinter.colorchooser as tkColorChooser
    from tkinter.ttk import Combobox
    
from tkinter import *
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu # ttk OptionMenu seems to be broken


from tkgridgui.tkfontchooser import askfont
from tkgridgui.edit_options import WidgetPropertyDefinitionsD, get_definition_optionsL

class _Dialog(Dialog):
    # use dialogOptionsD dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptionsD=None):
        
        self.dialogOptionsD = dialogOptionsD
        self.my_title = title
        Dialog.__init__(self, parent, title)

OMIT_ATTR = ('row_weights','col_weights', 'tab_labels', 'child_widget_list') # private attr.

class Edit_Properties_Dialog(_Dialog):

    def body(self, master):
        dialogframe = Frame(master, width=439, height=428)
        dialogframe.pack()


        self.Delete_Checkbutton = Checkbutton(dialogframe,text="Check Here to Delete Widget", width="15")
        
        self.Delete_Checkbutton.grid(row=0, column=1, columnspan=3, sticky=W+E+N+S)
        
        self.Delete_Checkbutton_StringVar = StringVar()
        self.Delete_Checkbutton_StringVar.set("no")
        self.Delete_Checkbutton.configure(variable=self.Delete_Checkbutton_StringVar, onvalue="yes", offvalue="no")
        
        self.name_labelL = []
        self.val_entryL = []
        self.val_strvarL = []
        self.def_labelL = []
        self.cboxD = {} # index=row: value=Combobox (if any)
        self.cbox_svarD = {}# index=Combobox Widget Object: value=Combobox StringVar (if any)
        self.val_crossrefD = {}# index=Combobox Widget Object: value=index of val_strvarL
        
        keyL = sorted( self.dialogOptionsD.keys() )
        
        keyL = [k for k in keyL if k not in OMIT_ATTR]
        
        for i,key in enumerate( keyL ):
            row = 3 + i
            val, desc = self.dialogOptionsD[ key ]
            
            self.name_labelL.append( Label(dialogframe,text=key) )
            
            self.val_entryL.append( Entry(dialogframe) )
            self.val_strvarL.append( StringVar() )
            self.val_entryL[-1].configure(textvariable=self.val_strvarL[-1])
            self.val_strvarL[-1].set( val )
            
            self.def_labelL.append( Label(dialogframe,text=desc) )
        

            self.name_labelL[-1].grid(row=row, column=1, sticky=E)
            self.val_entryL[-1].grid(row=row, column=2)
            
            if key.lower().endswith("ground"): # i.e. a color 
                btn = Button(dialogframe, text="Color", command=lambda N=i: self.get_color( N ) )
                btn.grid(row=row, column=0, sticky=E)
                
            elif key.lower()=="font":
                btn = Button(dialogframe, text="Font ", command=lambda N=i: self.get_font( N ) )
                btn.grid(row=row, column=0, sticky=E)
                
            self.def_labelL[-1].grid(row=row, column=3, sticky=W)
            
            if key in WidgetPropertyDefinitionsD:
                long_def_label = Label(dialogframe,text=WidgetPropertyDefinitionsD[key])
                long_def_label.grid(row=row, column=4, sticky=W)
                
                optionsL = get_definition_optionsL( key )
                if optionsL:
                    svar = StringVar()
                    self.cboxD[i] = Combobox(dialogframe, values=optionsL, width=7, textvariable=svar)
                    #                         validatecommand=lambda N=i: self.get_option(N))
                    self.cboxD[i].grid(row=row, column=0, sticky=E)
                    
                    self.cbox_svarD[ self.cboxD[i] ] = svar
                    self.cbox_svarD[ self.cboxD[i] ].set( val )
                    self.val_crossrefD[ self.cboxD[i] ] = i
                    
                    self.cboxD[i].bind("<<ComboboxSelected>>", self.get_option )

        #self.resizable(0,0) # Linux may not respect this

    def get_option(self, event):
        i = self.val_crossrefD[ event.widget ]
        #print('get_option for %i ='%i , self.cbox_svarD[ event.widget ].get() )
        self.val_strvarL[i].set( self.cbox_svarD[ event.widget ].get() )

    def get_font(self, N):
        font = askfont(self)
        if font:
            # spaces in the family name need to be escaped
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
                
            self.val_strvarL[N].set( font_str )
        

    def get_color(self, N):
        ctup,cstr = tkColorChooser.askcolor(title='Selected Color')
        if cstr:
            self.val_strvarL[N].set( cstr )
        

    def validate(self):
        """Return ONLY changes made to default values"""
        self.result = {} # return a dictionary of results
        
        # check for delete command
        if self.Delete_Checkbutton_StringVar.get() == "yes":

            msg = "Do you really want to delete %s?"%self.my_title

            child_widget_list = self.dialogOptionsD.get('child_widget_list',[])
            if len(child_widget_list) > 0:
                sL = [ '\n\n%s contains %i other widgets\n\n'%(self.my_title, len(child_widget_list)) ]
                
                for name in child_widget_list:
                    sL.append( '%s\n'%name )
                msg = msg + ''.join(sL)
            
            really = tkMessageBox.askyesno( "Delete %s ?"%self.my_title, msg )
            #print("really = ", really)
            if really:
                self.result["DeleteWidget"] = "yes"
        
        #self.name_labelL, self.val_entryL, self.val_strvarL, self.def_labelL,
        keyL = sorted( self.dialogOptionsD.keys() )
        
        keyL = [k for k in keyL if k not in OMIT_ATTR]
        
        for i,key in enumerate( keyL ):
            
            val, desc = self.dialogOptionsD[ key ]
            if str(val) != str(self.val_strvarL[i].get()):
                self.result[key] = str(self.val_strvarL[i].get())
            
        return 1

    def apply(self):
        #print( 'apply called in edit_Dialog' )
        pass

test_propsD = {"background"      : ("" ,"The background color"),
    "borderwidth"     : ("" ,"The size of the border in pixels. usually 1 or 2 pixels."),
    "cursor"          : ("" ,"The shape of the cursor when the cursor is over the widget."),
    "font"            : ("" ,"The font used for text on the widget."),
    "foreground"      : ("" ,"Color to use for text and bitmap content"),
    "from_"           : ("" ,"Constrain the values to a numeric range. For example, from_=-10 and to=10"),
    "height"          : ("" ,"Height in pixels or text lines"),
    "image"           : ("" ,"Image to display (requires tk.PhotoImage)"),
    "justify"         : ("" ,"Align multiple lines of text. LEFT, RIGHT, CENTER"),
    "label"           : ("" ,"An optional text label"),
    "length"          : ("" ,"Number of pixels for the x dimension if the scale is horizontal, or the y dimension if vertical"),
    "orient"          : ("" ,"HORIZONTAL or VERTICAL"),
    "overrelief"      : ("" ,"Relief to use when the mouse is over the widget SUNKEN RAISED GROOVE RIDGE FLAT"),
    "padx"            : ("" ,"Additional padding left and right of the text."),
    "pady"            : ("" ,"Additional padding above and below the text."),
    "relief"          : ("" ,"Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT"),
    "state"           : ("" ,"NORMAL, ACTIVE or DISABLED"),
    "style"           : ("" ,"TTK style"),
    "text"            : ("" ,"Text displayed on the widget."),
    "to"              : ("" ,"Value that defines one end of the scale's range"),
    "value"           : ("" ,"The initial value of the widget's variable"),
    "width"           : ("" ,"Width in pixels or characters")}

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
        dialog = Edit_Properties_Dialog(self.master, "Test Dialog", dialogOptionsD=test_propsD)
        print( '===============Result from Dialog====================' )
        print( dialog.result )
        print( '=====================================================' )

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
