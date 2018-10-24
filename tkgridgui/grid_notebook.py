#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
"""
Notebook widget where grid geometry manager layout is defined.

Each target position on the target GUI has a Tk widget type and generic name (like Button_1).

More proper names can be added later (e.g. Button_1 can be named as Button_SaveFile)
Detailed widget properties like color, style or text are assigned outside this file.
These widgets only define locations and widget type.
"""

import sys

    
from tkinter import *
import tkinter.messagebox
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu # ttk OptionMenu seems to be broken
from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Style, Notebook

from tkgridgui.edit_Dialog import Edit_Properties_Dialog
from tkgridgui.wt_select_Dialog import Wt_Select_Dialog
from tkgridgui.comp_tree import CNode, ComponentTree

supportedTkWidgetSet = set( ['Button', 'Canvas', 'Checkbutton', 
    'Combobox', 'Entry', 'Frame','Label', 'LabelFrame','Listbox', 'Message', 
    'Menubutton', 'Notebook' ,'OptionMenu','Progressbar',
    'Radiobutton', "RadioGroup", 'Scale', 'Separator', 'Spinbox', 'Text', 'Treeview', 'Tab'] )


CONTROLS = [
    ("Button",      "#7CFC00"), # lawngreen
    ("Canvas",      "#40E0D0"), # turquiose
    ("Checkbutton", "#66CDAA"), # mediumaquamarine
    ("Combobox",    "#CD853F"), # peru
    ("Entry",       "#3CB371"), # mediumseagreen
    ("Frame",       "#F0E68C"), # khaki
    ("Label",       "#FFA500"), # orange
    ("LabelFrame",  "#FF7F50"), # coral
    ("Listbox",     "#F08080"), # lightcoral
    ("Message",     "#D8BFD8"), # thistle
    ("Menubutton",  "#DA70D6"), # orchid
    ("Notebook",    "#FA8072"), # salmon
    ("OptionMenu",  "#9370DB"), # mediumpurple
    ("Progressbar", "#FF69B4"), # hotpink
    ("Radiobutton", "#FFFF00"), # yellow:    also alternate form
    ("RadioGroup",  "#FFD700"), # gold:      also alternate form
    ("Scale",       "#FF4500"), # orangered  both vertical and horizontal
    ("Separator",   "#DC143C"), # crimson    both vertical and horizontal
    ("Spinbox",     "#1E90FF"), # dodgerblue
    ("Text",        "#D2B48C"), # tan
    ("Treeview",    "#BC8F8F"), # rosybrown
    ]

ContainerControlsL = ['Frame','LabelFrame','Notebook','RadioGroup','Tab']

CONTROL_COLOR_D = {} # index=Control Name: value=color hex string (initialized from CONTROLS)
CONTROL_NEXT_NUMBER_D = {} # index=Control Name, value=next number for generic names

for widget_type, color in CONTROLS:
    CONTROL_COLOR_D[widget_type] = color
    CONTROL_NEXT_NUMBER_D[widget_type] = 1 # all start with 1

CONTROL_COLOR_D['Tab'] = '#cccccc'
CONTROL_NEXT_NUMBER_D['Tab'] = 1

def intCast( val=0 ):
    try:
        return int(val)
    except:
        return 0

MAX_NUM_COLS = 10
MAX_NUM_ROWS = 15

