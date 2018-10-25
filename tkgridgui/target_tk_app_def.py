#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
from builtins import str
"""
Define the target TK Application

Holds values of all controls on main GUI (grid_gui.GridGUI).
Provides Read and Save routines for full GUI definition.

Has not only widget types and locations from grid_notebook.NotebookGridDes,
  but also any additional property assignments that were made by EditWin.
"""

import os
import sys
import binascii

    
from tkinter import *
import tkinter.messagebox
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu # ttk OptionMenu seems to be broken
from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Style, Notebook
    
from tkgridgui.edit_options import get_properties_dict, set_attribute_if_possible
from tkgridgui.edit_Dialog import Edit_Properties_Dialog

from tkgridgui.grid_notebook import ContainerControlsL, intCast
from tkgridgui.config_file import ConfigInterface
from tkgridgui.comp_tree import CNode, ComponentTree
from tkgridgui.preview_win_widgets import PW_Widget, SCROLL_Y_WIDGETS, SCROLL_X_WIDGETS, tkWidgetsD

# the "width" property of these widgets refers to character width.
TEXT_WIDTH_WIDGETS = set(['Button','Checkbutton','Combobox','Entry','Label',  #'Listbox',
                          'Radiobutton','Spinbox','Text',"Message", "Menubutton", "Tab"])

reqd_variable_typeD = {'Entry':'StringVar', 'OptionMenu':'StringVar', 'Combobox':'StringVar', 
                       'Checkbutton':'StringVar', 'Menubutton':'StringVar',
                       'Radiobutton':'StringVar', 'Scale':'StringVar'}

DEBUG_PRINT = 0


def make_weights_dict_from_str( wt_str ):
    """return a dict with index=row or col: value=wt"""
    weightD = {} # index=row: value=wt
    sL = wt_str.split() # split string by spaces. may get multiple column settings
    for s in sL:
        cL = s.split(':') # each setting is of the form col:wt
        rc = intCast( cL[0] )
        wt = intCast( cL[-1] )
        weightD[rc] = wt
        
    return weightD
    
def add_entry_to_weight_str( rc_inp, wt_inp, current_str):
    """
    Reset string representation of tab_label row_weights or col_weights ("row:wt" or "col:wt") 
    If wt==0, then must remove any row entry other than 0.
    If the row is already present with a different wt, must detect it and change wt.
    """
    
    currentD = make_weights_dict_from_str( current_str ) # index=row: value=wt
        
    currentD[rc_inp] = wt_inp # may overwrite an existing value with 0
    
    full_str = ' '.join( ['%s:%s'%(rc,wt) for rc,wt in list(currentD.items()) if wt>0 ] )
    
    return full_str

