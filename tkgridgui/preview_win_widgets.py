#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()
from builtins import object
"""
For PreviewWin encapsulate the standard widgets within a Frame
since some situations require a compound object (e.g. scrolling)

Hide widget.config behind widget.pw_config so that widget attributes
and compound attributes can be handled properly.
"""

import os
import sys
    
from tkinter import *
import tkinter.messagebox
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu # ttk OptionMenu seems to be broken
from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Style, Notebook
    
from tkgridgui.edit_options import get_properties_dict, set_attribute_if_possible

from tkgridgui.grid_notebook import intCast, CONTROL_COLOR_D
from tkgridgui.config_file import ConfigInterface

from tkgridgui.tooltip import CreateToolTip

# see: http://effbot.org/zone/tkinter-scrollbar-patterns.htm
SCROLL_Y_WIDGETS = set(['Canvas','Listbox','Text','Treeview']) # Treeview has .xview() and .yview() methods
SCROLL_X_WIDGETS = set(['Canvas','Entry','Listbox','Text','Treeview'])

tkWidgetsD = {'Button':Button, 'Canvas':Canvas, 'Checkbutton':Checkbutton, 
    'Combobox':Combobox, 'Entry':Entry, 'Frame':Frame,
    'Label':Label, 'LabelFrame':LabelFrame,'Listbox':Listbox, 'Message':Message, 
    'Menubutton':Menubutton, 'Notebook':Notebook ,'OptionMenu':OptionMenu,'Progressbar':Progressbar,
    'Radiobutton':Radiobutton, 'RadioGroup':LabelFrame,  # <== note that RadioGroup is a LabelFrame 
    'Scale':Scale, 'Separator':Separator, 
    'Spinbox':Spinbox, 'Text':Text, 'Treeview':Treeview }


