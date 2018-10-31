#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object
r"""
tkGridGUI builds a target python Tkinter GUI graphic user interface using 
the grid geometry manager.

The main idea behind tkGridGUI is to allow a fully "wired" python 
Tkinter GUI application to be created in minutes.  The users main 
responsibility is to add logic to the Tkinter framework created by tkGridGUI.  
tkGridGUI holds structures to create items such as menus, toolbars and statusbars.

TkGridGUI
Copyright (C) 2018  Charlie Taylor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
import os
here = os.path.abspath(os.path.dirname(__file__))

__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2018 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "3 - Alpha" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"


import sys
from sys import platform

if sys.version_info < (3,):
    from tkSimpleDialog import Dialog
else:
    from tkinter.simpledialog import Dialog

from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import tkinter.colorchooser
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu # ttk OptionMenu seems to be broken
from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Style, Notebook

from tkgridgui.cross_platform_fonts_Dialog import get_cross_platform_font

from tkgridgui.grid_notebook import NotebookGridDes, CONTROLS, ContainerControlsL, CONTROL_NEXT_NUMBER_D, CONTROL_COLOR_D
from tkgridgui.target_tk_app_def import TargetTkAppDef # used to read and save App Definition
from tkgridgui.preview_win import PreviewWin

from tkgridgui.menu_maker_Dialog import Menumaker
from tkgridgui.make_py_src import FormSource
from tkgridgui.make_menu_src import buildMenuSource, getMenuSource

from tkgridgui.maybe_save_Dialog import maybe_save_dialog
from tkgridgui.named_color_picker_Dialog import named_color_picker

class GridGUI(object):
    """
    tkGridGUI builds a python Tkinter GUI graphic user interface using the grid geometry manager.
    """

    def __init__(self, MainWin):
        """Inits Tkinter window of GridGUI."""
        
        self.root = MainWin
        #MainWin.geometry("800x600") #You want the size of the app to be 500x500
        MainWin.geometry( '+10+30' )
        
        try:
            style = Style(self.root)
            if "win" == platform[:3]:
                style.theme_use('vista')
            elif "darwin" in platform:
                style.theme_use('clam')
            else:
                style.theme_use('clam')
            bg = style.lookup("TLabel", "background")
            self.root.configure(bg=bg)
        except:
            print("OOPS... failed to set style.theme_use... Let's press on.")
        
        self.MainWin = MainWin
        
        MainWin.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)
        MainWin.allow_subWindows_to_close = 0
        
        self.add_menu_to_MainWin()
        
        topFrame = Frame( MainWin ) # frame for controls
        #topFrame = tx.ScrolledWindow( MainWin )
        
        frame1 = LabelFrame(topFrame, text="Widgets")
        self.place_widget_selection_listbox( frame1 )
        frame1.pack(anchor=NW, side=LEFT)
        
        frame2 = Frame( topFrame ) # frame for radio buttons
        self.place_gui_definition_controls( frame2, MainWin )
        frame2.pack(anchor=N, side=LEFT)

        self.grid_frame = Frame(topFrame) 
        self.grid_notebook = NotebookGridDes(self, self.grid_frame, MainWin, num_cols=5, num_rows=8)
        self.grid_frame.pack(anchor=N, side=LEFT)
                
        topFrame.pack(fill=BOTH, expand=Y)
        
        # make a Status Bar
        statframe = Frame(MainWin)
        MainWin.statusMessage = StringVar()
        MainWin.statusMessage.set('Welcome to TkGridGUI')
        self.statusbar = Label(statframe, textvariable=MainWin.statusMessage, 
            relief=SUNKEN, anchor=W)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
        statframe.pack(anchor=SW, fill=X, side=BOTTOM)
        
        # Initialize some GridGUI parameters
        
        self.current_fileFullName = '' # no file for now
        self.current_filePath = '' # no file for now
        self.current_fileName = '' # no file for now

        self.target_app = TargetTkAppDef( name='myApp')
        self.PreviewWin = None # need to initialize later
        
        self.Listbox_1_Click( 'FromInit' ) # execute selection logic

        
        self.in_reading_mode = False # when True, suppresses some automatic trace actions.
        if len( sys.argv ) == 2:
            fName = sys.argv[1]
            if fName.find('.')<0:
                fName += '.def'
                
            fullpath = os.path.abspath(fName)
            
            if os.path.isfile( fullpath ): # if file exists, read it as a definition file
                self.openFile( fName=fullpath )
            else:
                self.MainWin.statusMessage.set('file "%s" does not exist'%fName)
                
        self.grid_notebook.notebook.bind("<<NotebookTabChanged>>", self.tab_of_notebook_changed)

        self.mouse_location = ''
        self.MainWin.bind("<Enter>", self.onMainWindowEnter)

    def onMainWindowEnter(self, event):
        """Only track Enter... Want last known location."""
        #if self.mouse_location != 'main_window':
        #    print('mouse_location = main_window')
        self.mouse_location = 'main_window'

    def refresh_preview_win(self, allow_destroy_children=True):
        """
        Place all of the widgets from grid_notebook onto PreviewWin.
        May need to delete and rebuild current widgets on PreviewWin.
        """
            
        if self.PreviewWin is None:
            self.PreviewWin = PreviewWin( self.MainWin, grid_gui=self )
            self.target_app.set_PreviewWin( self.PreviewWin )
            self.target_app.set_Notebook( self.grid_notebook )
        else:
            if allow_destroy_children:
                self.PreviewWin.destroy_all_children()
                self.target_app.destroy_all_preview_widgets()
            
        
        widgetL = self.grid_notebook.make_complete_list_of_widgets()
        #print("========== PreviewWin Widget Info.")
        for w in widgetL:
            #print( w )
            (widget_type, widget_name, tab_label, row_target, col_target) = w
            
            self.target_app.maybe_add_component( widget_type=widget_type, 
                                                 widget_name=widget_name, 
                                                 tab_label=tab_label, 
                                                 row=row_target, col=col_target)
            self.target_app.show_preview()
        #print("="*55)
        #print('ref crc_reference =',self.target_app.crc_reference, 'current =', self.target_app.get_model_crc() )
            
        
                
    def add_menu_to_MainWin(self):
        
        # make menus
        self.menuBar = Menu(self.MainWin, relief = 'raised', bd=2)

        # create file pulldown menu
        fileMenu = Menu(self.menuBar, tearoff=0)
        fileMenu.add('command', label = 'New', command=self.newForm, underline=0,accelerator="Ctrl+N")
        fileMenu.add('command', label = 'Open', command=self.openFile, underline=0,accelerator="Ctrl+O")
        fileMenu.add('command', label = 'Save', command=self.saveasFile, underline=0,accelerator="Ctrl+S")
        #fileMenu.add('command', label = 'SaveAs', command = self.saveasFile)
        fileMenu.add('command', label = 'Exit', command=self.cleanupOnQuit, underline=0,accelerator="Ctrl+X")
        self.menuBar.add('cascade', label="File", menu=fileMenu)

        # create options pulldown menu
        optMenu = Menu(self.menuBar, tearoff=0)
        optMenu.add('command', label = 'Font to Clipboard', command =self.FontPickButton_Select, underline=0,accelerator="Ctrl+F")
        optMenu.add('command', label = 'Color to Clipboard', command = self.ColorPickButton_Select, underline=0,accelerator="Ctrl+C")
        optMenu.add('command', label = 'Named Color to Clipboard', command = self.NamedColorPickButton_Select, underline=0,accelerator="Ctrl+K")
        self.menuBar.add('cascade', label="Options", menu=optMenu)
        
        # bind accelerator keys (need lambda since functions don't have "event" parameter)
        self.root.bind("<Control-N>", lambda event: self.newForm())
        self.root.bind("<Control-n>", lambda event: self.newForm())
        
        self.root.bind("<Control-O>", lambda event: self.openFile())
        self.root.bind("<Control-o>", lambda event: self.openFile())
        
        self.root.bind("<Control-S>", lambda event: self.saveasFile())
        self.root.bind("<Control-s>", lambda event: self.saveasFile())
        
        self.root.bind("<Control-X>", lambda event: self.cleanupOnQuit())
        self.root.bind("<Control-x>", lambda event: self.cleanupOnQuit())
            
            
        self.root.bind("<Control-F>", self.FontPickButton_Click)
        self.root.bind("<Control-f>", self.FontPickButton_Click)
        
        self.root.bind("<Control-C>", self.ColorPickButton_Click)
        self.root.bind("<Control-c>", self.ColorPickButton_Click)
        
        self.root.bind("<Control-K>", self.NamedColorPickButton_Click)
        self.root.bind("<Control-k>", self.NamedColorPickButton_Click)

        # create About menu
        self.menuBar.add('command', label="About", command = self.About)

        # create Help menu
        self.menuBar.add('command', label="Help", command = self.Help)

        self.root.config(menu=self.menuBar)

    def mainOrDialog_Callback(self, varName, index, mode):
        #print( "mainOrDialog_Callback varName, index, mode",varName, index, mode )
        #print( "    new StringVar value =",self.MainWin.mainOrDialog.get() )
        
        self.refresh_preview_win()
        if self.MainWin.mainOrDialog.get() == 'dialog':
            if self.MainWin.hideOkChkBox_StringVar.get() == "yes":
                self.PreviewWin.remove_mock_OK_Cancel_Buttons()
            else:
                self.PreviewWin.add_mock_OK_Cancel_Buttons()
        else:
            self.PreviewWin.remove_mock_OK_Cancel_Buttons()
    
    def place_gui_definition_controls(self, frame2, MainWin ):
        
        # show option for Main Window or Dialog
        MainWin.mainOrDialog=StringVar()
        lbframe = LabelFrame(frame2, text="GUI Type")
        lbframe.pack(anchor=W)

        b = Radiobutton(lbframe, text="Main Window", value='main', variable=MainWin.mainOrDialog)
        b.pack(anchor=W)
        b = Radiobutton(lbframe, text="Dialog", value='dialog', variable=MainWin.mainOrDialog)
        b.pack(anchor=W)
        MainWin.mainOrDialog.set('main')
        self.mainOrDialog_traceName = MainWin.mainOrDialog.trace_variable("w", self.mainOrDialog_Callback)
        
        MainWin.hideOkChkBox = Checkbutton(lbframe, text="Hide OK Btn", width="15")
        MainWin.hideOkChkBox.pack(anchor=E, side=TOP)
        MainWin.hideOkChkBox_StringVar = StringVar()
        MainWin.hideOkChkBox_StringVar.set("no")
        MainWin.hideOkChkBox.configure(variable=MainWin.hideOkChkBox_StringVar, onvalue="yes", offvalue="no")
        self.hideOkChkBox_traceName = MainWin.hideOkChkBox_StringVar.trace_variable("w", self.hideOkChkBox_Callback)
        
        # show checkbox for menu and status bar
        lbframe = LabelFrame(frame2, text="Window Options")
        lbframe.pack(anchor=W)
        
        MainWin.menuChkBox = Checkbutton(lbframe, text="Main Menu", width="15")
        MainWin.menuChkBox.pack(anchor=W, side=TOP)
        MainWin.menuChkBox_StringVar = StringVar()
        MainWin.menuChkBox_StringVar.set("no")
        MainWin.menuChkBox.configure(variable=MainWin.menuChkBox_StringVar, onvalue="yes", offvalue="no")
        self.menuChkBox_traceName = MainWin.menuChkBox_StringVar.trace_variable("w", self.menuChkBox_Callback)
        
        MainWin.statusBarChkBox = Checkbutton(lbframe, text="Status Bar", width="15")
        MainWin.statusBarChkBox.pack(anchor=W, side=TOP)
        MainWin.statusBarChkBox_StringVar = StringVar()
        MainWin.statusBarChkBox_StringVar.set("no")
        MainWin.statusBarChkBox.configure(variable=MainWin.statusBarChkBox_StringVar, onvalue="yes", offvalue="no")
        self.statusBarChkBox_traceName = MainWin.statusBarChkBox_StringVar.trace_variable("w", self.statusBarChkBox_Callback)
        
        MainWin.resizableChkBox = Checkbutton(lbframe, text="Resizable", width="15")
        MainWin.resizableChkBox.pack(anchor=W, side=TOP)
        MainWin.resizableChkBox_StringVar = StringVar()
        MainWin.resizableChkBox_StringVar.set("yes")
        MainWin.resizableChkBox.configure(variable=MainWin.resizableChkBox_StringVar, onvalue="yes", offvalue="no")
        self.resizableChkBox_traceName = MainWin.resizableChkBox_StringVar.trace_variable("w", self.resizableChkBox_Callback)
        
        # show choices for standard dialogs
        lbframe = LabelFrame(frame2, text="Standard Dialogs")
        lbframe.pack(anchor=W)

        MainWin.stdDialMessChkBox = Checkbutton(lbframe, text="Messages", width="15")
        MainWin.stdDialMessChkBox.pack(anchor=E, side=TOP)
        MainWin.stdDialMessChkBox_StringVar = StringVar()
        MainWin.stdDialMessChkBox_StringVar.set("no")
        MainWin.stdDialMessChkBox.configure(variable=MainWin.stdDialMessChkBox_StringVar, onvalue="yes", offvalue="no")
        

        MainWin.stdDialColorChkBox = Checkbutton(lbframe, text="Color Choose", width="15")
        MainWin.stdDialColorChkBox.pack(anchor=E, side=TOP)
        MainWin.stdDialColorChkBox_StringVar = StringVar()
        MainWin.stdDialColorChkBox_StringVar.set("no")
        MainWin.stdDialColorChkBox.configure(variable=MainWin.stdDialColorChkBox_StringVar, onvalue="yes", offvalue="no")

        MainWin.stdDialFileChkBox = Checkbutton(lbframe, text="File Open/Save", width="15")
        MainWin.stdDialFileChkBox.pack(anchor=E, side=TOP)
        MainWin.stdDialFileChkBox_StringVar = StringVar()
        MainWin.stdDialFileChkBox_StringVar.set("no")
        MainWin.stdDialFileChkBox.configure(variable=MainWin.stdDialFileChkBox_StringVar, onvalue="yes", offvalue="no")

        MainWin.stdAlarmChkBox = Checkbutton(lbframe, text="Alarm Handler", width="15")
        MainWin.stdAlarmChkBox.pack(anchor=E, side=TOP)
        MainWin.stdAlarmChkBox_StringVar = StringVar()
        MainWin.stdAlarmChkBox_StringVar.set("no")
        MainWin.stdAlarmChkBox.configure(variable=MainWin.stdAlarmChkBox_StringVar, onvalue="yes", offvalue="no")
        
        # put color picker button
        self.ColorPickButton = Button(frame2, text="Put Color on Clipboard", width=18)
        self.ColorPickButton.pack(anchor=W, side=TOP)
        self.ColorPickButton.bind("<ButtonRelease-1>", self.ColorPickButton_Click)
        
        # put color picker button
        self.ColorPickButton = Button(frame2, text="   --> Named Color", width=18)
        self.ColorPickButton.pack(anchor=W, side=TOP)
        self.ColorPickButton.bind("<ButtonRelease-1>", self.NamedColorPickButton_Click)
        
        # put Font picker button
        self.FontPickButton = Button(frame2, text="Put Font on Clipboard", width=18)
        self.FontPickButton.pack(anchor=W, side=TOP)
        self.FontPickButton.bind("<ButtonRelease-1>", self.FontPickButton_Click)
        
        # put All widgets on notebook 
        #self.PlaceAllWidgetsButton = Button(frame2, text="Debug All Widgets", width=18)
        #self.PlaceAllWidgetsButton.pack(anchor=W, side=TOP)
        #self.PlaceAllWidgetsButton.bind("<ButtonRelease-1>", self.PlaceAllWidgetsButton_Click)
        
        # append new row or column to current notebook tab
        add_frame = Frame( frame2 )
        self.AddNewRowButton = Button(add_frame, text="Add Row", width=8)
        self.AddNewRowButton.pack(anchor=W, side=LEFT)
        self.AddNewRowButton.bind("<ButtonRelease-1>", self.AddNewRowButton_Click)

        self.AddNewColButton = Button(add_frame, text="Add Col", width=8)
        self.AddNewColButton.pack(anchor=W, side=LEFT)
        self.AddNewColButton.bind("<ButtonRelease-1>", self.AddNewColButton_Click)
        add_frame.pack(anchor=W, side=TOP)

        # dup_widget_label can be used for set_placement_widget_label, or widget duplication
        self.dup_widget_label_desc = Label(frame2, width=16)
        self.dup_widget_label_desc["text"      ] = "\nduplicate widget\nand its properties"
        self.dup_widget_label_desc.pack(anchor=W)
        
        self.dup_widget_label = Label(frame2, width=16)        
        self.dup_widget_label["text"      ] = "\n\n"
        self.dup_widget_label["font"      ] = ("Courier", 8, "normal")
        self.dup_widget_label["relief"] = "groove"
        self.dup_widget_label.pack(anchor=W)
        self.dup_widget_label_plain_bg = self.dup_widget_label["background"]
        self.dup_widget_label["background"] = "#FFFACD"  # lemonchiffon
        
        # Refresh Preview Window
        #self.PlaceAllWidgetsButton = Button(frame2, text="Refresh Preview", width=18)
        #self.PlaceAllWidgetsButton.pack(anchor=W, side=TOP)
        #self.PlaceAllWidgetsButton.bind("<ButtonRelease-1>", self.GeneralDebugButton_Click)

    def GeneralDebugButton_Click(self, event):
        self.grid_notebook.repaint_all_labels()
        self.refresh_preview_win()

    def AddNewRowButton_Click(self, event):
        self.grid_notebook.append_row()
        
    def AddNewColButton_Click(self, event):
        self.grid_notebook.append_column()
        

    def PlaceAllWidgetsButton_Click(self, event):
        """As DEBUG TOOL, show all widgets in Notebook"""
        
        saved_sel = self.MainWin.placementWidgetType_svar.get()
        saved_tab = self.grid_notebook.current_tab_label()
        
        row = 1 # row_interface
        col = 1 # col_interface
        
        self.grid_notebook.set_current_tab_by_label( "Main" )
        
        for wname, wcolor in CONTROLS:
            self.MainWin.placementWidgetType_svar.set( wname )
            event.widget = self.grid_notebook.interface_gridBoxWidgetD[("Main", row, col)]# row_interface, col_interface
            self.grid_notebook.onGridBoxClicked( event )
            
            if wname in ContainerControlsL:
                new_tab_name = wname + "_%i"%(CONTROL_NEXT_NUMBER_D[wname] -1,)
                self.grid_notebook.set_current_tab_by_label( new_tab_name )
                
                # place some widgets on ContainerControlsL tab
                if wname == 'RadioGroup':
                    self.MainWin.placementWidgetType_svar.set( "Label" )
                    event.widget = self.grid_notebook.interface_gridBoxWidgetD[(new_tab_name, 2, 2)]# row_interface, col_interface
                    self.grid_notebook.onGridBoxClicked( event )
                    
                    for n_radio in range(3):
                        self.MainWin.placementWidgetType_svar.set( "Radiobutton" )
                        event.widget = self.grid_notebook.interface_gridBoxWidgetD[(new_tab_name, 3+n_radio, 2)]# row_interface, col_interface
                        self.grid_notebook.onGridBoxClicked( event )
                        
                    
                else:
                    self.MainWin.placementWidgetType_svar.set( "Button" )
                    event.widget = self.grid_notebook.interface_gridBoxWidgetD[(new_tab_name, 2, 2)]# row_interface, col_interface
                    self.grid_notebook.onGridBoxClicked( event )
                    
                    self.MainWin.placementWidgetType_svar.set( "Label" )
                    event.widget = self.grid_notebook.interface_gridBoxWidgetD[(new_tab_name, 3, 2)]# row_interface, col_interface
                    self.grid_notebook.onGridBoxClicked( event )
                    
                    self.MainWin.placementWidgetType_svar.set( "Entry" )
                    event.widget = self.grid_notebook.interface_gridBoxWidgetD[(new_tab_name, 4, 2)]# row_interface, col_interface
                    self.grid_notebook.onGridBoxClicked( event )
                    
                # restore notebook to Main tab
                self.grid_notebook.set_current_tab_by_label( "Main" )
                
            
            col += 1
            if col % 5 == 0:
                col = 1
                row += 1
                
        # Return Listbox_1 selection to original value
        self.MainWin.placementWidgetType_svar.set( saved_sel )
        self.grid_notebook.set_current_tab_by_label( saved_tab )
        
    def set_status_msg(self, msg):
        self.MainWin.statusMessage.set( msg )

    def gray_out_listbox(self, omit_list=None):
        """if omit_list is None, gray all."""
        if omit_list is None:
            omit_list = []
            
        n = -1
        for index, (wname, wcolor) in enumerate(CONTROLS):
            if wname in omit_list:
                self.Listbox_1.itemconfig(index, fg="black")
                n = index
            else:
                self.Listbox_1.itemconfig(index, fg="gray")
            self.Listbox_1.selection_clear(index)
            
        if n >= 0:
            self.Listbox_1.selection_set(n)
            self.Listbox_1_Click( 'FromGrayOut' ) # event is not used in Listbox_1_Click
    
    def restore_black_listbox(self):
        """Make sure all listbox options show up for all other tabs."""
        
        n = 0
        for i in self.Listbox_1.curselection():
            n = i
            break # set to 1st value encountered
    
        for index, (wname, wcolor) in enumerate(CONTROLS):
            self.Listbox_1.itemconfig(index, fg="black")
            self.Listbox_1.selection_clear(index)
            
        self.Listbox_1.selection_set(n)
        self.Listbox_1_Click( 'FromRestoreBlack' ) # event is not used in Listbox_1_Click

    def select_preview_tab(self, tab_name_inp):
        
        if not self.PreviewWin:
            self.refresh_preview_win() # make PreviewWin if not already done.
            
        tab_comp = self.target_app.compObjD[tab_name_inp]
        notebook_name = tab_comp.tab_label
        nb_obj = self.target_app.compObjD[ notebook_name ]
        
        # get index of tab on preview_win        
        for itab, (row, col, tab_name, tab_label) in enumerate( nb_obj.tab_nameL ):
            if tab_name_inp == tab_name:
                nb_obj.pw_widget.native_widget.select( itab )
                #print('grid_gui.tab_of_notebook_changed: set PreviewWin Tab to:', itab)
                break

    def tab_of_notebook_changed(self, event):
        
        if self.mouse_location == 'preview_win':
            return
        
        # look at the dup widget to see if it's a full widget duplication
        s_dup = self.dup_widget_label["text"].strip()
        if s_dup and s_dup.startswith('('): # i.e. widget has a (row,col) position
            saved_dup_text_on_tab_change = self.dup_widget_label["text"]        
            saved_dup_bg_on_tab_change   = self.dup_widget_label["background"]
        else:
            saved_dup_text_on_tab_change = ''
            saved_dup_bg_on_tab_change   = ''
        
        nb = self.grid_notebook.notebook
        #i = nb.index(nb.select())
        nb_tab_label = nb.tab(nb.select(), "text")
        #print("GridGUI Notebook Tab Set to:", nb_tab_label )

        self.Listbox_1.config( state=NORMAL )

        # gray out some listbox options for RadioGroup
        if nb_tab_label.startswith('RadioGroup'):
            self.gray_out_listbox( omit_list=("Radiobutton","Label") )
                        
        elif nb_tab_label.startswith('Notebook'):
            #print('=========>  Need to add Notebook logic.')
            
            self.gray_out_listbox( omit_list=None )
            self.set_placement_widget_label( 'Tab' )
            self.set_status_msg( "Only Tabs can be added to Notebook" )
            
        else:
            # Make sure all listbox options show up for all other tabs.
            self.restore_black_listbox()
            
            if saved_dup_text_on_tab_change:
                self.dup_widget_label["text"      ] = saved_dup_text_on_tab_change
                self.dup_widget_label["background"] = saved_dup_bg_on_tab_change
                self.dup_widget_label_desc["text"      ] = "\nduplicate widget\nand its properties"
                

        # Cause PreviewWin to switch to same Tab
        if nb_tab_label in self.target_app.compObjD: # i.e. the tab is in the TargetTkAppDef
            w = self.target_app.compObjD[ nb_tab_label ]
            treeL = w.get_tab_label_tree()
            #print('New widget tab_label_tree =', treeL )
            for name in treeL:
                if name.startswith('Tab_'):
                    self.select_preview_tab( name ) # nb_tab_label is tab_name
            
            

    def place_widget_selection_listbox(self, frame1):
        """frame1 in topFrame contains Widgets selection ListBox"""
        
        self.MainWin.placementWidgetType_svar=StringVar()
        self.MainWin.placementWidgetType_svar.set('Button')
        
        # Notebooks handled seperately

        self.Listbox_1 = Listbox(frame1,width=15 ,height=str(len(CONTROLS)), selectmode='single')#, selectmode="extended")
        self.Listbox_1.bind("<ButtonRelease-1>", self.Listbox_1_Click)

        for wname, wcolor in CONTROLS:
            #b = Radiobutton(frame1, text=text, value=cont, variable=self.MainWin.placementWidgetType_svar)
            #b.pack(anchor=W)
            #print("inserting wname into Listbox_1 "+wname)
            self.Listbox_1.insert(END, wname)
        
        self.Listbox_1.pack(anchor=W)
        self.Listbox_1.select_set(0) # make Top Item highlighted
            
    def cleanupOnQuit(self):
                
        if self.target_app.model_has_changed():
            dialog = maybe_save_dialog(self.MainWin, "Save Before Exit?")
            
            if (dialog.result is not None) and ( dialog.result['save_file'] == "yes"):
                self.saveasFile()
                return
            else:
                # ignore any other warnings
                self.target_app.reset_crc_reference() # for detecting changes to model
        
        
        #print( 'Doing final cleanup before quitting' )
        self.MainWin.allow_subWindows_to_close = 1
        self.MainWin.destroy()
    
    def set_duplication_widget_label(self, label_obj):
        """Given the widget Label object, set up for making duplicates."""
        
        self.dup_widget_label["text"      ] = label_obj["text"]
        self.dup_widget_label["background"] = label_obj["background"]
        self.dup_widget_label_desc["text"      ] = "\nduplicate widget\nand its properties"
        
    
    def set_placement_widget_label(self, widget_type):
        """Sets dup_widget_label for a simple Place of widget_type."""
        
        self.dup_widget_label["text"      ] = "\n%s\n"%widget_type
        #self.dup_widget_label["background"] = self.dup_widget_label_plain_bg # "#FFFACD"  # lemonchiffon
        self.dup_widget_label["background"] = CONTROL_COLOR_D[widget_type]
        self.dup_widget_label_desc["text"      ] = "\n\nPlace %s"%widget_type

        self.grid_notebook.dup_source_widget_name = '' # not a dup_widget_label event so no dup_source_widget_name
        
        
    def Listbox_1_Click(self, event): #click method for component ID=1
        
        val = 'Button'
        for i in self.Listbox_1.curselection():
            val = self.Listbox_1.get(i)# .lower()
        
        self.set_status_msg("Selected Widget: "+ val )
                
        self.MainWin.placementWidgetType_svar.set(val)

        tab_label = self.grid_notebook.current_tab_label()
        if not tab_label.startswith('Notebook'):
            # set duplicate widget text and background to indicate normal placement
            self.set_placement_widget_label( val )

    def hideOkChkBox_Callback(self, varName, index, mode):
        #print( 'Hide OK Button in Dialog =',self.MainWin.hideOkChkBox_StringVar.get(), end="\n")
        
        try:
            self.target_app.setSpecialOption('hideokbutton', self.MainWin.hideOkChkBox_StringVar.get())
        except:
            pass

        if self.MainWin.hideOkChkBox_StringVar.get() == "yes":
            self.PreviewWin.remove_mock_OK_Cancel_Buttons()
        else:
            self.PreviewWin.add_mock_OK_Cancel_Buttons()

    def menuChkBox_Callback(self, varName, index, mode):
        #print( 'make menu =',self.MainWin.menuChkBox_StringVar.get(), end="\n")
        
        try:
            self.target_app.setSpecialOption('hasmenu', self.MainWin.menuChkBox_StringVar.get())
            #print('Setting Menu "hasmenu" Option To:',self.MainWin.menuChkBox_StringVar.get())
        except:
            print('WARNING... Failed To Properly Set "hasmenu" Option.')
        
        if not self.in_reading_mode:
            if self.MainWin.menuChkBox_StringVar.get()=='yes' and self.target_app:
                dialog = Menumaker(self.MainWin, "Define Menu Structure",
                    self.target_app.getSpecialOption('menu'))
                #print( dialog.result, end="\n")
                
                if type(dialog.result) == type({}):

                    add_menu_ctrl_keys = dialog.result.get('add_menu_ctrl_keys','yes')
                    self.target_app.setSpecialOption('add_menu_ctrl_keys', add_menu_ctrl_keys)

                    menuStr = dialog.result.get('menu','').strip()
                    if len( menuStr ) > 0:
                        self.target_app.setSpecialOption('menu',menuStr)
                        #print( 'Recording new Menu Definition', end="\n")
                        
                        
        if not self.PreviewWin:
            self.refresh_preview_win() # make PreviewWin if not already done.

        # delete menuBar
        if self.MainWin.menuChkBox_StringVar.get()=='no' and self.target_app:
            if (self.PreviewWin is not None):
                if self.PreviewWin.menuBar:
                    self.PreviewWin.delete_menu()

        # create menuBar
        if self.MainWin.menuChkBox_StringVar.get()=='yes' and self.target_app:
            if (self.PreviewWin is not None):
                if self.PreviewWin.menuBar:
                    self.PreviewWin.delete_menu() # delete so menuBar can be recreated
                    
                menuL = buildMenuSource( self.target_app.getSpecialOption( 'menu' ) )
                menuSrcL = getMenuSource( menuL, rootName='self'  )
                    
                self.PreviewWin.add_menu( menuSrcL )
        
        self.refresh_preview_win() # redraw the form window showing menu state.

        
    def statusBarChkBox_Callback(self, varName, index, mode):
        #print( 'Status Bar =',self.MainWin.statusBarChkBox_StringVar.get(), end="\n")
        
        try:
            self.target_app.setSpecialOption('hasstatusbar', self.MainWin.statusBarChkBox_StringVar.get())
        except:
            pass
            
        if not self.PreviewWin:
            self.refresh_preview_win() # make PreviewWin if not already done.
        
        # add statusbar to PreviewWin
        if self.MainWin.statusBarChkBox_StringVar.get()=='yes' and self.target_app:
            if (self.PreviewWin is not None):
                if not self.PreviewWin.statusbar:
                    self.PreviewWin.add_mock_statusbar()
                    
        # remove statusbar from PreviewWin
        if self.MainWin.statusBarChkBox_StringVar.get()=='no' and self.target_app:
            if (self.PreviewWin is not None):
                if  self.PreviewWin.statusbar:
                    self.PreviewWin.remove_mock_statusbar()
                    
        self.refresh_preview_win() # redraw the form window showing menu state.

    def resizableChkBox_Callback(self, varName, index, mode):
        #print( 'Status Bar =',self.MainWin.resizableChkBox_StringVar.get(), end="\n")
        
        try:
            self.target_app.setSpecialOption('resizable', self.MainWin.resizableChkBox_StringVar.get())
        except:
            pass
                    
        self.refresh_preview_win() # redraw the form window showing menu state.
        
                
    def ColorPickButton_Click(self, event): #put selected color on clipboard
        self.ColorPickButton_Select()
        
    def ColorPickButton_Select(self): #put selected color on clipboard
        self.set_status_msg('Place Selected Color on Clipboard')
        ctup,cstr = tkinter.colorchooser.askcolor(title='Place Selected Color on Clipboard')
        if cstr != None:
            self.set_status_msg('%s is on Clipboard'%cstr)
            self.ColorPickButton.clipboard_clear()
            self.ColorPickButton.clipboard_append(cstr)
            
            #print( 'color chosen=',cstr, end="\n")
                
    def NamedColorPickButton_Click(self, event): #put selected color on clipboard
        self.NamedColorPickButton_Select()
        
    def NamedColorPickButton_Select(self): #put selected color on clipboard
        self.set_status_msg('Place Named Color on Clipboard')
        
        dialog = named_color_picker(self.MainWin, title="Place Named Color on Clipboard")
        if dialog.result is not None:
            (_, _, _, _, _, _, cstr, name) = dialog.result["named_color"]
            
            self.set_status_msg('%s %s is on Clipboard'%(name, cstr) )
            self.ColorPickButton.clipboard_clear()
            self.ColorPickButton.clipboard_append(cstr)
            
    def FontPickButton_Click(self, event):
        self.FontPickButton_Select()
    
    def FontPickButton_Select(self):
        self.set_status_msg('Place Selected Font on Clipboard')
        dialog = get_cross_platform_font(self.MainWin, title="Get Font")
        if dialog.result is not None:
            font_str = dialog.result['full_font_str']
            
            # for example:    Comic\ Sans\ MS 20 bold roman
                
            self.set_status_msg('%s is on Clipboard'%font_str)
            self.ColorPickButton.clipboard_clear()
            self.ColorPickButton.clipboard_append(font_str)
            
            #print( 'font chosen=',font_str, end="\n")
            

    def Help(self):
        
        usage = """
        