class Component( object ):
    """Carries info for each widget in the target app."""
    
    def __str__(self):
        return '<%s, %s>'%(self.widget_name, self.tab_label)
    
    
    def __init__(self, widget_type="Button", widget_name="Button_1", tab_label="Main", 
                       row=1, col=1, target_app=None ):
                           
        self.widget_type = widget_type # like Button or Canvas 
        self.widget_name = widget_name # like Button_1 or Canvas_23
        self.tab_label = tab_label # tab names in NotebookGridDes ("Main" is main Frame in app)
        self.row = row
        self.col = col
        self.target_app = target_app # allows call-back to TargetTkAppDef
        
        self.default_tkOptionD = {} # holds default widget options when 1st created (used to detect changes to options)
        
        self.user_tkOptionD = {}    # holds tk options set by user. (i.e. not same as default_tkOptionD)
        
        self.user_tkOptionD['docstring'] = ''
        
        if widget_type != 'Tab':
            self.user_tkOptionD['sticky'] = ''
            self.user_tkOptionD['columnspan'] = ''
            self.user_tkOptionD['rowspan'] = ''
            
        # Containers might have row/col weights set
        if self.widget_type in ContainerControlsL:
            self.user_tkOptionD['row_weights'] = ''
            self.user_tkOptionD['col_weights'] = ''
            
        
        # Some widgets have special values that need to be set
        if widget_type == "Spinbox":
            self.user_tkOptionD['from_']  = 1
            self.user_tkOptionD['to'] = 10
        elif widget_type == "Radiobutton":
            self.user_tkOptionD['value'] = widget_name.split('_')[-1] # should be the Radiobutton number
        elif widget_type == "Combobox":
            self.user_tkOptionD['values'] = 'Mine Yours Ours'
        elif widget_type == "Separator":
            self.user_tkOptionD['sticky'] = 'ew' # Separator is invisible w/o sticky
        elif widget_type == 'Text':
            self.user_tkOptionD['scrolly'] = 'yes'
        elif widget_type in SCROLL_Y_WIDGETS:
            self.user_tkOptionD['scrolly'] = 'no' # only Text gets default 'yes'
            
        if widget_type in SCROLL_X_WIDGETS:
            self.user_tkOptionD['scrollx'] = 'no'
        
        
        # set a "reasonable" default width and height
        if widget_type in TEXT_WIDTH_WIDGETS:
            self.width_type  = "text"
            self.user_tkOptionD['text'] = widget_name
            
            if widget_type == 'Text':
                self.user_tkOptionD['width']  = 40
                self.user_tkOptionD['height'] = 12
            elif widget_type == "Message":
                self.user_tkOptionD['width'] = 55 # percent of message length
            elif widget_type == "Tab":
                pass
            else:
                self.user_tkOptionD['width'] = 15
                
        elif widget_type == "Listbox":
            self.user_tkOptionD['width']  = 18
            self.user_tkOptionD['height'] = 12
            
        elif widget_type == "OptionMenu":
            self.user_tkOptionD['width']  = 20
            self.user_tkOptionD['height'] = 2
            
        elif widget_type == "Menubutton":
            self.user_tkOptionD['width']  = 20
            self.user_tkOptionD['height'] = 2
            
        elif widget_type == "Treeview":
            pass
            
        elif widget_type == "Scale":
            pass
            
        elif widget_type == "Notebook":
            self.width_type  = "pixel"
            self.user_tkOptionD['width']  = 400
            self.user_tkOptionD['height'] = 300
            
            # Notebook Tab labels separated by \n
            self.user_tkOptionD['tab_labels'] = 'Mickey\nGoofy\nPopeye'
            
            self.tab_nameL = [] # tuples of Tab name and label, e.g. (row, col, Tab_1, text)
            
        else:
            self.width_type  = "pixel"
            self.user_tkOptionD['width']  = 60
            self.user_tkOptionD['height'] = 50
        
        self.pw_widget = None # use maybe_make_widget to create 
        self.disp_frame = None

        # may need a tk variable for PreviewWin
        tkvar_type = reqd_variable_typeD.get( self.widget_type, '' ) # e.g. StringVar
        self.tkvar = None
        self.tkvar_list = None # Menubutton has a list of tk variables
        if tkvar_type:
            try:
                if tkvar_type == "StringVar":
                    self.tkvar = StringVar()
                elif tkvar_type == "IntVar":
                    self.tkvar = IntVar()
                elif tkvar_type == "DoubleVar":
                    self.tkvar = DoubleVar()
                else:
                    print("ERROR... do not recognize tk variable type = ", tkvar_type)
                    
                if widget_type=="Menubutton":
                    self.tkvar_list = []
                    for _ in range(3):
                        self.tkvar_list.append( StringVar() )
            except:
                print("WARNING... Failed to make ",tkvar_type," for ",self.widget_name)

        
    def get_docstring(self):
        """For documenting generated source code."""
        
        loc_str = ' at %s(%s,%s)'%(self.tab_label, self.row, self.col)
        
        # if the user supplied a docstring, use it.
        if self.user_tkOptionD['docstring']:
            return '%12s: '%self.widget_type + self.user_tkOptionD['docstring'] + ' :' + loc_str
        
        # ---------------------
        text = self.user_tkOptionD.get('text', '')
        if text == self.widget_name:
            text = ''
        if text:
            return '%12s: '%self.widget_type + text + ' :' + loc_str
        
        # ---------------------
        value = self.user_tkOptionD.get('value', '')
        if value:
            return '%12s: '%self.widget_type + '%s'%value + ' :' + loc_str
        
        # ---------------------
        values = self.user_tkOptionD.get('values', '')
        if values:
            return '%12s: '%self.widget_type + '%s'%values + ' :' + loc_str
        
        # ---------------------
        from_ = '%s'%self.user_tkOptionD.get('from_', '')
        if from_:
            return '%12s: '%self.widget_type + from_ + ' to ' + '%s'%self.user_tkOptionD.get('to', '') + ' :' + loc_str

        # ---------------------
        return '%12s: '%self.widget_type + loc_str

    def highlight_pw_widget(self):
        
        if self.widget_type == "Tab":
            notebook_name = self.tab_label
            nb_obj = self.target_app.compObjD[ notebook_name ]
            if nb_obj.pw_widget is not None:
                nb_obj.pw_widget.pw_highlight_widget()
                print('target_app calling select_preview_tab with widget_name =', self.widget_name)
                self.target_app.grid_notebook.grid_gui.select_preview_tab( self.widget_name )
        
        elif self.pw_widget is not None:
            self.pw_widget.pw_highlight_widget()
            
    
    def highlight_grid_widget(self):
        if self.target_app.grid_notebook is not None:
            self.target_app.grid_notebook.highlight_grid_widget( self.widget_name )
    
    def highlight_widget(self): # highlight BOTH PreviewWin and grid_notebook
        self.highlight_pw_widget()
        self.highlight_grid_widget()
    
    def unhighlight_pw_widget(self):
        if self.widget_type == "Tab":
            notebook_name = self.tab_label
            nb_obj = self.target_app.compObjD[ notebook_name ]
            if nb_obj.pw_widget is not None:
                nb_obj.pw_widget.pw_unhighlight_widget()
        
        
        elif self.pw_widget is not None:
            self.pw_widget.pw_unhighlight_widget()
    
    def unhighlight_grid_widget(self):
        if self.target_app.grid_notebook is not None:
            self.target_app.grid_notebook.unhighlight_grid_widget( self.widget_name )
    
    def unhighlight_widget(self): # un-highlight BOTH PreviewWin and grid_notebook
        self.unhighlight_pw_widget()
        self.unhighlight_grid_widget()

    def widget_has_moved(self, tab_label="Main", row=1, col=1):
        """Test for widget having been moved"""
        if (tab_label, row, col) == (self.tab_label, self.row, self.col):
            return False
        else:
            return True

    def reset_location(self, tab_label="Main", row=1, col=1):
        self.tab_label = tab_label # tab names in NotebookGridDes ("Main" is main Frame in app)
        self.row = row
        self.col = col
        
    def maybe_make_widget(self, disp_frame):
        """If not already created, create the pw_widget"""
        
        # Tab should never get here.
        if self.pw_widget is None:
            
            self.disp_frame = disp_frame
                        
            # disp_frame is the native_widget of pw_widget's parent
            self.pw_widget = PW_Widget( disp_frame, self )
        
            self.set_widget_tk_properties()
            
            #if self.pw_widget is not None: bind preview widget
            self.pw_widget.native_widget.bind("<Button-3>", self.Widget_Right_Click)
            
            return True
        else:
            return False
                
    def Widget_Right_Click(self, __event): # event not used
        #print( "Widget_Right_Click on ",self.widget_name )

        # set tab of grid_notebook to this widget's tab_label
        nb_obj = self.target_app.grid_notebook
        nb_obj.set_current_tab_by_label( self.tab_label )

        self.highlight_widget()
        
        # put all pw_widget properties into dialogOptionsD for editing
        dialogOptionsD = {}
        for key,val in list(self.default_tkOptionD.items()):
            dialogOptionsD[key] = (val, "def.")
            
        for key,val in list(self.user_tkOptionD.items()): # user_tkOptionD holds tk options set by user. (i.e. not same as default_tkOptionD)
            dialogOptionsD[key] = (val, "USER VALUE")

        dialogOptionsD['child_widget_list'] = self.target_app.get_names_of_containers_widgets( self.widget_name )

        # get grid_notebook label object to highlight it.
        (tab_label, rtarg, col_target, placementWidgetType, label) = \
            self.target_app.grid_notebook.label_obj_from_nameD[ self.widget_name ]

        self.target_app.grid_notebook.current_label_being_edited = label # used as flag in onGridBoxLeave to maintain hightlight
        
        dialog = Edit_Properties_Dialog(self.target_app.grid_notebook.master, self.widget_name, dialogOptionsD=dialogOptionsD)

        self.target_app.grid_notebook.current_label_being_edited = None # used as flag in onGridBoxLeave to maintain hightlight

        self.unhighlight_widget()
            
        if dialog.result is not None:
            # check for delete widget command
            if ("DeleteWidget" in dialog.result) and (dialog.result["DeleteWidget"]=="yes"):
                    
                if self.widget_type in ContainerControlsL:
                    
                    self.target_app.removeContainerByName( self.widget_name )
                else:
                                
                    #print("Deleting ",self.widget_name)
                    self.target_app.grid_notebook.delete_widget_by_name( self.widget_name )
                    
                    self.target_app.delComponentByName( self.widget_name )
                
            else:
                #preview_comp = self.target_app.compObjD[ self.widget_name ]
                #print('target_app dialog.result =',dialog.result)
                self.user_tkOptionD.update( dialog.result )
                self.set_user_properties()
                
                #self.target_app.grid_notebook.grid_gui.refresh_preview_win()
                #self.target_app.PreviewWin.update_idletasks()
                #self.target_app.PreviewWin.update()  # <-- update idle tasks ??
                #self.target_app.PreviewWin.setActive()
                
                # need to repostion Canvas Label
                if self.widget_type == "Canvas":
                    self.pw_widget.native_widget.delete( 'all' )
                    w = int(self.user_tkOptionD['width'])
                    h = int(self.user_tkOptionD['height'])
                    self.pw_widget.native_widget.create_text(w//2,h//2, text=self.widget_name, 
                                                             fill="black", width=w, anchor='center')
                
            if self.target_app.PreviewWin is not None:
                self.target_app.PreviewWin.maybe_resize_preview_win()
                
    def destroy_preview_widget(self):
        """destroy pw_widget if present"""
        if self.pw_widget is not None:
            self.pw_widget.destroy()
            self.pw_widget = None
            self.disp_frame = None
    
    def set_widget_tk_properties(self):
        
        if self.pw_widget is None:
            return
        
        #if self.widget_type == 'Tab':
        #    return
        
        #... now done by PW_Widget
        # get the default property options for native_widget when 1st created.
        #self.default_tkOptionD = get_properties_dict( self.pw_widget )
        
        # set any user options (at this point only width and height)
        #for key, val in self.user_tkOptionD.items():
        #    set_attribute_if_possible(self.pw_widget, key, val)
        self.pw_widget.set_native_widget_attr()
        
        # set text of widgets with insert method
        try:
            self.pw_widget.native_widget.delete(0, END)
        except:
            pass
        try:
            self.pw_widget.native_widget.insert(END, self.widget_name)
        except:
            pass
    
    def set_user_properties(self):
        
        self.pw_widget.set_native_widget_attr()
        
        # set any user options (at this point only width and height)
        #for key, val in self.user_tkOptionD.items():
        #    set_attribute_if_possible(self.pw_widget.native_widget, key, val)
        
        #self.target_app.PreviewWin.update_idletasks()
    
    def get_property(self, attr_name):
        if attr_name in self.user_tkOptionD:
            return self.user_tkOptionD[ attr_name ]
            
        if attr_name in self.default_tkOptionD:
            return self.default_tkOptionD[ attr_name ]
        return None
    
    def set_a_row_weight(self, row_inp, wt_inp):
        """container objects might have weights on rows and columns"""
        self.user_tkOptionD['row_weights'] = add_entry_to_weight_str( row_inp, wt_inp, self.user_tkOptionD['row_weights'])
    
    def set_a_col_weight(self, col_inp, wt_inp):
        """container objects might have weights on rows and columns"""
        self.user_tkOptionD['col_weights'] = add_entry_to_weight_str( col_inp, wt_inp, self.user_tkOptionD['col_weights'])

    def get_tab_label_tree(self):
        """Return a list of parents to this Component """
        
        treeL = [self.widget_name]
        
        c = self
        while c.tab_label in self.target_app.compObjD:
            treeL.append( c.tab_label )
            c = self.target_app.compObjD[ c.tab_label ]
            
        return treeL