class NotebookGridDes( Frame ):
    """A ttk.Notebook used to design grid geometry manager layouts"""
    

    def __init__(self, grid_gui, mainFrame,  MainWin,  name='grid_notebook', num_cols=6, num_rows=10):
        """Create ttk.Notebook used to design grid geometry manager layouts"""
        
        self.grid_gui = grid_gui
        self.mainFrame = mainFrame
        self.MainWin = MainWin
        
        self.num_cols_inp = num_cols
        self.num_rows_inp = num_rows
        self.tab_num_rows_colsD = {} # index=tab_label: value=(num_row, num_cols)
        
        Frame.__init__(self, mainFrame, name=name)
        self.pack(expand=Y, fill=BOTH)
        
        self.notebook = None
        self.initialize_NotebookGridDes()
    
    def initialize_NotebookGridDes(self):
        self.tabLabelL = [] # list of notebook tabs in order of addition
        self.nbFrameL = [] # list of Frame objects for each tab in notebook
        
        # need to have widget dictionaries for each tab of notebook
        self.colInsertWidgetD = {} # index=(tab_label, col_interface): value=Label Widget
        self.rowInsertWidgetD = {} # index=(tab_label, row_interface): value=Label Widget

        self.colWeightsWidgetD = {} # index=(tab_label, col_interface): value=Label Widget
        self.rowWeightsWidgetD = {} # index=(tab_label, row_interface): value=Label Widget

        self.interface_gridBoxWidgetD = {} # index=(tab_label, row_interface, col_interface): value=Label Widget
        self.default_label_font = ("Courier", 8, "normal") # will be set when interface_gridBoxWidgetD is initialized
        
        # NOTE: row_target, col_target for defined_target_widgetD
        self.defined_target_widgetD = {}   # index=(tab_label, row_target, col_target): value=placementWidgetType or ''
        self.label_obj_from_nameD = {}     # index=widget_name (e.g. Button_1): 
        #                                    value=(tab_label, row_target, col_target, placementWidgetType, Labelobj)
        
        del self.notebook # start over
        self.notebook = Notebook(self, name='main')
        self.notebook.pack(fill=BOTH, expand=Y, padx=2, pady=3)
        
        self.current_label_being_edited = None # used as flag in onGridBoxLeave to maintain hightlight
        
        
        self.must_confirm_box_h = True
        self.box_h = 46  # initial guesstimate of widget height
        self.box_h3 = self.box_h // 3
        self.box_h23 = (self.box_h * 2) // 3
        
        self.must_confirm_box_w = True
        self.box_w = 116  # initial guesstimate of widget width
        self.box_w3 = self.box_w // 3
        self.box_w23 = (self.box_w * 2) // 3
        
        self.drag_set = set() # set of possible target widgets for drag and drop

        
        self.create_tab(tab_label="Main")
        #self.create_tab(tab_label="Test Frame")
        
    
    def highlight_grid_widget(self, widget_name):
        if widget_name in self.label_obj_from_nameD:
            _, _, _, _, label = self.label_obj_from_nameD[ widget_name ]
            label['font'] = ("Helvetica", 12, "bold italic underline")

    def unhighlight_grid_widget(self, widget_name):
        if widget_name in self.label_obj_from_nameD:
            _, _, _, _, label = self.label_obj_from_nameD[ widget_name ]
            label['font'] = self.default_label_font

    
    def set_label_text_bg_from_widget_name(self, widget_name, placementWidgetType, Labelobj, row_target, col_target):
        """Try to add some helpful info onto line3 of labels"""

        Labelobj["background"] = CONTROL_COLOR_D[ placementWidgetType ] # aka widget_type

        if widget_name not in self.label_obj_from_nameD:
            
            Labelobj["text"      ] = "(%d,%d)\n%s\n" % (row_target, col_target, widget_name)
        else:
            def fitted_line3( s ):
                if len(s)<15:
                    return s
                return s[:12] + '...'
            
            line3 = ''
            
            # only works if target_app has widget_name
            if widget_name in self.grid_gui.target_app.compObjD:
                c = self.grid_gui.target_app.compObjD[ widget_name ]
                text = c.user_tkOptionD.get('text','')
                
                if text and (text != widget_name):
                    line3 = fitted_line3( text )
                elif c.user_tkOptionD.get('docstring',''):
                    line3 = fitted_line3( c.user_tkOptionD.get('docstring','') )
            
            Labelobj["text"      ] = "(%d,%d)\n%s\n%s" % (row_target, col_target, widget_name, line3)
        
    
    def set_row_column_weights_from_target_app(self):
        """Needs to set all weight Label widgets to show row/col weights"""
        # self.colWeightsWidgetD = {} # index=(tab_label, col_interface): value=Label Widget
        
        # rowD and colD: index=(tab_label,row_target), value=wt
        rowD, colD = self.grid_gui.target_app.get_a_full_desc_of_weights()
        
        for (tab_label, col_interface), label in list(self.colWeightsWidgetD.items()):
            col_target = col_interface - 1
            if (tab_label, col_target) in colD:
                wt = colD[ (tab_label, col_target) ]
            else:
                wt = 0
            
            label["text"      ] = "col:%i\nwt:%s"%(col_target, wt)
            if wt > 0:
                label["background"] = "#ff6060"
            else:
                label["background"] = "#daa520" # goldenrod "#ff8080" # light coral
        
        for (tab_label, row_interface), label in list(self.rowWeightsWidgetD.items()):
            row_target = row_interface - 1
            if (tab_label, row_target) in rowD:
                wt = rowD[ (tab_label, row_target) ]
            else:
                wt = 0
            
            label["text"      ] = "row:%i\nwt:%s"%(row_target, wt)
            if wt > 0:
                label["background"] = "#ff6060"
            else:
                label["background"] = "#daa520" # goldenrod "#ff8080" # light coral
            
    def repaint_all_labels(self):
        
        # start by painting all label widgets lemonchiffon
        for tab_label in self.tabLabelL:
            num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
            
            for row_target in range( num_rows ):
                row_interface = row_target + 1
                for col_target in range( num_cols ):
                    col_interface = col_target + 1
                    label = self.interface_gridBoxWidgetD[ (tab_label, row_interface, col_interface) ]
                    label["text"      ] = "(%d,%d)\n\n" % (row_target, col_target)
                    label["background"] = "#FFFACD"  # lemonchiffon
            
        # place defined widgets where they belong        
        
        # save any info on rowspan and columnspan
        row_col_spanL = [] # do not place rowspan or columnspan on 1st pass. Save for 2nd pass.
        
        for widget_name, (tab_label, row_target, col_target, widget_type, label) in list(self.label_obj_from_nameD.items()):
            
            row_interface = row_target + 1
            col_interface = col_target + 1
            num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
            
            label = self.interface_gridBoxWidgetD[(tab_label, row_interface, col_interface)]
            self.set_label_text_bg_from_widget_name( widget_name, widget_type, label, row_target, col_target )
            #    label["text"      ] = "(%d,%d)\n%s\n" % (row_target, col_target, widget_name)
            #    label["background"] = CONTROL_COLOR_D[ widget_type ]

            
            # if any rowspan/columnspan, show them
            target_comp = self.grid_gui.target_app.compObjD[ widget_name ]
            rowspan    = max(1, intCast( target_comp.user_tkOptionD.get('rowspan',1) ))
            columnspan = max(1, intCast( target_comp.user_tkOptionD.get('columnspan',1) ))
            if rowspan>1 or columnspan>1:
                # need to show rowspan/columnspan grid labels.
                for i in range( int(columnspan) ):
                    for j in range( int(rowspan) ):
                        if i!=0 or j!=0:
                            col_interface = col_target + 1 + i
                            row_interface = row_target + 1 + j
                            
                            ctarg = col_target + i
                            rtarg = row_target + j
                            
                            # Make sure grid is big enough to hold span labels
                            
                            if (ctarg < num_cols) and (rtarg < num_rows):
                                # ignore any rowspan or columnspan that falls off the grid
                            
                                label = self.interface_gridBoxWidgetD[(tab_label, row_interface, col_interface)]
                                #label["text"      ] = "(%d,%d)\n%s\n%s" % (row_target, col_target, widget_name, '---SPAN---')
                                #label["background"] = CONTROL_COLOR_D[widget_type]
                                
                                if rowspan>1 and columnspan>1:
                                    text = "(%d,%d)\n%s\n%s" % (row_target, col_target, widget_name, 'col+rowspan')
                                elif rowspan>1:
                                    text = "(%d,%d)\n%s\n%s" % (row_target, col_target, widget_name, 'rowspan')
                                else:
                                    text = "(%d,%d)\n%s\n%s" % (row_target, col_target, widget_name, 'columnspan')
                                
                                bg = CONTROL_COLOR_D[widget_type]
                                
                                row_col_spanL.append( (label, text, bg, tab_label, row_interface, col_interface) )
                        
        if row_col_spanL:
            for (label, text, bg, tab_label, row_interface, col_interface) in row_col_spanL:
                if self.widget_is_empty(label):
                    label["text"      ] = text
                    label["background"] = bg
                else:
                    label = self.interface_gridBoxWidgetD[(tab_label, row_interface, col_interface)]
                    sL = label["text"].split('\n')
                    sL[-1] = '???SPAN ERROR???'
                    label["text"] = '\n'.join(sL)
                    label["background"] = "#ff9797"
        
    
    def set_complete_list_of_widgets(self, widgetL):
        """
        Start over with full list of tuples describing all the widgets.
        Tuples = (widget_type, widget_name, tab_label, row_target, col_target)
        """
        
        # put the widgets into order of dependency
        # widgetL = list of (c.widget_type, c.widget_name, c.tab_label, c.row, c.col)
        ct = ComponentTree()
        for (widget_type, widget_name, tab_label, row, col) in widgetL:
            c = self.grid_gui.target_app.compObjD[ widget_name ]
            ct.add_node( CNode(widget_name, tab_label, c) )
            
        cnodeL = ct.get_ordered_components()
        cL = [cnode.component for cnode in cnodeL]
        widgetL = [(c.widget_type, c.widget_name, c.tab_label, c.row, c.col) for c in cL ]
        
        #print("NOTE... called set_complete_list_of_widgets.")
        #print( widgetL )
        
        self.initialize_NotebookGridDes()

        for widget_type, color in CONTROLS:
            CONTROL_NEXT_NUMBER_D[widget_type] = 1 # all start with 1
        CONTROL_NEXT_NUMBER_D['Tab'] = 1
        
        # set CONTROL_NEXT_NUMBER_D values to match input list of widgets
        for (widget_type, widget_name, tab_label, row_target, col_target) in widgetL:
            try:
                num = int( widget_name.split('_')[-1] )
                CONTROL_NEXT_NUMBER_D[widget_type] = max(num+1, CONTROL_NEXT_NUMBER_D[widget_type])
            except:
                print("ERROR... Widget Number is SURELY Screwed Up.")
                print( (widget_type, widget_name, tab_label, row_target, col_target) )
                
        # create any widgets and/or tabs
        row_col_spanL = [] # do not place rowspan or columnspan on 1st pass. Save for 2nd pass.
        for (placementWidgetType, widget_name, tab_label, row_target, col_target) in widgetL:
            
            # If widget is a ContainerControlsL, then create a tab on Notebook 
            #                ['Frame','LabelFrame','Notebook','RadioGroup']
            if (placementWidgetType in ContainerControlsL) and (widget_name not in self.tabLabelL):
                self.create_tab(tab_label=widget_name)
            elif tab_label not in self.tabLabelL:
                self.create_tab(tab_label=tab_label)

            # make sure the grid is big enough
            num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
            if col_target >= num_cols:
                self.set_current_tab_by_label( tab_label )
                for ic in range(num_cols, col_target+1):
                    self.insert_column( ic )
            if row_target >= num_rows:
                self.set_current_tab_by_label( tab_label )
                for ir in range(num_rows, row_target+1):
                    self.insert_row( ir )


            self.defined_target_widgetD[(tab_label, row_target, col_target)] = placementWidgetType
            row_interface, col_interface = row_target+1, col_target+1
            
            label = self.interface_gridBoxWidgetD[(tab_label, row_interface, col_interface)]
            self.set_label_text_bg_from_widget_name( widget_name, placementWidgetType, label, row_target, col_target )
            #    label["text"      ] = "(%d,%d)\n%s\n" % (row_target, col_target, widget_name)
            #    label["background"] = CONTROL_COLOR_D[placementWidgetType]
            
            self.label_obj_from_nameD[ widget_name ] = (tab_label, row_target, col_target, placementWidgetType, label)
                    

        # repaint the NotebookGridDes Labels
        self.repaint_all_labels()
        
        # refresh the PreviewWin
        self.grid_gui.refresh_preview_win()
            
    
    def make_complete_list_of_widgets(self):
        """Return info about all of the placed widgets"""
        widgetL = []
        
        for widget_name, (tab_label, row_target, col_target, widget_type, label) in list(self.label_obj_from_nameD.items()):
            widgetL.append( (widget_type, widget_name, tab_label, row_target, col_target) )
        
        return widgetL
        
    def current_tab_label(self):
        """return the label of the current tab."""
        return self.notebook.tab(  self.notebook.select(), 'text' )
    
    def current_tab_index(self):
        """return the index of the current tab."""
        return self.notebook.index('current')
    
    def set_current_tab_by_label(self, tab_label):
        """Switch to the tab with label "tab_label"."""
        try:
            i = self.tabLabelL.index( tab_label )
        except:
            i = 0
            self.set_status_msg( "Error... could not find tab label " + tab_label, also_print=True)
        self.notebook.select(i)
    
    def get_tab_index_by_label(self, tab_label):
        """return the tab index for label "tab_label"."""
        try:
            i = self.tabLabelL.index( tab_label )
        except:
            i = 0
            self.set_status_msg( "Error... could not find tab label " + tab_label, also_print=True)
        return i

    
    def find_empty_space_on_tab(self, tab_label):
        """return a (row_target, col_target) on "tab_label" notebook page."""
        try:
            i = self.tabLabelL.index( tab_label )
        except:
            self.set_status_msg( "Error... could not find tab label OR empty space " + tab_label, also_print=True)
            return (None, None)
        
        num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
        
        # search all locations for an empty spot
        for col_target in range( num_cols ):
            for row_target in range( num_rows ):
                # index=(tab_label, row_target, col_target): value=placementWidgetType
                if self.defined_target_widgetD[(tab_label, row_target, col_target)] == '':
                    return (row_target, col_target)

        # if nothing found, then issue a warning and return (None, None)
        self.set_status_msg( "Error... could not empty space on: " + tab_label, also_print=True)
        return (None, None)
        
        

    def set_status_msg(self, msg, also_print=False):
        """Set the status message in the  main window"""
        if also_print:
            print( msg )
        
        self.MainWin.statusMessage.set( msg )
    
    def make_col_control(self, tab_label, col_interface):
        """Make a control Label on "tab_label" for column."""
        
        i_tab = self.get_tab_index_by_label( tab_label )
        nbFrame = self.nbFrameL[ i_tab ]
        
        col_target = col_interface - 1
        
        label = Label(nbFrame, width=16)
        s = "col:%i"%col_target
        label["text"      ] = "+" + s.center(14," ") + "+"
        label["font"      ] = self.default_label_font
        label["background"] = "#87CEFA" # lightskyblue
        label["relief"] = "raised"
        
        self.colInsertWidgetD[tab_label, col_interface] = label
        
        label.grid(row=0, column=col_interface)

        label.bind("<Button-1>", self.onColInsertClicked)
        label.bind("<Enter>", self.onColControlEnter)
        label.bind("<Leave>", self.onControlLeave)
        label.bind("<Motion>", self.onColControlMove)
        
        # Put column weight controls below widget labels
        row_weight_controls = 99
        
        label = Label(nbFrame, width=8)
        label["text"      ] = "col:%i\nwt:0"%col_target
        label["font"      ] = ("Courier", 10, "normal")
        label["background"] = "#daa520" # goldenrod "#ff8080" # light coral
        label["relief"] = "raised"
        
        self.colWeightsWidgetD[tab_label, col_interface] = label
        
        label.grid(row=row_weight_controls, column=col_interface)
        
        label.bind("<Button-1>", self.onSetColumnWeightClicked)
        
        
    
    def make_row_control(self, tab_label, row_interface):
        """Make a control Label on "tab_label" for row."""
        
        i_tab = self.get_tab_index_by_label( tab_label )
        nbFrame = self.nbFrameL[ i_tab ]
        
        row_target = row_interface - 1
        
        label = Label(nbFrame, width=8)
        label["text"      ] =  "+\nrow:%i\n+"%row_target
        label["font"      ] = self.default_label_font
        label["background"] = "#87CEFA" # lightskyblue
        label["relief"] = "raised"
        
        self.rowInsertWidgetD[tab_label, row_interface] = label
        
        label.grid(row=row_interface, column=0)

        label.bind("<Button-1>", self.onRowInsertClicked)   
        label.bind("<Enter>", self.onRowControlEnter)
        label.bind("<Leave>", self.onControlLeave)
        label.bind("<Motion>", self.onRowControlMove)
        
        # Put row weight controls below widget labels
        col_weight_controls = 99
        
        label = Label(nbFrame, width=8)
        label["text"      ] =  "row:%i\nwt:0"%row_target
        label["font"      ] = ("Courier", 10, "normal")
        label["background"] = "#daa520" # goldenrod "#ff8080" # light coral
        label["relief"] = "raised"
        
        self.rowWeightsWidgetD[tab_label, row_interface] = label
        
        label.grid(row=row_interface, column=col_weight_controls)
        
        label.bind("<Button-1>", self.onSetRowWeightClicked)


    def target_grid_is_empty(self, tab_label, row_target, col_target):
        """See if position on notebook tab_label is empty"""
        if self.defined_target_widgetD[(tab_label, row_target, col_target)]:
            return False
        else:
            return True
            
    def current_grid_is_empty(self, row_target, col_target):
        """See if position on CURRENT notebook tab_label is empty"""
        tab_label = self.current_tab_label()
        return self.target_grid_is_empty( tab_label, row_target, col_target )
    
    def widget_is_empty(self, widget):
        """Given a Label widget, see if it is available for widget placement"""
        sL = widget["text"].split('\n')
        if len(sL)==3:
            if sL[1].strip() == '':
                return True
        return False
    
    def widget_is_container(self, label_widget):
        _, _, widget_name, _ = self.get_all_widget_info( label_widget )
        _, _, _, widget_type, _ = self.label_obj_from_nameD.get( widget_name, '' )
        
        if widget_type in ContainerControlsL:
            return True
        else:
            return False
    
    def get_widget_type(self, label_widget):
        _, _, widget_name, _ = self.get_all_widget_info( label_widget )
        _, _, _, widget_type, _ = self.label_obj_from_nameD.get( widget_name, '' )
        return widget_type
    
    def get_widget_rc_target(self, widget):
        """Given a Label widget, get the row_target, col_target from the "text" string."""
        
        # assume that the Label is in the field of target widgets
        sL = widget["text"].split('\n')
        row, col = sL[0][1:-1].split(',')  # get row col from string like "(7,8)"
        row_target, col_target = int(row), int(col)
        return row_target, col_target

    #def get_widget_rc_target_from_name(self, name): # name is like Button_3
    #    """Given a Label widget, get the row_target, col_target from the "text" string."""
    #    (tab_label, rtarg, col_target, placementWidgetType, label) = self.label_obj_from_nameD[name]
    #    return self.get_widget_rc_target( label )

    
    def get_all_widget_info(self, label_widget):
        """Given a Label widget, get the row_target, col_target, name and line3 from the "text" string."""
        
        # assume that the Label is in the field of target widgets
        sL = label_widget["text"].split('\n')
        row, col = sL[0][1:-1].split(',')  # get row col from string like "(7,8)"
        row_target, col_target = int(row), int(col)
        
        widget_name = sL[1]
        line3 = sL[2]
        
        return row_target, col_target, widget_name, line3
        
    #def get_all_widget_info_from_name(self, name): # name is like Button_3
    #    """Given a widget name, get the row_target, col_target, name and line3 from the "text" string."""
    #    (tab_label, rtarg, col_target, placementWidgetType, label) = self.label_obj_from_nameD[name]
    #    return self.get_all_widget_info( label )

    def make_target_grid_label(self, tab_label, row_target, col_target):
        """
        Add a Label object to represent target GUI grid location.
        These positions are all empty right now.
        """
        
        i_tab = self.get_tab_index_by_label( tab_label )
        nbFrame = self.nbFrameL[ i_tab ]
        
        row_interface = row_target + 1
        col_interface = col_target + 1

        label = Label(nbFrame, width=16)
        label["text"      ] = "(%d,%d)\n\n" % (row_target, col_target)
        label["font"      ] = self.default_label_font
        label["background"] = "#FFFACD"  # lemonchiffon
        label["relief"] = "groove"
        
        self.interface_gridBoxWidgetD[(tab_label, row_interface,col_interface)] = label
        self.defined_target_widgetD[(tab_label, row_target, col_target)] = ''
        
        label.grid(row=row_interface, column=col_interface)

        label.bind("<Enter>", self.onGridBoxEnter)
        label.bind("<Leave>", self.onGridBoxLeave)
        label.bind("<Button-1>", self.onGridBoxClicked)   

        label.bind("<Button-3>", self.onGridBoxRightClicked)   


        label.bind('<B1-Motion>', self.onLeftDrag)
        label.bind("<ButtonRelease-1>", self.onLeftDrop)

  
    def onLeftDrag(self, event):
        #print( 'Got left mouse button drag:',)
        #print( 'Widget=%s X=%s Y=%s' % (event.widget["text"].replace('\n',' '), event.x, event.y))
        
        xroot = event.widget.winfo_rootx()
        yroot = event.widget.winfo_rooty()
        
        try:
            w2 = self.winfo_containing(event.x+xroot, event.y+yroot)
            #print( '... Widget#2=%s' % (w2["text"].replace('\n',' '),))
        except:
            w2 = None
        
        # restore any Labels that were dragged over
        for w in self.drag_set:
            if w != w2:
                if self.widget_is_empty( w ):
                    w["background"] = "#FFFACD"  # lemonchiffon
                    #print('Restore Empty',w["text"].replace('\n',' '))
                else:
                    widget_type = self.get_widget_type(w)
                    w["background"] = CONTROL_COLOR_D[ widget_type ]
                    #print('Restore Widget',w["text"].replace('\n',' '))
        self.drag_set.clear()
        
        # set background of potential drop target Label
        if w2 is not None and (w2 != event.widget):
            self.drag_set.add( w2 )
            if self.widget_is_empty( w2 ) or self.widget_is_container(w2):
                w2["background"] =  "#FF00FF"  # magenta
         
    def onLeftDrop(self, event):
        
        xroot = event.widget.winfo_rootx()
        yroot = event.widget.winfo_rooty()
        
        # w2 is Label object that event.widget is dropped upon
        w2 = self.winfo_containing(event.x+xroot, event.y+yroot)
        #print('xxxDropped Widget=%s on %s'% (event.widget["text"].replace('\n',' '), w2["text"].replace('\n',' ')))
        
        # Might be here from simple Click. Check for any drag_set members before using Drop Logic.
        if self.drag_set:
            
            old_row_target, old_col_target, widget_name, line3 = self.get_all_widget_info( event.widget )
            new_row_target, new_col_target = self.get_widget_rc_target( w2 )
            
            # only try to move if there is an actual movement
            if (old_row_target != new_row_target) or ( old_col_target != new_col_target):
                
                if widget_name.startswith('Tab_'):
                    self.grid_gui.target_app.arrange_notebook_tabs( widget_name, new_row_target, new_col_target )
                
                s = 'Dropped Widget=%s on %s'% (event.widget["text"].replace('\n',' '), w2["text"].replace('\n',' '))
                self.set_status_msg(s)
                self.move_widget_on_current_tab( event.widget, new_row_target, new_col_target, w2)
                
                self.repaint_all_labels()
        
    def move_widget_on_current_tab(self, widget, new_row_target, new_col_target, w2):
        """Move widget from current location to new location. (might move to another tab)"""
        
        tab_label = self.current_tab_label()

        # w2 is Label object that widget is dropped upon
        if self.target_grid_is_empty( tab_label, new_row_target, new_col_target):
            w2_type = ''
        else:
            w2_row_target, w2_col_target, w2_name, w2_line3 = self.get_all_widget_info( w2 )
            w2_type = self.defined_target_widgetD[(tab_label, w2_row_target, w2_col_target)]
        
        
        # can only move to target location if it is empty.
        if w2_type == '':
        
            old_row_target, old_col_target, widget_name, line3 = self.get_all_widget_info( widget )
            placementWidgetType = self.defined_target_widgetD[(tab_label, old_row_target, old_col_target)]
            
            # clear the old location
            self.defined_target_widgetD[(tab_label, old_row_target, old_col_target)] = ''
            widget["text"      ] = "(%d,%d)\n\n" % (old_row_target, old_col_target)
            widget["font"      ] = self.default_label_font
            widget["background"] = "#FFFACD"  # lemonchiffon
            
            # set up the new location
            self.defined_target_widgetD[(tab_label, new_row_target, new_col_target)] = placementWidgetType
            new_row_interface, new_col_interface = new_row_target + 1, new_col_target + 1
            
            self.label_obj_from_nameD[ widget_name ] = (tab_label, new_row_target, new_col_target, placementWidgetType, widget)
            
            label = self.interface_gridBoxWidgetD[(tab_label, new_row_interface, new_col_interface)]
            
            self.set_label_text_bg_from_widget_name( widget_name, placementWidgetType, label, new_row_target, new_col_target )
            #    label["text"      ] = "(%d,%d)\n%s\n" % (row_target, col_target, widget_name)
            #    label["background"] = CONTROL_COLOR_D[placementWidgetType]
        
            s = "Moved widget "+widget_name+" at (%s,%i,%i)"%(tab_label, old_row_target, old_col_target) +\
                " to (%s,%i,%i)"%(tab_label, new_row_target, new_col_target)
            #print(s)
            self.set_status_msg(s)
            
            self.grid_gui.refresh_preview_win()
        
        elif self.widget_is_container( w2 ) and (w2 != widget) : # move to container's tab
            
            old_row_target, old_col_target, widget_name, line3 = self.get_all_widget_info( widget )
            
            w2_type = self.get_widget_type( w2 )
            w2["background"] = CONTROL_COLOR_D[ w2_type ]
            
            # if current position on current tab is open on new tab, put it there
            if self.target_grid_is_empty( w2_name, old_row_target, old_col_target):
                new_row_target, new_col_target = old_row_target, old_col_target
            else:
                new_row_target, new_col_target = self.find_empty_space_on_tab( w2_name )
            
            if new_row_target is not None: # i.e. if a place was found on the other tab.
                
                old_row_target, old_col_target, widget_name, line3 = self.get_all_widget_info( widget )
                placementWidgetType = self.defined_target_widgetD[(tab_label, old_row_target, old_col_target)]
                
                # clear the old location
                self.defined_target_widgetD[(tab_label, old_row_target, old_col_target)] = ''
                widget["text"      ] = "(%d,%d)\n\n" % (old_row_target, old_col_target)
                widget["font"      ] = self.default_label_font
                widget["background"] = "#FFFACD"  # lemonchiffon
                
                # set up the new location
                self.defined_target_widgetD[(w2_name, new_row_target, new_col_target)] = placementWidgetType
                new_row_interface, new_col_interface = new_row_target + 1, new_col_target + 1
                
                self.label_obj_from_nameD[ widget_name ] = (w2_name, new_row_target, new_col_target, placementWidgetType, widget)
                
                label = self.interface_gridBoxWidgetD[(w2_name, new_row_interface, new_col_interface)]
                self.set_label_text_bg_from_widget_name( widget_name, placementWidgetType, label, row_target, col_target )
                #    label["text"      ] = "(%d,%d)\n%s\n" % (row_target, col_target, widget_name)
                #    label["background"] = CONTROL_COLOR_D[placementWidgetType]
                
            
            s = 'Moved widget "%s" to tab_label "%s" (%s,%s)'%(widget_name, w2_name, new_row_target, new_col_target)
            #print("="*55)
            #print( s )
            #print("="*55)
            self.set_status_msg( s )
            
            self.grid_gui.refresh_preview_win()
        
        else:
            s = "Error... tried to move widget to Occupied Target Location (%i,%i)"%(new_row_target, new_col_target)
            #print( s )
            self.set_status_msg( s )
        

    def create_tab(self, tab_label="New Tab"):
        """Add new tab to grid notebook for Label objects."""
        
        nbFrame = Frame(self.notebook, name='panel_%i'%len(self.tabLabelL) )
        self.tabLabelL.append( tab_label )
        self.nbFrameL.append( nbFrame )
        
        nbFrame.pack(side=TOP, fill=BOTH, expand=Y)
        
        # Place Row and Col controls that Insert or Delete Rows and Cols
        for row_interface in range(1, self.num_rows_inp+1):
            self.make_row_control( tab_label, row_interface)
                        
        for col_interface in range(1, self.num_cols_inp+1):
            self.make_col_control( tab_label, col_interface )

        # add grid labels
        """Show only num_row x num_col widgets... i.e. No scroll currently available"""
        self.tab_num_rows_colsD[ tab_label ] = (self.num_rows_inp, self.num_cols_inp)
        for row_target in range( self.num_rows_inp ):
            for col_target in range( self.num_cols_inp ):
                self.make_target_grid_label( tab_label, row_target, col_target)

        # add tab to notebook
        self.notebook.add(nbFrame, text=tab_label, underline=0, padding=2)
        #print("tabs() =", self.notebook.tabs())
    
    def append_column(self):
        """Append a column to the grid of the current notebook tab."""
        tab_label = self.current_tab_label()
        
        # increase number of columns for current tab
        num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
        num_cols += 1
        self.tab_num_rows_colsD[ tab_label ] = (num_rows, num_cols)
        
        end_col_interface = num_cols # NEED num_cols for EACH TAB
        self.make_col_control( tab_label, end_col_interface )
        
        # add another column at the end with the right (col,row) label
        end_col_target = end_col_interface - 1
        for row_target in range( num_rows ):
            self.make_target_grid_label( tab_label, row_target, end_col_target)
    
    def insert_column(self, col_target):
        """Insert a column into the grid of the current notebook tab."""
        tab_label = self.current_tab_label()
        
        num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
        if num_cols >= MAX_NUM_COLS:
            tkinter.messagebox.showinfo("Insert Warning...",
                "Can NOT have more than %i columns\n\n"%MAX_NUM_COLS\
                +"For now, simply use Frame objects to expand the grid area.")
            return
        
        self.append_column()
        # ----------------------------
        
        # make a copy of current widget info
        copy_defined_target_widgetD = self.defined_target_widgetD.copy()   # index=(tab_label, row_target, col_target): value=placementWidgetType or ''
        copy_label_obj_from_nameD = self.label_obj_from_nameD.copy()       # index=widget_name: value=(tab_label, row_target, col_target, placementWidgetType, Labelobj)
        
        # empty out the main data
        self.defined_target_widgetD = {}   # index=(tab_label, row_target, col_target): value=placementWidgetType
        for key in list(copy_defined_target_widgetD.keys()):
            self.defined_target_widgetD[key] = ''
            
        self.label_obj_from_nameD = {}     # index=widget_name: value=(tab_label, row_target, col_target, placementWidgetType, Labelobj)
        
        for widget_name,(wtab_label, wrow_target, wcol_target, placementWidgetType, wLabelobj) in list(copy_label_obj_from_nameD.items()):
            
            placementWidgetType = copy_defined_target_widgetD[ (wtab_label, wrow_target, wcol_target) ]
            
            if (tab_label==wtab_label) and (wcol_target>=col_target):
                
                self.label_obj_from_nameD[ widget_name ] = (wtab_label, wrow_target, wcol_target+1, placementWidgetType, wLabelobj)
                target_comp = self.grid_gui.target_app.compObjD[ widget_name ]
                target_comp.row = target_comp.col + 1
                
                self.defined_target_widgetD[ (wtab_label, wrow_target, wcol_target+1) ] = placementWidgetType
                
                #if self.grid_gui.PreviewWin is not None:
                #    self.grid_gui.PreviewWin.widget_ijD[wrow_target, wcol_target+1] =\
                #        self.grid_gui.PreviewWin.widget_ijD[wrow_target, wcol_target]# index=(i,j) grid position: value=widget
                #    del self.grid_gui.PreviewWin.widget_ijD[wrow_target, wcol_target]
                
            else:
                self.label_obj_from_nameD[ widget_name ] = (wtab_label, wrow_target, wcol_target, placementWidgetType, wLabelobj)
                
                self.defined_target_widgetD[ (wtab_label, wrow_target, wcol_target) ] = placementWidgetType
            
    
        self.repaint_all_labels()
        self.grid_gui.refresh_preview_win()
        self.set_status_msg('Inserted Column at col:%s'%col_target)
    
    def append_row(self):
        """Append a new row at the bottom of the current notebook tab."""
        tab_label = self.current_tab_label()
        
        # increase number of rows for current tab
        num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
        num_rows += 1
        self.tab_num_rows_colsD[ tab_label ] = (num_rows, num_cols)
        
        end_row_interface = num_rows # NEED num_rows for EACH TAB
        self.make_row_control( tab_label, end_row_interface )
        
        # add another row at the end with the right (col,row) label
        end_row_target = end_row_interface - 1
        for col_target in range( num_cols ):
            self.make_target_grid_label( tab_label, end_row_target, col_target)
    
    def insert_row(self, row_target):
        """Insert a row into the grid of the current notebook tab."""
        tab_label = self.current_tab_label()
        
        
        num_rows, num_cols = self.tab_num_rows_colsD[ tab_label ]
        if num_rows >= MAX_NUM_ROWS:
            tkinter.messagebox.showinfo("Insert Warning...",
                "Can NOT have more than %i rows\n\n"%MAX_NUM_ROWS\
                +"For now, simply use Frame objects to expand the grid area.")
            return
        
        
        self.append_row()
        
        # ----------------------------
        
        # make a copy of current widget info
        copy_defined_target_widgetD = self.defined_target_widgetD.copy()   # index=(tab_label, row_target, col_target): value=placementWidgetType
        copy_label_obj_from_nameD = self.label_obj_from_nameD.copy()       # index=widget_name: value=(tab_label, row_target, col_target, placementWidgetType, Labelobj)
        
        # empty out the main data
        self.defined_target_widgetD = {}   # index=(tab_label, row_target, col_target): value=placementWidgetType
        for key in list(copy_defined_target_widgetD.keys()):
            self.defined_target_widgetD[key] = ''
        
        self.label_obj_from_nameD = {}     # index=widget_name: value=(tab_label, row_target, col_target, placementWidgetType, Labelobj)
        
        for widget_name,(wtab_label, wrow_target, wcol_target, placementWidgetType, wLabelobj) in list(copy_label_obj_from_nameD.items()):
            
            placementWidgetType = copy_defined_target_widgetD[ (wtab_label, wrow_target, wcol_target) ]
            
            if (tab_label==wtab_label) and (wrow_target>=row_target):
                
                self.label_obj_from_nameD[ widget_name ] = (wtab_label, wrow_target+1, wcol_target, placementWidgetType, wLabelobj)
                target_comp = self.grid_gui.target_app.compObjD[ widget_name ]
                target_comp.row = target_comp.row + 1
                
                self.defined_target_widgetD[ (wtab_label, wrow_target+1, wcol_target) ] = placementWidgetType
                
            else:
                self.label_obj_from_nameD[ widget_name ] = (wtab_label, wrow_target, wcol_target, placementWidgetType, wLabelobj)
                
                self.defined_target_widgetD[ (wtab_label, wrow_target, wcol_target) ] = placementWidgetType
            
    
        self.repaint_all_labels()
        self.grid_gui.refresh_preview_win()
        self.set_status_msg('Inserted Row at row:%s'%row_target)
    
    def onSetColumnWeightClicked(self, event):
        tab_label = self.current_tab_label()
        
        sL = event.widget["text"].split('\n') # weight labels have 2 lines
        col = int( sL[0].split(':')[-1] )
        
        #print( "Set Weight for Column %i"%col, ' on tab ',tab_label )
        
        dialog = Wt_Select_Dialog(self.master, "Column %i Weight"%col)
        
        if dialog.result is not None:
            wt = intCast( dialog.result['weight'] )
            
            self.grid_gui.target_app.set_a_col_weight(tab_label, col, wt)

            event.widget["text"      ] =  "col:%i\nwt:%s"%(col, wt)
            if wt > 0:
                event.widget["background"] = "#ff6060"
            else:
                event.widget["background"] = "#daa520" # goldenrod "#ff8080" # light coral
                
            self.grid_gui.refresh_preview_win()

            self.set_status_msg('Set Column Weight=%s at col:%s'%(wt, col) )

    
    def onSetRowWeightClicked(self, event):
        tab_label = self.current_tab_label()
        
        sL = event.widget["text"].split('\n') # weight labels have 2 lines
        row = int( sL[0].split(':')[-1] )
        
        #print( "Set Weight for Row %i"%row, ' on tab ',tab_label )
        
        dialog = Wt_Select_Dialog(self.master, "Row %i Weight"%row)
        
        if dialog.result is not None:
            wt = intCast( dialog.result['weight'] )
            
            self.grid_gui.target_app.set_a_row_weight(tab_label, row, wt)

            event.widget["text"      ] =  "row:%i\nwt:%s"%(row, wt)
            if wt > 0:
                event.widget["background"] = "#ff6060"
            else:
                event.widget["background"] = "#daa520" # goldenrod "#ff8080" # light coral

            self.grid_gui.refresh_preview_win()

            self.set_status_msg('Set Row Weight=%s at row:%s'%(wt, row) )

    # mouse clicked widget
    def onColInsertClicked(self, event):
        """Col Control is Clicked.  Will Insert or Delete a Col"""
        tab_label = self.current_tab_label()
        
        #print( 'Clicked "%s" Column Control.'%tab_label )
        #print("    event x,y =", event.x, event.y)
        #print("    widget w,h =", event.widget.winfo_width(), event.widget.winfo_height())

        sL = event.widget["text"].split() # col labels are a single line
        col_target = int( sL[1].strip().split(':')[-1] )

        x = int( event.x )
        if x < self.box_w3:
            #print("   Insert a new col at col_target #%i"%col_target)
            self.set_status_msg("Insert a new col at col_target #%i"%col_target)
            
            self.insert_column( col_target )
        elif x > self.box_w23:
            self.set_status_msg("Insert a new col at col_target #%i"%(col_target+1) )
            
            self.insert_column( col_target+1 )
        else:
            self.set_status_msg("")

    # mouse clicked widget
    def onRowInsertClicked(self, event):
        """Row Control is Clicked. Will Insert or Delete a Row."""
        tab_label = self.current_tab_label()
        
        #print( 'Clicked "%s" Row Control.'%tab_label )
        #print("    event x,y =", event.x, event.y)
        #print("    widget w,h =", event.widget.winfo_width(), event.widget.winfo_height())

        sL = event.widget["text"].split('\n') # row labels have 3 lines
        row = int( sL[1].strip().split(':')[-1] )

        y = int( event.y )
        
        if y < self.box_h3:
            #print("   Insert a new row at row #%i"%row)
            self.set_status_msg("Insert a new row at row #%i"%row)
            self.insert_row( row )
        elif y > self.box_h23:
            self.set_status_msg("Insert a new row at row #%i"%(row+1))
            self.insert_row( row+1 )
        else:
            self.set_status_msg("")

    def onRowControlMove(self, event):
        """Movement inside a Row Control.  Changes cursor for Insert and Delete."""
        y = int( event.y )
        
        if y < self.box_h3:
            #print(y,"<",self.box_h3)
            event.widget.config(cursor='plus')
        elif y > self.box_h23:
            #print(y,">",self.box_h23)
            event.widget.config(cursor='plus')
        else:
            #print(self.box_h3,"<",y,"<",self.box_h3)
            event.widget.config(cursor='arrow')

    def onColControlMove(self, event):
        """Movement inside a Col Control.  Changes cursor for Insert and Delete."""
        x = int( event.x )
        
        if x < self.box_w3:
            #print(x,"<",self.box_h3)
            event.widget.config(cursor='plus')
        elif x > self.box_w23:
            #print(x,">",self.box_h23)
            event.widget.config(cursor='plus')
        else:
            #print(self.box_h3,"<",x,"<",self.box_h3)
            event.widget.config(cursor='arrow')


    # mouse is over a widget
    def onRowControlEnter(self, event):
        """When cursor moves inside a Row Control.  Changes widget border relief."""
        event.widget["relief"] = "sunken"

        # confirm box height on first entry
        if self.must_confirm_box_h:
            self.must_confirm_box_h = False
            self.box_h =  event.widget.winfo_height()
            self.box_h3 = self.box_h // 3
            self.box_h23 = (self.box_h * 2) // 3
            
    # mouse is over a widget
    def onColControlEnter(self, event):
        """When cursor moves inside a Col Control.  Changes widget border relief."""
        event.widget["relief"] = "sunken"
        
        # confirm box width on first entry
        if self.must_confirm_box_w:
            self.must_confirm_box_w = False
            self.box_w = event.widget.winfo_width()
            self.box_w3 = self.box_w // 3
            self.box_w23 = (self.box_w * 2) // 3
        
    # mouse is leaving a widget
    def onControlLeave(self, event):
        """Restore widget border relief when cursor leaves Row or Col Control."""
        event.widget["relief"] = "raised"

    # mouse is over a widget
    def onGridBoxEnter(self, event):
        """When cursor moves inside a Grid Box change widget border relief."""
        event.widget["relief"] = "ridge"
        #event.widget["borderwidth"] = 3
        #event.widget["padx"] = 0
        #event.widget["pady"] = 0
        
        background = event.widget.cget("background")
        if background == "#FFFACD":
            event.widget["background"] = "#FFFFEE"

        if self.must_confirm_box_h:
            self.must_confirm_box_h = False
            self.box_h =  event.widget.winfo_height()
            self.box_h3 = self.box_h // 3
            self.box_h23 = (self.box_h * 2) // 3
            
            self.must_confirm_box_w = False
            self.box_w = event.widget.winfo_width()
            self.box_w3 = self.box_w // 3
            self.box_w23 = (self.box_w * 2) // 3
            
        # highlight widget in PreviewWin
        if not self.widget_is_empty(event.widget):
            _, _, widget_name, _ = self.get_all_widget_info( event.widget )
            if widget_name in self.grid_gui.target_app.compObjD:
                target_comp = self.grid_gui.target_app.compObjD[ widget_name ]
                
                target_comp.highlight_pw_widget()

    def set_label_widget_background(self, label_widget):
        
        tab_label = self.current_tab_label()
        row_target, col_target = self.get_widget_rc_target( label_widget )
        placementWidgetType = self.defined_target_widgetD[(tab_label, row_target, col_target)]
        
        if placementWidgetType:
            label_widget["background"] = CONTROL_COLOR_D[placementWidgetType]
        else:
            label_widget["background"] = "#FFFACD"  # lemonchiffon
        

    # mouse is leaving a widget
    def onGridBoxLeave(self, event):
        """Restore Grid Box border relief when cursor leaves."""
        
        if event.widget == self.current_label_being_edited:
            return
        
        event.widget["relief"] = "groove"
        #event.widget["borderwidth"] = 2
        #event.widget["padx"] = 1
        #event.widget["pady"] = 1
        
        self.set_label_widget_background( event.widget )
        
        # return PreviewWin widget to normal
        if not self.widget_is_empty(event.widget):
            _, _, widget_name, _ = self.get_all_widget_info( event.widget )
            if widget_name in self.grid_gui.target_app.compObjD:
                target_comp = self.grid_gui.target_app.compObjD[ widget_name ]
                
                target_comp.unhighlight_pw_widget()

    # mouse clicked widget
    def onGridBoxClicked(self, event):
        """
        Detect a Click on Label widget in main grid.
        Each Label widget represents GUI widget that will be added to created GUI.
        """
        
        tab_label = self.current_tab_label()
        
        row_target, col_target = self.get_widget_rc_target( event.widget )
        
        row_interface, col_interface = row_target+1, col_target+1
        #print('row_target=%d, col_target=%d'%(row_target, col_target))
        #print("Clicked (%i,%i)"%(row_target, col_target ),' on ',tab_label)
        
        #print("self.defined_target_widgetD = ",self.defined_target_widgetD)
        
        # see what widget is selected for placement on the main form
        # (might be placing a duplicate of a selected widget)
        s_dup = self.grid_gui.dup_widget_label["text"].strip()
        
        if tab_label.startswith('Notebook'):
            placementWidgetType = 'Tab'
            self.dup_source_widget_name = ''
            self.set_status_msg(" Only Tab Inserts Allowed on Notebook" , also_print=True)
                    
        elif s_dup and s_dup.startswith('('): # i.e. widget has a (row,col) position
            sL = self.grid_gui.dup_widget_label["text"].split('\n')
            
            # save source widget name for use in target_tk_app_def.TargetTkAppDef making widget
            self.dup_source_widget_name = sL[1]
            placementWidgetType = self.dup_source_widget_name.split('_')[0]
            
        else:
            placementWidgetType = self.MainWin.placementWidgetType_svar.get()
            self.dup_source_widget_name = ''
        
        # ======================= PlacementWidgetType decided =======================
        # Check for existing widget at grid location row, col in current tab_label
        if ((tab_label, row_target, col_target) in self.defined_target_widgetD) and \
           self.defined_target_widgetD[(tab_label, row_target, col_target)]:

            # get widget_type for widget already in (tab_label, row_target, col_target)
            ptype = self.defined_target_widgetD[ (tab_label, row_target, col_target) ]
            self.set_status_msg(ptype + " Widget is at (%i, %i) "%(row_target, col_target) )
            #print( ptype + " Widget is at (%s, %i, %i) "%(tab_label, row_target, col_target) )
            
            # toggle dup_widget_label if already set to this choice
            if self.grid_gui.dup_widget_label["text"      ] == event.widget["text"]:
                # set duplicate widget back to plain
                #self.grid_gui.dup_widget_label["text"      ] = "\n\n"
                #self.grid_gui.dup_widget_label["background"] = self.grid_gui.dup_widget_label_plain_bg # "#FFFACD"  # lemonchiffon
        
                val = self.grid_gui.MainWin.placementWidgetType_svar.get()
                self.grid_gui.set_placement_widget_label( val )
                
            else:
                self.grid_gui.set_duplication_widget_label( event.widget )
            
            
        else: # If row,col is empty, place a new widget here.
            
            # if it's a legal widget, (i.e. is in tkWidgets Dictionary), place it.
            if placementWidgetType in supportedTkWidgetSet:
                
                num_widget = CONTROL_NEXT_NUMBER_D[placementWidgetType]
                CONTROL_NEXT_NUMBER_D[placementWidgetType] += 1
                widget_name = placementWidgetType + "_%i"%num_widget
                
                if tab_label.startswith('Notebook'):
                    # tell target_app about the new tab
                    self.grid_gui.target_app.add_tab_to_notebook(row_target, col_target, widget_name, tab_label) # tab_label is Notebook_XXX
                                
                self.defined_target_widgetD[(tab_label, row_target, col_target)] = placementWidgetType
                
                label = self.interface_gridBoxWidgetD[(tab_label, row_interface, col_interface)]
                self.set_label_text_bg_from_widget_name( widget_name, placementWidgetType, label, row_target, col_target )
                #    label["text"      ] = "(%d,%d)\n%s\n" % (row_target, col_target, widget_name)
                #    label["background"] = CONTROL_COLOR_D[placementWidgetType]
                
                self.label_obj_from_nameD[ widget_name ] = (tab_label, row_target, col_target, placementWidgetType, label)
            
                self.set_status_msg("Placing widget "+placementWidgetType+" at (%s, %i,%i)"%(tab_label, row_target, col_target))
                #print( ("Placing widget "+placementWidgetType+" at (%s, %i,%i)"%(tab_label, row_target, col_target)) )
                
                # If widget is a ContainerControlsL, then create a tab on Notebook 
                #                ['Frame','LabelFrame','Notebook','RadioGroup']
                if placementWidgetType in ContainerControlsL:
                    self.create_tab(tab_label=widget_name)
                    
                self.grid_gui.refresh_preview_win()
                self.repaint_all_labels()
                
            else:
                self.set_status_msg("Widget "+placementWidgetType+" NOT Recognized", also_print=True)

    # right button click
    def onGridBoxRightClicked(self, event):
        """
        Detect a RightClick on Label widget in current grid.
        If the Label widget is assigned, then it will be edited.
        """
        
        tab_label = self.current_tab_label()
        
        row_target, col_target = self.get_widget_rc_target( event.widget )
        
        row_interface, col_interface = row_target+1, col_target+1
        #print('row_target=%d, col_target=%d'%(row_target, col_target))
        #print("Clicked (%i,%i)"%(row_target, col_target ),' on ',tab_label)
        
        #print("self.defined_target_widgetD = ",self.defined_target_widgetD)
        
        # see what widget is selected for placement on the main form
        placementWidgetType = self.MainWin.placementWidgetType_svar.get()
        #print("placementWidgetType = " + placementWidgetType)
        
        # Check for existing widget at grid location row, col in current tab_label
        if ((tab_label, row_target, col_target) in self.defined_target_widgetD) and \
           self.defined_target_widgetD[(tab_label, row_target, col_target)]:

            # get widget_type for widget already in (tab_label, row_target, col_target)
            ptype = self.defined_target_widgetD[ (tab_label, row_target, col_target) ]
            self.set_status_msg('Editing ' +ptype + " Widget at (%i, %i) "%(row_target, col_target) )
            #print( ptype + " Widget is at (%s, %i, %i) "%(tab_label, row_target, col_target) )
            
            # get label object, and set up for any property editing
            label = self.interface_gridBoxWidgetD[(tab_label, row_interface, col_interface)]
            
            # prepare to call property editor
            _, _, widget_name, _ = self.get_all_widget_info( label )
            
            self.highlight_grid_widget( widget_name )
                        
            
            # get default and user properties
            if 1:#self.grid_gui.PreviewWin is not None:
                
                target_comp = self.grid_gui.target_app.compObjD[ widget_name ]
                dialogOptionsD = {}
                for key,val in list(target_comp.default_tkOptionD.items()):
                    dialogOptionsD[key] = (val, "def.")
                    
                for key,val in list(target_comp.user_tkOptionD.items()): # user_tkOptionD holds tk options set by user. (i.e. not same as default_tkOptionD)
                    dialogOptionsD[key] = (val, "USER VALUE")
            
                dialogOptionsD['child_widget_list'] = self.grid_gui.target_app.get_names_of_containers_widgets( widget_name )
            
                # highlight widget on PreviewWin
                target_comp.highlight_pw_widget() # onGridBoxLeave tries to override this when Edit_Properties_Dialog is called.
                
                #self.grid_gui.PreviewWin.update()
                    
            #else:
            #    dialogOptionsD = None
            #    target_comp = None                
            
            # call property editor
            
            self.current_label_being_edited = event.widget # used as flag in onGridBoxLeave to maintain hightlight
            
            dialog = Edit_Properties_Dialog(self.master, widget_name, dialogOptionsD=dialogOptionsD)

            self.current_label_being_edited = None # used as flag in onGridBoxLeave to maintain hightlight

            def unhighlight_edited_widget():
                # restore label on grid to normal
                self.unhighlight_grid_widget( widget_name )
                if target_comp is not None:
                    target_comp.unhighlight_pw_widget()
            
            # use dialog results to set properties
            if dialog.result is None:
                self.master.after( 500, unhighlight_edited_widget ) # give user half a sectond to see highlight
            else:
                # check for delete widget command
                if ("DeleteWidget" in dialog.result) and (dialog.result["DeleteWidget"]=="yes"):
                    
                    unhighlight_edited_widget()
                    
                    _, _, _, widget_type, _ = self.label_obj_from_nameD.get( widget_name, '' )
                    
                    if widget_type in ContainerControlsL:
                        
                        self.grid_gui.target_app.removeContainerByName( widget_name )
                        
                    else:
                        #print("Deleting ",widget_name)
                        self.delete_widget_by_name( widget_name )
                        self.grid_gui.target_app.delComponentByName( widget_name )
                                        
                else: # not deleting, so update user_tkOptionD for widget
                    self.master.after( 500, unhighlight_edited_widget ) # give user half a sectond to see highlight
                    
                    #print('grid_notebook dialog.result =',dialog.result)
                    if target_comp is not None:
                        target_comp.user_tkOptionD.update( dialog.result )
                        if  target_comp.widget_type != "Tab":
                            target_comp.set_user_properties()
        
                    # need to repostion Canvas Label
                    if target_comp.widget_type == "Canvas":
                        target_comp.pw_widget.native_widget.delete( 'all' )
                        w = int(target_comp.user_tkOptionD['width'])
                        h = int(target_comp.user_tkOptionD['height'])
                        target_comp.pw_widget.native_widget.create_text(w//2,h//2, text=target_comp.widget_name, 
                                                                        fill="black", width=w, anchor='center')
                    elif  target_comp.widget_type == "Tab":
                        self.grid_gui.target_app.change_notebook_tab_label( target_comp.widget_name, target_comp.user_tkOptionD['text'] )
                        
                        self.grid_gui.refresh_preview_win()

                        
                # reinitialize display
                #widgetL = [(c.widget_type, widget_name, c.tab_label, c.row, c.col) for widget_name,c in self.grid_gui.target_app.compObjD.items()]
                self.repaint_all_labels( )
                
                if self.grid_gui.PreviewWin is not None:
                    self.grid_gui.PreviewWin.maybe_resize_preview_win()

            
            
    def delete_widget_by_name(self, widget_name):
        
        (tab_label, row_target, col_target, placementWidgetType, label) = self.label_obj_from_nameD[ widget_name ]

        if placementWidgetType in ContainerControlsL:
            self.set_status_msg("Can NOT delete Containeer Widget "+placementWidgetType+\
                                " at (%s,%i,%i)"%(tab_label, row_target, col_target), also_print=True)
                                    
            tkinter.messagebox.showinfo("Delete Warning...",
                "Can NOT delete Containeer Widget "+placementWidgetType+'\n\n'+\
                " at (%s,%i,%i)"%(tab_label, row_target, col_target))
                                    
        else:
            # if this is just added, reset numbering in CONTROL_NEXT_NUMBER_D
            num_widget = int( widget_name.split('_')[-1] )
            if CONTROL_NEXT_NUMBER_D[placementWidgetType] == num_widget + 1:
                CONTROL_NEXT_NUMBER_D[placementWidgetType] = num_widget
                
            self.defined_target_widgetD[(tab_label, row_target, col_target)] = ''
            
            label["text"      ] = "(%d,%d)\n\n" % (row_target, col_target)
            label["background"] = "#FFFACD"  # lemonchiffon
            
            del self.label_obj_from_nameD[ widget_name ]
        
            self.set_status_msg("Deleted widget "+placementWidgetType+\
                                " at (%s,%i,%i)"%(tab_label, row_target, col_target), also_print=True)
                
            self.grid_gui.refresh_preview_win()
                

        
        