class PW_Widget( object ):
    
    def grid(self, row=0, column=0):
        self.pw_frame.grid( row=row, column=column )
        
    def winfo_x(self):
        return self.pw_frame.winfo_x()
        
    def winfo_width(self):
        return self.pw_frame.winfo_width()
            
    def winfo_y(self):
        return self.pw_frame.winfo_y()
        
    def winfo_height(self):        
        return self.pw_frame.winfo_height()
    
    def destroy(self):
        self.pw_frame.destroy()
    
    def destroy_children(self):
        for child in self.pw_frame.winfo_children():
            child.destroy()
    
    def keys(self):
        """Only get native_widget.keys()"""
        return  list(self.native_widget.keys()) # + self.cobj.user_tkOptionD.keys()
    
    def cget(self, name):
        return self.native_widget.cget( name )
    
    def __getitem__(self, attr_name):
        """expected attr_name values: relief, background, fg, font, etc."""
        if attr_name in self.cobj.user_tkOptionD:
            return self.cobj.user_tkOptionD[ attr_name ]
            
        if attr_name in self.cobj.default_tkOptionD:
            return self.cobj.default_tkOptionD[ attr_name ]
        return None
        
    def __setitem__(self, key, value):
        #print("Entering __setitem__ with key=",key,' and value=',value)
        if value is None:
            value = ''

        if value:
            self.cobj.user_tkOptionD[ key ] = value
            
        elif key in self.cobj.user_tkOptionD:
            # i.e. no value input, but key is in user_tkOptionD so delete it.
            del self.cobj.user_tkOptionD[ key ]
            
        # do nothing if no value and key not already in user_tkOptionD
                
        #print('Setting Item Attr:',key,' = ',value)
        self.set_native_widget_attr()
    

    
    def __init__(self, disp_frame, cobj):
        """
        disp_frame is PreviewWin.prevFrame for Main objects
        disp_frame is the native_widget of pw_widget's parent otherwise
         
        cobj is target_tk_app_def.Component (e.g. cobj.widget_type, cobj.widget_name, 
            cobj.row, cobj.col, cobj.tab_label, cobj.tkvar, cobj.user_tkOptionD
        """
        self.disp_frame = disp_frame
        self.cobj = cobj
                        
        self.pw_frame = Frame( disp_frame )
        self.pw_frame_background = self.pw_frame['background']
        self.pw_frame_borderwidth = self.pw_frame['borderwidth']
        self.pw_frame_highlightbackground = self.pw_frame['highlightbackground']
        
        #print('disp_frame: ',disp_frame.winfo_class())
        #for child in disp_frame.winfo_children():
        #    print('child: ',child.winfo_class())
        #    print('child.keys()',child.keys())
        
        # just in case row_weight or col_weight is applied to native_widget
        self.pw_frame.rowconfigure(0, weight=1)
        self.pw_frame.columnconfigure(0, weight=1)
        
        
        self.put_native_widget_into_pw_frame()

    def native_widget_clicked(self, event):
        """When native_widget is clicked, try to change grid_notebook tab."""
        
        if self.cobj.target_app.grid_notebook is None:
            #print('grid_notebook is None')
            return
        
        nb_obj = self.cobj.target_app.grid_notebook
        nb_obj.set_current_tab_by_label( self.cobj.tab_label )
        

    def tab_of_notebook_changed(self, event):
        """When PreviewWin Tab changes, try to change grid_notebook tab."""
        
        if self.cobj.target_app.grid_notebook is None:
            #print('grid_notebook is None')
            return
        
        nb = self.native_widget
        text = nb.tab(nb.select(), "text")
        nb_obj = self.cobj.target_app.grid_notebook
        
        for itab, (row, col, tab_name, tab_label) in enumerate( self.cobj.tab_nameL ):
            #print( (row, col, tab_name, tab_label) )
            if text == tab_label:
                nb_obj.set_current_tab_by_label( tab_name )
                #nb_obj.pw_widget.native_widget.select( itab )
                #print('preview_win_widgets.tab_of_notebook_changed: set PreviewWin Tab to:', itab)
                break
    
    def tab_of_notebook_clicked(self, event):
        
        if self.cobj.target_app.grid_notebook is None:
            #print('grid_notebook is None')
            return
            
        #print('x:', event.x)
        #print('y:', event.y)            

        nb = self.native_widget

        clicked_tab = nb.tk.call(nb._w, "identify", "tab", event.x, event.y)
        #print('clicked tab:', clicked_tab)

        active_tab = nb.index(nb.select())
        #print(' active tab:', active_tab)
        
        self.tab_of_notebook_changed( event )

        #if clicked_tab == active_tab:
        #    print( 'clicked_tab == active_tab' )
        
    def put_native_widget_into_pw_frame(self):
        
        cobj = self.cobj
        
        if cobj.widget_type == 'Notebook':
                
            self.native_widget = Notebook( self.pw_frame, width=400, height=300 )
            #self.native_widget.bind("<<NotebookTabChanged>>", self.tab_of_notebook_changed)
            self.native_widget.bind("<ButtonRelease-1>", self.tab_of_notebook_clicked)
            
            tab_label_str = cobj.user_tkOptionD.get('tab_labels', 'Pine\nBirch\nCherry')
            tab_labelL = tab_label_str.split('\n')
            
            # First tab is just to identify Notebook_xxx
            #tab_frame = Frame( self.native_widget )
            #self.native_widget.add(tab_frame, text=cobj.widget_name)
            
            self.tab_frameL = [] # list of Frame objects used as tabs for Notebook
            
            # add desired tabs after that
            for tab_str in tab_labelL:
                tab_frame = Frame( self.native_widget )
                self.native_widget.add( tab_frame, text=tab_str )
                
                # save Frame objects to put Tab widgets onto.
                self.tab_frameL.append( tab_frame )
                        
        elif cobj.widget_type == 'Frame':
            self.native_widget = Frame( self.pw_frame, bd=2, relief=GROOVE )
                
        elif cobj.widget_type == 'Spinbox':
            self.native_widget = Spinbox(self.pw_frame, from_=0, to=100)
        
        elif cobj.widget_type == 'Treeview':
            self.native_widget = Treeview( self.pw_frame )
            tree = self.native_widget
            # Inserted at the root, program chooses id:
            tree.insert('', 'end', 'widgets', text='Widget Tour')
             
            # Same thing, but inserted as first child:
            tree.insert('', 0, 'gallery', text=cobj.widget_name)

            # Treeview chooses the id:
            id = tree.insert('', 'end', text='Tutorial')

            # Inserted underneath an existing node:
            for tree_widget in sorted( tkWidgetsD.keys() ):
                tree.insert('widgets', 'end', text=tree_widget)
            tree.insert(id, 'end', text='Tree')                
        
        elif cobj.widget_type in ['RadioGroup', 'LabelFrame']:
            self.native_widget = LabelFrame( self.pw_frame, text=cobj.widget_name )
        
        elif cobj.widget_type == "Canvas":
            self.native_widget = Canvas( self.pw_frame )
            w = int(cobj.user_tkOptionD['width'])
            h = int(cobj.user_tkOptionD['height'])
            #self.native_widget.create_rectangle((2, 2, w-1, h-1), outline="blue")
            self.native_widget.config(bg='#aaffaa')
            self.native_widget.create_text(w//2,h//2, text=cobj.widget_name, 
                                           fill="black", width=w, anchor='center')
        
        elif cobj.tkvar is None:
            # has no tk variable, so don't worry about it
            self.native_widget = tkWidgetsD[cobj.widget_type]( self.pw_frame )
            
        # ============ The following all have tk variable controllers. ===============
        else: # e.g. StringVar
            # 'Entry' 'OptionMenu' 'Combobox' 'Checkbutton' 'Radiobutton' 'Scale'
            if cobj.widget_type == 'Entry':
                self.native_widget = Entry(self.pw_frame, textvariable=cobj.tkvar)
                
            elif cobj.widget_type == 'OptionMenu':
                self.native_widget = OptionMenu(self.pw_frame, cobj.tkvar, "one", "two", "three", "four")
                cobj.tkvar.set( "two" )
                
            elif cobj.widget_type == 'Combobox':
                self.native_widget = Combobox(self.pw_frame, textvariable=cobj.tkvar)
                self.native_widget['values'] = ('X', 'Y', 'Z')
                self.native_widget.current(0)
                
            elif cobj.widget_type == 'Checkbutton':
                self.native_widget = Checkbutton(self.pw_frame, variable=cobj.tkvar, onvalue="yes", offvalue="no")
                cobj.tkvar.set("yes")
                
            elif cobj.widget_type == 'Menubutton':
                self.native_widget = Menubutton(self.pw_frame, text=cobj.widget_name, relief=GROOVE)
                self.native_widget.menu =  Menu ( self.native_widget , tearoff = 0 )
                self.native_widget["menu"] =  self.native_widget.menu
                for i,tkvar in enumerate(cobj.tkvar_list):
                    self.native_widget.menu.add_checkbutton(label="option %i"%(i+1,), variable=tkvar )
                
            elif cobj.widget_type == 'Radiobutton':
                
                if cobj.tab_label.startswith("RadioGroup"):
                    tkvar = cobj.target_app.compObjD[ cobj.tab_label ].tkvar
                    self.native_widget = Radiobutton(self.pw_frame, variable=tkvar, value=cobj.widget_name)
                    #print(cobj.widget_name,' is part of ',cobj.tab_label)
                    self.native_widget.select()
                else:
                    self.native_widget = Radiobutton(self.pw_frame, variable=cobj.tkvar, value=cobj.widget_name)
                    #print(cobj.widget_name,' is an isolated radio button')
                    
                
            elif cobj.widget_type == 'Scale':
                self.native_widget = Scale(self.pw_frame, variable=cobj.tkvar, from_=0, to=100)
                
            else:
                print("WARNING... ignoring tk variable for ", cobj.widget_name)
                self.native_widget = tkWidgetsD[cobj.widget_type]( self.pw_frame )
                
        self.has_y_scroll = False # might get set in self.set_native_widget_attr()
        self.has_x_scroll = False # might get set in self.set_native_widget_attr()
        self.vbar = False         # might get set in self.set_native_widget_attr()
        self.hbar = False         # might get set in self.set_native_widget_attr()
        
        if cobj.widget_type in ('Treeview',):
            self.tooltip = CreateToolTip(self.pw_frame, text=cobj.widget_name,
                                         background=CONTROL_COLOR_D[ cobj.widget_type ] )
        else:
            self.tooltip = CreateToolTip(self.native_widget, text=cobj.widget_name,
                                         background=CONTROL_COLOR_D[ cobj.widget_type ] )
    
        #self.native_widget.pack(side=LEFT,expand=True,fill=BOTH)
        self.native_widget.grid(row=0, column=0)
        
        cobj.default_tkOptionD = get_properties_dict( self.native_widget )
        
        self.set_native_widget_attr()

        # bind to native_widget_clicked so the grid_notebook tab can be set
        if cobj.widget_type != 'Notebook':
            self.native_widget.bind("<ButtonRelease-1>", self.native_widget_clicked)


    def maybe_add_y_scroll(self):
        if self.has_y_scroll:
            return # already have a y scroll widget
        else:
            self.has_y_scroll = True
            if self.cobj.widget_type == 'Canvas':
                w = int(self.cobj.user_tkOptionD['width'])
                h = int(self.cobj.user_tkOptionD['height'])
                self.native_widget.config( scrollregion=(0,0,w,h*2) )

            vbar=Scrollbar(self.pw_frame,orient=VERTICAL)
            vbar.grid(row=0, column=1, sticky='ns')
            vbar.config(command=self.native_widget.yview)

            self.native_widget.config( yscrollcommand=vbar.set )
            self.vbar = vbar
    
    def maybe_add_x_scroll(self):
        if self.has_x_scroll:
            return # already have a y scroll widget
        else:
            self.has_x_scroll = True
            if self.cobj.widget_type == 'Canvas':
                w = int(self.cobj.user_tkOptionD['width'])
                h = int(self.cobj.user_tkOptionD['height'])
                if self.has_y_scroll:
                    self.native_widget.config( scrollregion=(0,0,w*2,h*2) )
                else:
                    self.native_widget.config( scrollregion=(0,0,w*2,h) )
                    
            elif self.cobj.widget_type == 'Text':
                self.native_widget.config( wrap=NONE )

            hbar=Scrollbar(self.pw_frame,orient=HORIZONTAL)
            hbar.grid(row=1, column=0, sticky='ew', columnspan=2)
            hbar.config(command=self.native_widget.xview)

            self.native_widget.config( xscrollcommand=hbar.set )
            self.hbar = hbar
    
    
    def pw_highlight_widget(self):
        if self['background']:
            self.native_widget["background"] = "#FF6666"
        else:
            self.pw_frame["background"] = "#FF6666"
            self.pw_frame["highlightbackground"] = "#FF6666"
            self.pw_frame["borderwidth"] = 5
            
        #print('did the Highlighting of pw widget')
    
    def pw_unhighlight_widget(self):
        if self['background']: # taken from user_tkOptionD or default_tkOptionD
            self.native_widget["background"] = self['background']
        else:
            self.pw_frame["background"] = self.pw_frame_background
            self.pw_frame["highlightbackground"] = self.pw_frame_highlightbackground
            self.pw_frame["borderwidth"] = self.pw_frame_borderwidth
    
    def handle_scroll_logic(self):
        
        must_rebuild = False
        
        if self.cobj.user_tkOptionD.get('scrolly','no') == 'yes':
            self.maybe_add_y_scroll()
        elif self.has_y_scroll:
            must_rebuild = True # request is "no", but already have y scroll
            
        if self.cobj.user_tkOptionD.get('scrollx','no') == 'yes':
            self.maybe_add_x_scroll()
        elif self.has_x_scroll:
            must_rebuild = True # request is "no", but already have x scroll
        
        if must_rebuild:
            self.destroy_children()
            self.put_native_widget_into_pw_frame()
    
    def set_native_widget_attr(self):
        # NEED TO WAIT UNTIL PLACED INTO PARENT GRID BEFORE CHANGING ATTR.
        # set any user options (at this point only width and height)
        #print('user_tkOptionD =',self.cobj.user_tkOptionD,' for ',self.cobj.widget_name)
        
        self.handle_scroll_logic()
        
        for key, val in list(self.cobj.user_tkOptionD.items()):
            if key == 'sticky':
                # for sticky, need to set both pw_frame and native_widget
                set_attribute_if_possible(self.pw_frame, key, val)
                set_attribute_if_possible(self.native_widget, key, val)
                
            elif key in PW_FRAME_ATTR:
                set_attribute_if_possible(self.pw_frame, key, val)
            else:
                set_attribute_if_possible(self.native_widget, key, val)
            
        