class TargetTkAppDef( object ):
        
    def __init__(self, name='myApp', PreviewWin=None, grid_notebook=None ):
        
        self.name = name
        
        self.PreviewWin = PreviewWin  # display for widgets
        self.grid_notebook = grid_notebook
        self.init_properties()
        
        # if crc_reference does not match a call to get_model_crc, then the model has changed.
        self.crc_reference = self.get_model_crc()
    
    def init_properties(self):
        # form and widgets have non-tk options here (e.g. name, x, y)
        self.app_attrD = {'name':self.name,'x':350, 'y':20, 'width':300, 'height':300,
            'guitype':'main', 'hideokbutton':'no',
            'hasmenu':'no', 
            'menu':'File\n  New\n  Open\n  Save\n\n  Exit\nHelp\n  Sounds\n    Moo\n    Meow',
            'add_menu_ctrl_keys':'yes',
            'hasstatusbar':'no','hasstddialmess':'no', 'hasstddialfile':'no', 
            'hasstddialcolor':'no', 'hasstdalarm':'no', 'resizable':'yes',
            'row_weights':'', 'col_weights':''}
                
        self.tkOptionD = {} # form and widgets have Tk options here (e.g. width, background, etc.)
        
        # compObjD has attributes like row, col, widget_name, tab_label, etc.
        self.compObjD = {} # index=widget_name: value=Component object
        
        self.tab_ownerD = {} # index=Tab name: value=Notebook name
    
    def reset_crc_reference(self):
        """When a model is first read, or after it is saved, reset the crc_reference."""
        self.crc_reference = self.get_model_crc()
    
    def model_has_changed(self):
        """Returns True if the model has changed (i.e. CRC no longer matches.)"""
        return self.crc_reference != self.get_model_crc()
    
    def get_model_crc(self):
        """Use a calculated cylic redundancy check (CRC) to detect changes to model."""
        sL = [] # will concatenate a list of strings for final calc.
        
        for key in sorted(dir(self), key=lambda s: s.lower()):
            if key.startswith('__') or key in ('PreviewWin','grid_notebook','crc_reference'):
                pass
            else:
                val = getattr(self, key)
                if type(val) in (int, dict, list, float, str, type(None)):
                    #print(key,'self crc')
                    sL.append( repr(val) )
                
        for widget_name in sorted(list(self.compObjD.keys()), key=lambda s: s.lower()):
            c = self.compObjD[ widget_name ]
            
            for key in sorted(dir(c), key=lambda s: s.lower()):
                if key.startswith('__') or key in ('PreviewWin','grid_notebook'):
                    pass
                else:
                    val = getattr(c, key)
                    if type(val) in (int, dict, list, float, str, type(None)):
                        #print(key,'c crc')
                        sL.append( repr(val) )
        # create a single string 
        s = ''.join(sL)
        #if sys.version_info < (3,):
        return binascii.crc32( binascii.a2b_qp(s) ) & 0xffffffff # to get same value for all python platforms, use & 0xffffffff
        #else:
        #    return binascii.crc32( binascii.a2b_qp(s) ) & 0xffffffff # to get same value for all python platforms, use & 0xffffffff
    
    def change_notebook_tab_label(self, tab_name_inp,  tab_label_inp):
        notebook_name = self.tab_ownerD[ tab_name_inp ]
        nb_obj = self.compObjD[ notebook_name ]
        
        for itab, (row, col, tab_name, tab_label) in enumerate( nb_obj.tab_nameL ):
            if tab_name == tab_name_inp:
                if tab_label_inp:
                    tab_label = tab_label_inp
                nb_obj.tab_nameL[ itab ] = (row, col, tab_name_inp, tab_label)
                break
        
        # arrange labels in pasted order. sorted by (row, col)
        nb_obj.tab_nameL = sorted( nb_obj.tab_nameL )
        nb_obj.user_tkOptionD['tab_labels'] = '\n'.join( [t[3] for t in nb_obj.tab_nameL] )
        
    
    def arrange_notebook_tabs(self, tab_name_inp, row_inp, col_inp):
        
        notebook_name = self.tab_ownerD[ tab_name_inp ]
        nb_obj = self.compObjD[ notebook_name ]
        
        for itab, (row, col, tab_name, tab_label) in enumerate( nb_obj.tab_nameL ):
            if tab_name == tab_name_inp:
                nb_obj.tab_nameL[ itab ] = (row_inp, col_inp, tab_name_inp, tab_label)
                break
        
        # arrange labels in pasted order. sorted by (row, col)
        nb_obj.tab_nameL = sorted( nb_obj.tab_nameL )
        nb_obj.user_tkOptionD['tab_labels'] = '\n'.join( [t[3] for t in nb_obj.tab_nameL] )
        
        #print('tab_nameL',nb_obj.tab_nameL)
        
        if nb_obj.pw_widget:
            nb_obj.pw_widget.destroy()
            nb_obj.pw_widget = None
            #print('Eliminated ',notebook_name,'Preview Object')
                
    def add_tab_to_notebook(self, row, col, tab_name, notebook_name):
        self.tab_ownerD[ tab_name ] = notebook_name
        
        #print('compObjD.keys() =',self.compObjD.keys())
        nb_obj = self.compObjD[ notebook_name ]
        
        nb_obj.tab_nameL.append( (row, col, tab_name, tab_name) ) # make label same as name for now
        #print(notebook_name, ' tab_nameL= ', nb_obj.tab_nameL)
        
        # arrange labels in pasted order. sorted by (row, col)
        self.arrange_notebook_tabs( tab_name, row, col )
        
    
    def get_tab_native_widget(self, tab_name ):
        notebook_name = self.tab_ownerD[ tab_name ]
        nb_obj = self.compObjD[ notebook_name ]
        #print('.......... nb_obj =', nb_obj)
        
        n = 0
        #print('    nb_obj.tab_nameL=',nb_obj.tab_nameL)
        for i, (row, col, t_name, tab_label) in enumerate( nb_obj.tab_nameL ):
            #print('In get_tab_native_widget, tab_name=',tab_name,' t_name=',t_name)
            if t_name == tab_name:
                n = i
                break
        
        #print('.......... In get_tab_native_widget, tab_name=',tab_name,' n=',n)
        return nb_obj.pw_widget.tab_frameL[ n ]
        
    
    def reinitialize(self):
        """Delete everything and start over"""
        self.destroy_all_preview_widgets()
        self.del_all_components()
        self.init_properties()
    
    def get_a_full_desc_of_weights(self):
        """
        Returns a two dict of non-zero weights, a row dict and a column dict.
        The indeces are of the form (tab_label, row) and (tab_label, col)
        The values are the wt value
        """
        full_rowD = {} # index=(tab_label,row_target), value=wt
        full_colD = {} # index=(tab_label,col_target), value=wt
        # first add Main entries
        rowD = make_weights_dict_from_str( self.app_attrD['row_weights'] )
        for row,wt in list(rowD.items()):
            full_rowD[ ("Main", row) ] = wt
        
        colD = make_weights_dict_from_str( self.app_attrD['col_weights'] )
        for col,wt in list(colD.items()):
            full_colD[ ("Main", col) ] = wt
        
        #print("...NOTICE...Need to iterate container widgets and add weights")
        for widget_name, c in list(self.compObjD.items()):
            if c.widget_type in ContainerControlsL:
                
                rowD = make_weights_dict_from_str( c.user_tkOptionD['row_weights'] )
                for row,wt in list(rowD.items()):
                    full_rowD[ (c.widget_name, row) ] = wt
                
                colD = make_weights_dict_from_str( c.user_tkOptionD['col_weights'] )
                for col,wt in list(colD.items()):
                    full_colD[ (c.widget_name, col) ] = wt
        
        #print('full_rowD = ',full_rowD)
        #print('full_colD = ',full_colD)
        return full_rowD, full_colD
    
    def set_a_row_weight(self, tab_label, row_inp, wt_inp):
        if tab_label=="Main":
            self.app_attrD['row_weights'] = add_entry_to_weight_str( row_inp, wt_inp, self.app_attrD['row_weights'])
        else:
            c = self.compObjD[ tab_label ]
            c.user_tkOptionD['row_weights'] = add_entry_to_weight_str( row_inp, wt_inp, c.user_tkOptionD['row_weights'])
    
    def set_a_col_weight(self, tab_label, col_inp, wt_inp):
        if tab_label=="Main":
            self.app_attrD['col_weights'] = add_entry_to_weight_str( col_inp, wt_inp, self.app_attrD['col_weights'])
        else:
            c = self.compObjD[ tab_label ]
            c.user_tkOptionD['col_weights'] = add_entry_to_weight_str( col_inp, wt_inp, c.user_tkOptionD['col_weights'])
    
    def setSpecialOption(self, name, value):
        self.app_attrD[name] = value
        
    def getSpecialOption(self, name ):
        return self.app_attrD.get(name, '')
    
    def set_PreviewWin(self, PreviewWin):
        self.PreviewWin = PreviewWin
    
    def set_Notebook( self, grid_notebook ):
        self.grid_notebook = grid_notebook

    
    def show_preview(self):
        """Loops over all components, adds them to PreviewWin if they are new or have changed."""
        
        if self.PreviewWin is None:
            return
            
        ct = ComponentTree()
        for widget_name, c in list(self.compObjD.items()):
            ct.add_node( CNode(widget_name, c.tab_label, c) )
        
        containerD = {"Main":self.PreviewWin.prevFrame} # index=tab_label: value=tk parent object
        
        cnodeL = ct.get_ordered_components()

        # --------- set up info for any Tab or Notebook Component objects -----------
        # Notebook Tab labels separated by \n
        #self.user_tkOptionD['tab_labels'] = 'Mickey\nGoofy\nPopeye'
        #self.tab_nameL = [] # tuples of Tab name and label, e.g. (row, col, Tab_1, text)
        
        nb_tab_nameLD = {} # index=notebook_name: value=tab_nameL
        for cn in cnodeL:
            c = cn.component
            if c.widget_type == 'Notebook':
                nb_tab_nameLD[c.widget_name] = []
            elif c.widget_type == 'Tab':
                nb_tab_nameLD[c.tab_label].append( (c.row, c.col, c.widget_name, c.user_tkOptionD['text']) )
                nb_tab_nameLD[c.tab_label] = sorted( nb_tab_nameLD[c.tab_label] )

        
        # --------- make preview components -----------
        for cn in cnodeL:
            c = cn.component
            #print('In show_preview, widget_name =',c.widget_name, '  tab_label=',c.tab_label,
            #      '\n ...  containerD.keys()=',containerD.keys())
            
            if c.widget_type == 'Tab':
                self.tab_ownerD[ c.widget_name ] = c.tab_label
                containerD[ c.widget_name ] = self.get_tab_native_widget( c.widget_name )
            else:
                if c.widget_type == 'Notebook':
                    c.tab_nameL = nb_tab_nameLD[ c.widget_name ]
                
                parent_component = self.compObjD.get( c.tab_label , None )
                #                    parent_name,  parent Component,  parent container widget
                c.maybe_make_widget(  containerD[c.tab_label] ) # returns True if had to make it.
                
                if c.pw_widget:
                    self.PreviewWin.add_widget(c.row, c.col, c.pw_widget)
                    containerD[ c.widget_name ] = c.pw_widget.native_widget # put possible parent widgets into dictionary
        
        # set any column or row weights
        if self.grid_notebook is not None:
            #print("Setting columnconfigure and rowconfigure")
            #print('    self.app_attrD["col_weights"] = ', self.app_attrD["col_weights"])
            self.grid_notebook.set_row_column_weights_from_target_app()
            # -------------------------------------------
            # rowD and colD: index=(tab_label,row_target), value=wt
            rowD, colD = self.get_a_full_desc_of_weights()
            
            for (tab_label, row_target),wt in list(rowD.items()):
                parent = containerD.get( tab_label, None )
                if parent is not None:
                    parent.rowconfigure(row_target, weight=wt)
        
            
            for (tab_label, col_target),wt in list(colD.items()):
                parent = containerD.get( tab_label, None )
                if parent is not None:
                    parent.columnconfigure(col_target, weight=wt)
            
            # -----------------------------------------
            #weightD = make_weights_dict_from_str( self.app_attrD["col_weights"] )
            #for col,wt in weightD.items():
            #    #print('col=%s, wt=%s'%(col,wt))
            #    parent = containerD.get( "Main", None )
            #    if parent is not None:
            #        parent.columnconfigure(col, weight=wt)
            #        #print('executed col=%s, wt=%s'%(col,wt))
            #    
            #weightD = make_weights_dict_from_str( self.app_attrD["row_weights"] )
            #for row,wt in weightD.items():
            #    parent = containerD.get( "Main", None )
            #    #print('row=%s, wt=%s'%(row,wt))
            #    if parent is not None:
            #        parent.rowconfigure(row, weight=wt)
            #        #print('executed row=%s, wt=%s'%(row,wt))
        
    
    def destroy_all_preview_widgets(self):
        """destroy pw_widget if present"""
        for c in list(self.compObjD.values()):
            if c.pw_widget is not None:
                c.destroy_preview_widget()
        #print( 'Destroyed all preview widgets' )
    
    def del_all_components(self):
        for c in list(self.compObjD.values()):
            c.destroy_preview_widget()
        self.compObjD = {}
        #print( 'Deleted all preview widgets' )
    
    def delComponentByName(self, widget_name):
        '''MUST have "widget_name" value in compObjD dictionary'''
        
        if widget_name in self.compObjD:
            c = self.compObjD[ widget_name ]
            c.destroy_preview_widget()
            del self.compObjD[ widget_name ] 
            #print( 'Deleted "%s" from form'%widget_name )
        
    def maybe_add_component(self, widget_type="Button", widget_name="Button_1", tab_label="Main", 
                            row=1, col=1):
        """If the component is not already in app, add it."""
        
        if widget_name in self.compObjD:
            c = self.compObjD[ widget_name ]
            
            if c.widget_has_moved( tab_label=tab_label, row=row, col=col ):
                c.destroy_preview_widget()
                c.reset_location( tab_label=tab_label, row=row, col=col )                
        else:
            c = Component( widget_type=widget_type, widget_name=widget_name, tab_label=tab_label, 
                           row=row, col=col, target_app=self )
            self.compObjD[ widget_name ] = c
            
            # # duplicating a widget, so copy over all the user_tkOptionD properties
            if self.grid_notebook is not None:
                if self.grid_notebook.dup_source_widget_name:
                    c_src = self.compObjD[ self.grid_notebook.dup_source_widget_name ]
                    
                    for key,val in list(c_src.user_tkOptionD.items()):
                        # set all attr to source widget values, unless it's the dup_source_widget_name 
                        if val != self.grid_notebook.dup_source_widget_name:
                            c.user_tkOptionD[key] = val

                    if widget_type == "Notebook":
                        c.grid_notebook = self.grid_notebook
    
    def removeContainerByName(self, container_name):
        """
        container_name is a widget_name to be removed.
        The approach is to collect the names of remaining components and rebuild the target_app.
        """
        del_child_nameL = self.get_names_of_containers_widgets( container_name )
        del_child_nameL.append( container_name )
        
        # if container is a Tab, then need to correct its Notebook tab_labels attribute.
        if container_name.startswith('Tab_'):
            c_tab = self.compObjD[ container_name ]
            notebook_name = c_tab.tab_label
            c_nb = self.compObjD[ notebook_name ]
            sL = c_nb.user_tkOptionD['tab_labels'].split('\n')
            sL = [s for s in sL if s != container_name]
            c_nb.user_tkOptionD['tab_labels'] = '\n'.join(sL)
        
        # get list of components in add-order.
        cnodeL = self.get_ordered_components()
        
        # reinitialize, but save app_attr values
        save_tkOptionD = self.tkOptionD.copy()
        self.reinitialize()
        self.grid_notebook.initialize_NotebookGridDes()
        self.grid_notebook.notebook.bind("<<NotebookTabChanged>>", self.grid_notebook.grid_gui.tab_of_notebook_changed)
        
        self.tkOptionD = save_tkOptionD
        
        # add back in all the undeleted components
        #print('del_child_nameL =', del_child_nameL)
        for cn in cnodeL:
            c = cn.component
            if c.widget_name not in del_child_nameL:
                #print('adding back in', c.widget_name)


                self.maybe_add_component( widget_type=c.widget_type, widget_name=c.widget_name, 
                                          tab_label=c.tab_label, row=c.row, col=c.col)

                c_new = self.compObjD[ c.widget_name ]
                #print('c_new =', c_new)
                
                for key, val in list(c.user_tkOptionD.items()):
                    if key == 'tab_labels':
                        val = val.replace('\\n', '\n')
                        c_new.user_tkOptionD[key] = val
                        
                    elif key not in ['widget_type', 'tab_label', 'row', 'col']:
                        c_new.user_tkOptionD[key] = val

        # put the widgets on the grid_notebook
        widgetL = []
        for cn in cnodeL:
            c = cn.component
            if c.widget_name not in del_child_nameL:
                widgetL.append( (c.widget_type, c.widget_name, c.tab_label, c.row, c.col) )
            
        self.grid_notebook.set_complete_list_of_widgets( widgetL )

        self.grid_notebook.repaint_all_labels()
        
        self.grid_notebook.grid_gui.refresh_preview_win()
        self.grid_notebook.grid_gui.restore_black_listbox()
        
    def get_ordered_components(self):
        """Return a complete list of all components in add-order."""        
        
        ct = ComponentTree()
        for widget_name, c in list(self.compObjD.items()):
            ct.add_node( CNode(widget_name, c.tab_label, c) )
                
        cnodeL = ct.get_ordered_components()
        return cnodeL
    
    def get_names_of_containers_widgets(self, container_name):
        """Return the widget_name value for all widgets in container_name."""
                        
        c_cont = self.compObjD[ container_name ]
        if c_cont.widget_type not in ContainerControlsL:
            return [] # if not a container, simply return an empty list.
        
        ct = ComponentTree()
        for widget_name, c in list(self.compObjD.items()):
            ct.add_node( CNode(widget_name, c.tab_label, c) )
                
        cnodeL = ct.get_ordered_components()

        child_tab_set = set([container_name])
        child_name_set = set()
        num_kids = 0
        
        while True:
            for cn in cnodeL:
                c = cn.component
                
                if c.tab_label in child_tab_set:
                    child_name_set.add( c.widget_name )
                    
                    if c.widget_type in ContainerControlsL:
                        child_tab_set.add( c.widget_name )
                    
            if len(child_name_set) == num_kids:
                break
            num_kids = len(child_name_set)
            
        return sorted( list(child_name_set) )

    
    def readAppDefFile(self, readPathName):
        
        def maybe_int( s ):
            try:
                result = int(s.strip())
            except:
                result = s
            return result
        
        if readPathName:
            self.reinitialize()
            
            fullpath = os.path.abspath( readPathName )
            fname = os.path.basename( fullpath )
            name = fname.split('.')[0]
            suffix = fname.split('.')[1]
            if suffix.lower() != 'def':
                print( 'WARNING... Expected *.def file, got',fname )
                
            # make an instance of ConfigInterface
            cf = ConfigInterface( config_filename=fullpath )
            
            infoD = cf.get_dictionary() # includes all sections
            
            for sec_name in cf.get_sectionL():
                #print("Section:",sec_name)
                #print(infoD[sec_name])
                #print()
                
                D = infoD[sec_name]
                for key,val in list(D.items()):
                    D[key] = maybe_int( val )
                
                if sec_name=='app_attr':
                    for key,val in list(D.items()):
                        if key in ('menu', 'tablabels'):
                            val = val.replace('\\n', '\n')
                            val = val.replace('\\t', '  ')
                                                
                        if key in self.app_attrD:
                            self.app_attrD[key] = val
                        else:
                            self.tkOptionD[key] = val                    
                        
                else: # a component
                    self.maybe_add_component( widget_type=D['widget_type'], widget_name=sec_name, 
                                              tab_label=D['tab_label'], row=D['row'], col=D['col'])
                    
                    c = self.compObjD[ sec_name ]
                    for key, val in list(D.items()):
                        if key == 'tab_labels':
                            val = val.replace('\\n', '\n')
                            c.user_tkOptionD[key] = val
                            #print('Made tab_labels =', val.replace('\n',' | '))
                            
                        elif key not in ['widget_type', 'tab_label', 'row', 'col']:
                            c.user_tkOptionD[key] = val


            if self.grid_notebook is not None:
                self.grid_notebook.set_row_column_weights_from_target_app()
                #print('self.app_attrD["col_weights"] = ', self.app_attrD["col_weights"])

            self.reset_crc_reference() # set to current value of crc_reference

    def saveAppDefFile(self, savePathName=''):
        
        if savePathName:
            if 1:#try:
                # make sure we have full path
                fullpath = os.path.abspath(savePathName)
                fname = os.path.basename( fullpath )
                name = fname.split('.')[0]
                suffix = fname.split('.')[1]
                if suffix.lower() != 'def':
                    print( 'ERROR... illegal file name',fname )
                    return 0 # indicates an error
            
                self.name = name
                curdir = os.path.dirname( fullpath )
                fName = os.path.normpath(curdir +'/'+ name + '.def') # def file name
                
                # see if file already exists, if so then move it to backup
                if os.path.exists( fName ):
                    backup_fname = name + '.def.bak'
                    full_backup = os.path.abspath( backup_fname )
                    
                    if os.path.exists( full_backup ):
                        os.remove( full_backup )
                        print('Deleted Previous Backup:', backup_fname)

                    print(" Created Backup File:",backup_fname)
                    os.rename( fName, full_backup)

                
                if DEBUG_PRINT: print( 'app definition saved to',fName )
                self.app_attrD['name'] = name
                
                # set to actual width and height of PreviewWin
                #print("TargetTkAppDef PreviewWin set to: ", self.PreviewWin)

                if self.PreviewWin is not None:
                    self.app_attrD['width']  = self.PreviewWin.winfo_width() 
                    self.app_attrD['height'] = self.PreviewWin.winfo_height()
                    self.app_attrD['x'] = self.PreviewWin.winfo_x()
                    self.app_attrD['y'] = self.PreviewWin.winfo_y()
                else:
                    print('WARNING... no PreviewWin for Save Info.')
        
                # make an instance of ConfigInterface
                cf = ConfigInterface( config_filename=fName )
                
                for key, val in list(self.app_attrD.items()):
                    if key == 'menu':
                        val = val.replace('\n','\\n')
                        val = val.replace('\t','\\t')
                    
                    cf.set('app_attr', key, val)
                
                keyL = sorted( self.compObjD.keys() )
                for key in keyL:
                    c = self.compObjD[ key ]
                    
                    # save attributes not in user_tkOptionD
                    for a in ['widget_type', 'tab_label', 'row', 'col']:
                        cf.set(c.widget_name, a, getattr(c, a))

                    # save user_tkOptionD
                    for a, val in list(c.user_tkOptionD.items()):
                        if a=='sticky': # only save sticky, if user input it.
                            if val:
                                cf.set(c.widget_name, a, val)
                        elif a == 'tab_labels':
                            val = val.replace('\n','\\n')
                            val = val.replace('\t','\\t')
                            cf.set(c.widget_name, a, val)
                            #print('Saving tab_labels as: ',val)
                        else:
                            cf.set(c.widget_name, a, val)
        

                cf.save_file()
                
                self.reset_crc_reference() # set to current value of crc_reference
                
                return 1 # indicates a good save
                
            else:#except:
                print( 'ERROR... saving file:',savePathName )
                return 0 # indicates an error
        else:
            print("ERROR... no file name in saveAppDefFile.")
            return 0


if __name__ == "__main__":
    
    fd = TargetTkAppDef( 'myTestApp' )
    fd.tkOptionD['background']='yellow'
    
    N = (len( fd.compObjD )+2) * 20
    I = len( fd.compObjD ) + 1
    fd.maybe_add_component(widget_type="Button", widget_name="Button_1", tab_label="Main", 
                        row=1, col=1)
    #fd.saveAppDefFile()

    fd.maybe_add_component(widget_type="Label", widget_name="Label_1", tab_label="Main", 
                        row=1, col=2)
    #fd.saveAppDefFile()        

    for obj in list(fd.compObjD.values()):
        print( 'for "%s" object "%s"'%(obj.widget_name, obj.widget_type) )
        if obj.default_tkOptionD:
            print('...default properties')
            for key,val in list(obj.default_tkOptionD.items()):
                print( key,val )
        print('...user properties')
        for key,val in list(obj.user_tkOptionD.items()):
            print( key,val )
        print()

    print( 'fd.get_model_crc() =',fd.get_model_crc() )
    