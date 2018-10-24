#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
"""
Provide a Toplevel window to display widgets as they will look 
in the target application.

Apply any new attributes that come from an EditWin.
"""

import sys
    
from tkinter import *
import tkinter.messagebox
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu # ttk OptionMenu seems to be broken
from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Style, Notebook

class PreviewWin( Toplevel ):


    def __init__(self, MainWin):
        
        Toplevel.__init__(self, MainWin)#, bg='#ADD8E6') #'lightblue': '#ADD8E6',
        self.title('Preview Window')
        
        self.MainWin = MainWin
        
        self.widget_ijD = {} # index=(i,j) grid position: value=widget
        
        # only main window can close this window
        self.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)
        
        screen_width = MainWin.winfo_screenwidth()
        screen_height = MainWin.winfo_screenheight()
        
        if MainWin.state() == "zoomed":
            MainWin.state("normal")
        
        x_main = MainWin.winfo_x()
        y_main = MainWin.winfo_y()
        #print('MainWin (x,y) = (%s,%s)'%(x_main, y_main), '  MainWin.state()=',MainWin.state())

        # try to place PreviewWin right next to grid_notebook
        #    ... position to the upper right
        x = x_main + MainWin.winfo_width()  + 10
        y = y_main + 25 # if row added to GridGUI, can still see close "x" of MainWin

        # when launched from CLI, winfo_x and winfo_y are == 0
        # check for bad placement and try to make the best of it 
        if (x > screen_width - 310) or (x < 340):
            x=screen_width - 310
        
        if (y > screen_height - 210):
            y = screen_height - 210
        
        #print('setting PreviewWin geometry to:',(300,200,x,y))
        self.geometry( '%ix%i+%i+%i'%(300,200,x,y))
        #self.geometry( '+%i+%i'%(10,10))  # <-- sets x,y only.  w,h fill for widgets
        
        self.prevFrame = Frame(self)
        self.prevFrame.pack(fill=BOTH, expand=True)
        
        self.menuBar = False
        self.statusbar = False
        self.OK_Cancel_Frame = False
    
    #def position_next_to_main(self):
    #    x = self.MainWin.winfo_x() + self.MainWin.winfo_width()  + 10
    #    y = self.MainWin.winfo_y() + 25 # if row added to GridGUI, can still see close "x" of MainWin
    #    if x<340: x=340
    #    if y<10: y=10
    #    # position over to the upper right
    #    self.geometry( '+%i+%i'%(x,y))
    
    def destroy_all_children(self):
        """
        Delete all widgets directly attached to prevFrame.
        Some could be compound widgets like Frame or Notebook objects.
        """
        # should be the same as self.prevFrame.winfo_children()

        for ij, child in list(self.widget_ijD.items()):
            child.destroy()
            
        for child in self.prevFrame.winfo_children():
            child.destroy()
            
    
        self.widget_ijD = {} # index=(i,j) grid position: value=widget
        
    #def setActive(self):
    #    self.lift()
    #    self.focus_force()
    #    self.grab_set()
    #    self.grab_release()
    
    def remove_mock_statusbar(self):
        if self.statusbar:
            self.statusbar.destroy()
            self.statusbar = False
            #print('Status Bar Deleted from PreviewWin')
    
    def add_mock_statusbar(self):
        if self.OK_Cancel_Frame:
            need_to_replace_OK_Cancel = True
            self.remove_mock_OK_Cancel_Buttons()
        else:
            need_to_replace_OK_Cancel = False
        
        
        if not self.statusbar:
            self.statusbar = Label(self, text='Status Bar', bd=1, relief=SUNKEN)
            self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
            #print('Status Bar Added to PreviewWin')
    
        if need_to_replace_OK_Cancel:
            self.add_mock_OK_Cancel_Buttons()

    
    def remove_mock_OK_Cancel_Buttons(self):
        if self.OK_Cancel_Frame:
            self.OK_Cancel_Frame.destroy()
            self.OK_Cancel_Frame = False
            #print("OK Cancel Buttons Deleted from PreviewWin")
        
        
    def add_mock_OK_Cancel_Buttons(self):
        if not self.OK_Cancel_Frame:
        
            self.OK_Cancel_Frame = Frame(self)
            frame = self.OK_Cancel_Frame
            
            self.Button_1 = Button( frame , width="12", text="OK")
            self.Button_2 = Button( frame , width="12", text="Cancel")
            self.Label_1 = Label( frame , width="2", text="")
            self.Label_2 = Label( frame , width="2", text="")
            
            self.Label_1.grid( row=2, column=1, sticky='ew')
            self.Button_1.grid(row=2, column=2, pady="5", padx="5")
            self.Button_2.grid(row=2, column=4, pady="5", padx="5")
            self.Label_2.grid( row=2, column=5, sticky='ew')
            
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(5, weight=1)
            
            frame.pack(anchor=SW, fill=X, side=BOTTOM)
    
    def delete_menu(self):
        #print('Deleting Menu')
        if self.menuBar:
            #if hasattr(self, 'menuBar'):
            self.menuBar.delete(0,1000)
            #self.config(menu=None)
            #print('... Deleted Menu')
            self.menuBar = False
    
    def add_menu(self, menuSrcL):
        """add a menu to PreviewWin using user-input menuStr"""
        if not self.menuBar:
        
            for line in menuSrcL:
                #print('====>',line.strip(), end='\n')
                if line.find(', command')>=0:
                    line = line.split(', command')[0] + ')'
                    #print('========>',line.strip(), end='\n')
                exec( line.strip() ) # should create self.menuBar
    
    def add_widget(self, i,j, pw_widget):
        
        self.widget_ijD[(i,j)] = pw_widget
        
        if pw_widget.cobj.widget_type == 'Tab':
            #print('Skipping the .grid for Tab ',pw_widget.cobj.widget_name)
            pass
        else:
            #print('Doing the .grid for ',pw_widget.cobj.widget_name)
            pw_widget.grid(row=i, column=j)
        
        self.maybe_resize_preview_win()
    
    def maybe_resize_preview_win(self):
        
        self.update_idletasks()
    
        wprev = self.prevFrame.winfo_reqwidth()
        hprev = self.prevFrame.winfo_reqheight()
        #print("PreviewWin Req: w=%s, h=%s"%(wprev, hprev))
        
        if wprev>300 or hprev>200:
            self.geometry("")
        return
        
        #xmax_widget = pw_widget.winfo_x() + pw_widget.winfo_width()  + 20
        #ymax_widget = pw_widget.winfo_y() + pw_widget.winfo_height() + 60
        
        #if self.statusbar:
        #    ymax_widget += 20
            
        
        #if len(self.widget_ijD) >= 3:
        #    self.geometry("")
            
        #elif xmax_widget > wprev:
        #    #print('Expanding Preview Window Width to:',xmax_widget)
        #    #self.MainWin.statusMessage.set( 'Expanding Preview Window Width to: %s'%xmax_widget )
        #    #self.config( width=xmax_widget )
        #    self.geometry("")
        #    #self.update()

        #elif ymax_widget > hprev:
        #    #print('Expanding Preview Window Height to:',ymax_widget)
        #    #self.MainWin.statusMessage.set( 'Expanding Preview Window Height to: %s'%ymax_widget  )
        #    self.geometry("")
        #    #self.config( height=ymax_widget )
        #    #self.update()
        
        
    def cleanupOnQuit(self):
        if self.MainWin.allow_subWindows_to_close:
            # I'm not sure that transient windows need this, but I'm trying to be careful
            self.parent.focus_set()
            self.destroy()
        
        print( 'To Exit Applicaton, Use Main Window.' )
        self.MainWin.statusMessage.set('To Exit Applicaton, Use Main Window.')
    
        tkinter.messagebox.showinfo(
            "Use Main Window to Exit",
            "\n\n"+\
            "Please Use Main Window to Exit\n")