Basic Usage: 
  Select Widget in Listbox with Left Click.
  Place Widget with Left Click in grid.

Edit Widget:
  Right Click Widget in Grid or Preview Window.

Move Widget:
  Left Button Drag and Drop in Grid.

Duplicate Widget: 
  Left Click Widget in Grid.
  Left Click in grid to place the duplicate.

Insert Row or Column with Left Click on "+" control.

Add Weight to row or column with "wt" control.

Select Corresponding Tab for Widgets in Frames, RadioGroups etc.
"""
        
        tkinter.messagebox.showinfo(
            "Help for TkGridGUI",
            usage)

    def About(self):
        tkinter.messagebox.showinfo(
            "About TkGridGUI v(%s)"%__version__,
            "TkGridGUI v(%s) is:\n\n"%__version__+\
            "A quick approach to\n"+\
            "building Tkinter applications.\n"+\
            "Written by Charlie Taylor\n"
        )
    
    def newForm(self):
        #print( "New Form" )
        
        if self.target_app.model_has_changed():
            dialog = maybe_save_dialog(self.MainWin, "Save Current File?")
            
            if (dialog.result is not None) and ( dialog.result['save_file'] == "yes" ):
                self.saveasFile()
                return

        self.current_fileFullName = '' # no file for now
        # leave path alone... self.current_filePath = '' # no file for now
        self.current_fileName = '' # no file for now

        self.MainWin.title( 'TkGridGUI: ' + self.current_fileName )
        
        if self.PreviewWin:
            self.PreviewWin.delete_menu()
            self.PreviewWin.remove_mock_statusbar()

        self.target_app.reinitialize()
        self.grid_notebook.initialize_NotebookGridDes()
        self.grid_notebook.notebook.bind("<<NotebookTabChanged>>", self.tab_of_notebook_changed)
        
        self.refresh_preview_win()
        
        # ignore any other warnings
        self.target_app.reset_crc_reference() # for detecting changes to model
        

    def openFile(self, fName=None):
        #print( 'Open File' )
                
        if self.target_app.model_has_changed():
            dialog = maybe_save_dialog(self.MainWin, "Save Current File?")
            
            if (dialog.result is not None) and (dialog.result['save_file'] == "yes"):
                self.saveasFile()
                return
            else:
                # ignore any other warnings
                self.target_app.reset_crc_reference() # for detecting changes to model

        
        self.in_reading_mode = True # when True, suppresses some automatic trace actions.
        if fName is None:
            
            if self.current_filePath:
                initialdir = self.current_filePath
            else:
                initialdir = '.'
            
            filetypes = [
                ('tkGridGUI definition','*.def'),
                ('Any File','*.*')]
            self.pathopen = tkinter.filedialog.askopenfilename(parent=self.MainWin, title='Open tkGridGUI file', 
                filetypes=filetypes, initialdir=initialdir)
            #print('self.pathopen =',self.pathopen)
        else:
            self.pathopen = os.path.abspath(fName)
        
        if self.pathopen:
            
            self.newForm() # clean up any leftovers from another job
            
            full_fname = os.path.abspath( self.pathopen )
            head,tail = os.path.split( full_fname )
            
            self.current_fileFullName = full_fname
            self.current_filePath = head
            self.current_fileName = tail
                        
            self.target_app.readAppDefFile( self.pathopen )

            #'hasmenu':'no', 
            self.MainWin.menuChkBox_StringVar.set( self.target_app.getSpecialOption( 'hasmenu' ) )

            #'hasstatusbar':'no',
            self.MainWin.statusBarChkBox_StringVar.set( self.target_app.getSpecialOption( 'hasstatusbar' ) )

            #'resizable':'no'
            self.MainWin.resizableChkBox_StringVar.set( self.target_app.getSpecialOption( 'resizable' ) )
            
            #'hideokbutton':'no'
            self.MainWin.hideOkChkBox_StringVar.set( self.target_app.getSpecialOption( 'hideokbutton' ) )

            #'guitype':'main',
            self.MainWin.mainOrDialog.set( self.target_app.getSpecialOption( 'guitype' ) )

            #'hasstddialmess':'no', 
            self.MainWin.stdDialMessChkBox_StringVar.set( self.target_app.getSpecialOption( 'hasstddialmess' ) )

            #'hasstddialcolor':'no', 
            self.MainWin.stdDialColorChkBox_StringVar.set( self.target_app.getSpecialOption( 'hasstddialcolor' ) )

            #'hasstddialfile':'no', 
            self.MainWin.stdDialFileChkBox_StringVar.set( self.target_app.getSpecialOption( 'hasstddialfile' ) )

            #'hasstdalarm':'no', 
            self.MainWin.stdAlarmChkBox_StringVar.set( self.target_app.getSpecialOption( 'hasstdalarm' ) )


            #for key,val in self.target_app.app_attrD.items():
            #    print('%20s %s'%(key, str(val).replace('\t','    ')))
            
            widgetL = [(c.widget_type, widget_name, c.tab_label, c.row, c.col) for widget_name,c in list(self.target_app.compObjD.items())]
            self.grid_notebook.set_complete_list_of_widgets( widgetL )
            
            if not self.PreviewWin:
                self.refresh_preview_win() # make PreviewWin if not already done.
            
            # maybe create menuBar
            if self.MainWin.menuChkBox_StringVar.get()=='yes' and self.target_app:
                if (self.PreviewWin is not None):
                    if self.PreviewWin.menuBar:
                        self.PreviewWin.delete_menu() # delete so menuBar can be recreated
                        
                    menuL = buildMenuSource( self.target_app.getSpecialOption( 'menu' ) )
                    menuSrcL = getMenuSource( menuL, rootName='self'  )
                        
                    self.PreviewWin.add_menu( menuSrcL )
            
            
            # maybe add statusbar to PreviewWin
            if self.MainWin.statusBarChkBox_StringVar.get()=='yes' and self.target_app:
                if (self.PreviewWin is not None):
                    if not self.PreviewWin.statusbar:
                        self.PreviewWin.add_mock_statusbar()
            
            if self.PreviewWin:
                w = self.target_app.getSpecialOption( 'width' )
                h = self.target_app.getSpecialOption( 'height' )
                x = self.target_app.getSpecialOption( 'x' )
                y = self.target_app.getSpecialOption( 'y' )
                
                if self.PreviewWin.statusbar:
                    y += 30
                
                self.PreviewWin.geometry( '%ix%i+%i+%i'%(w,h,x,y))
                #self.PreviewWin.geometry( '' ) # allow to resize after set to x,y
                self.PreviewWin.update_idletasks()
                
            self.MainWin.title( 'TkGridGUI: ' + self.current_fileName )

            self.target_app.reset_crc_reference() # for detecting changes to model

        self.in_reading_mode = False # when True, suppresses some automatic trace actions.
        
        self.refresh_preview_win() # redraw the form window showing menu state
        
        self.grid_notebook.notebook.bind("<<NotebookTabChanged>>", self.tab_of_notebook_changed)
        

        
    def saveasFile(self):
        #print( 'Save File to Disk' )
        self.set_status_msg('Save File to Disk')
        
        filetypes = [
            ('TkGridGUI','*.def'),
            ('Any File','*.*')]
        
        if self.current_fileName:
            fname = self.current_fileName
        else:
            fname = ''
                        
        if self.current_filePath:
            initialdir = self.current_filePath
        else:
            initialdir = '.'
            
        fsave = tkinter.filedialog.asksaveasfilename(parent=self.MainWin, title='Saving TkGridGUI Definition File', 
            initialfile=fname, filetypes=filetypes, initialdir=initialdir)
        
        if fsave:
            if not fsave.lower().endswith('.def'):
                fsave += '.def'
                    
            full_fname = os.path.abspath( fsave )
            head,tail = os.path.split( full_fname )
            
            self.current_fileFullName = full_fname
            self.current_filePath = head
            self.current_fileName = tail
            
            # set values in target_app

            #'hasmenu':'no', 
            self.target_app.setSpecialOption( 'hasmenu', self.MainWin.menuChkBox_StringVar.get() )

            #'hasstatusbar':'no',
            self.target_app.setSpecialOption( 'hasstatusbar' , self.MainWin.statusBarChkBox_StringVar.get() )

            #'resizable':'no'
            self.target_app.setSpecialOption( 'resizable', self.MainWin.resizableChkBox_StringVar.get() )

            #'guitype':'main',
            self.target_app.setSpecialOption( 'guitype', self.MainWin.mainOrDialog.get() )
            
            #'hideokbutton':'no'
            self.target_app.setSpecialOption( 'hideokbutton', self.MainWin.hideOkChkBox_StringVar.get() )

            #'hasstddialmess':'no', 
            self.target_app.setSpecialOption( 'hasstddialmess', self.MainWin.stdDialMessChkBox_StringVar.get() )

            #'hasstddialcolor':'no', 
            self.target_app.setSpecialOption( 'hasstddialcolor', self.MainWin.stdDialColorChkBox_StringVar.get() )

            #'hasstddialfile':'no', 
            self.target_app.setSpecialOption( 'hasstddialfile', self.MainWin.stdDialFileChkBox_StringVar.get() )

            #'hasstdalarm':'no', 
            self.target_app.setSpecialOption( 'hasstdalarm', self.MainWin.stdAlarmChkBox_StringVar.get() )
            
            # first save *.def file
            if self.target_app.saveAppDefFile( savePathName=self.current_fileFullName ):
                # if that goes OK, then save *.py file
                                
                self.MainWin.title( 'TkGridGUI: ' + self.current_fileName )
                
                sf = FormSource( self.target_app, self.MainWin, self )
                sf.saveToFile() # save *.py file
                
                head, tail = os.path.split( sf.sourceFile.pathopen )
                self.set_status_msg('Saved File: "%s" and "%s" in "%s"'%(self.current_fileName, tail, head) )
                
                self.target_app.reset_crc_reference() # for detecting changes to model
                
            else:
                self.set_status_msg("WARNING... *.def file save failed.  NO SAVE PERFORMED.")


def main():
    
    root = Tk()
    MainWin = root
    MainWin.title('Main Window')
    #MainWin.geometry('320x320+10+10')
    MainWin.config(background='#FFFACD')#'lemonchiffon': '#FFFACD'

    grid_gui = GridGUI( MainWin )
    
    MainWin.mainloop()

if __name__=="__main__":
    
    main()