PW_FRAME_ATTR = ['rowspan','columnspan','sticky']


if __name__=="__main__":
    
    from tkgridgui.preview_win import PreviewWin
    from tkgridgui.target_tk_app_def import Component
    
    
    widgetL = sorted( tkWidgetsD.keys() )
    def get_widget_type_name( i ):
        wtype = widgetL[ i % len(widgetL) ]
        i,r = divmod( i, len(widgetL) )
        name = wtype + '_%i'%(i+1,  )
        return wtype, name

    class TestPW(object):
        def __init__(self, master):
            frame = Frame(master, width=300, height=300)
            frame.pack()
            self.master = master
            self.x, self.y, self.w, self.h = -1,-1,-1,-1
            
            self.Button_1 = Button(text="Test PW_Widget", relief="raised", width="15")
            self.Button_1.place(x=84, y=36)
            self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

            self.PreviewWin = None
            self.num_comp = 0
    
        def cleanupOnQuit(self):
            #print( 'Doing final cleanup before quitting' )
            self.PreviewWin.destroy()
            self.master.allow_subWindows_to_close = 1
            self.master.destroy()
        

        def Button_1_Click(self, event): #click method for component ID=1
            
            if self.PreviewWin is None:
                self.PreviewWin = PreviewWin( self.master )
            else:
                wtype, name = get_widget_type_name( self.num_comp )
                col,row = divmod( self.num_comp, 9 )
                
                #print('Adding:',wtype, name,' to row=',row,' col=',col)
                c = Component( widget_type=wtype, 
                               widget_name=name, 
                               tab_label='Main', 
                               row=row, col=col, target_app=self )
                self.num_comp += 1
                
                if wtype in SCROLL_Y_WIDGETS:
                    c.user_tkOptionD['scrolly'] = 'yes'
                if wtype in SCROLL_X_WIDGETS:
                    c.user_tkOptionD['scrollx'] = 'yes'
                
                
                pw = PW_Widget( self.PreviewWin.prevFrame, c )
                self.PreviewWin.add_widget( c.row, c.col, pw )
                
                #pw.set_native_widget_attr()
    
    root = Tk()
    MainWin = root
    MainWin.title('Main Window')
    #MainWin.geometry('320x320+10+10')
    MainWin.config(background='#FFFACD')#'lemonchiffon': '#FFFACD'

    grid_gui = TestPW( MainWin )
    
    MainWin.mainloop()
        