if __name__ == '__main__':
    
    from tkgridgui.target_tk_app_def import TargetTkAppDef
    from tkgridgui.preview_win import PreviewWin
    
    class MockGridGUI(object):
        def __init__(self, MainWin):
            self.MainWin = MainWin
            topFrame = Frame( MainWin ) # frame for controls

            self.grid_frame = Frame(topFrame) 
            self.grid_notebook = NotebookGridDes( self, self.grid_frame, MainWin, num_cols=6, num_rows=10)
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
            
    
            MainWin.placementWidgetType_svar=StringVar()
            MainWin.placementWidgetType_svar.set('Button')
            MainWin.bind("<Key>", self.key_set_placement_widget)
            
            self.target_app = TargetTkAppDef( name='myApp')
            self.PreviewWin = None
        
        def key_set_placement_widget(self, event):
            """When the user hits a number key, set the placementWidgetType to that index of CONTROLS"""
            try:
                i = int( event.char )
                MainWin.placementWidgetType_svar.set( CONTROLS[i][0] )
                msg = 'placementWidgetType_svar set to:' + CONTROLS[i][0]
                #print( msg )
                self.MainWin.statusMessage.set( msg )
            except:
                pass
        
        def refresh_preview_win(self):
            """Get all widget info from grid_notebook and pass into to target_app."""
            if self.PreviewWin is None:
                self.PreviewWin = PreviewWin( self.MainWin )
                self.target_app.set_PreviewWin( self.PreviewWin )
                #self.grid_gui.PreviewWin = PreviewWin
            
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
    
    root = Tk()
    MainWin = root
    MainWin.title('Main Window')
    #MainWin.geometry('320x320+10+10')
    MainWin.config(background='#FFFACD')#'lemonchiffon': '#FFFACD'

    grid_gui = MockGridGUI( MainWin )
    
    MainWin.mainloop()    
    