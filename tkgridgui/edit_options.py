#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from builtins import range
from itertools import combinations
"""
Collect the basic edit options for all widgets, including definitions

Given a widget from PreviewWin, get the actual attributes from widget.keys()

Provide helper functions to set and get properties.
"""

WidgetPropertyDefinitionsD = {} # index=option name: value=definition
SortedPropertyNamesL = [] # sorted list of option names

grid_option_set = set(['sticky','columnspan','rowspan'])

def add_definition( options_str ):
    """Take input options_str and process it into an options dictionary"""
    strL = options_str.split('\n')
    
    for s in strL:
        sL = s.split('#')
        if len(sL)==2:
            WidgetPropertyDefinitionsD[sL[0].strip()] = sL[1].strip()

def get_definition_optionsL( attr_name ):
    """Some attr have defined options.  The definitions end with all-cap options."""
    if attr_name=='cursor':
        return partial_cursorL
        
    elif attr_name=='sticky':
        optionsL = []
        for i in range(1,5):
            cL = list(combinations('nsew', i))
            for c in cL:
                optionsL.append( ''.join(c) )
        return optionsL
    
    s = WidgetPropertyDefinitionsD.get( attr_name, '' )
    if s:
        optionsL = []
        sL = reversed( s.split() )
        for word in sL:
            if word.isupper():
                optionsL.append( word.lower() )
            else:
                break
        return optionsL
        
    else:
        return []

def set_attribute_if_possible(widget, attr_name, value):
    prop_set = set( widget.keys() )

    #print('prop_set = ', sorted(prop_set))
    if attr_name in prop_set:
        widget[ attr_name ] = value
        #print("Setting: ",attr_name,' to ',value)
    elif attr_name in grid_option_set:
        # ignore rowspan and columnspan if not an integer
        if attr_name in ('rowspan','columnspan'):
            try:
                value = int(value)
            except:
                return
        widget.grid( {attr_name:value} )

def get_properties_dict( widget ):
    """Returns a dictionary of  name, current value (as strings)"""
    resultD = {}
    
    prop_set = set( widget.keys() )
    for name in SortedPropertyNamesL:
        if name in prop_set:
            val = str( widget.cget( name ) )
            resultD[name] = val
            
    return resultD
    
def get_properties_for_editing( widget ):
    """Returns a sorted list of tuples (option name, current value, definition)"""
    resultL = []
    
    prop_set = set( widget.keys() )
    for name in SortedPropertyNamesL:
        if name in prop_set:
            val = str( widget.cget( name ) )
            resultL.append( (name, val, WidgetPropertyDefinitionsD[name]) )
            
    return resultL

buttonStr = '''anchor #Postion of text. NW N NE W CENTER E SW S SE
background #The background color
borderwidth # The size of the border in pixels. usually 1 or 2 pixels.
foreground #Color to use for text and bitmap content
image #Image to display (requires tk.PhotoImage)
justify #Align multiple lines of text. LEFT RIGHT CENTER
overrelief #Relief when mouse is over widget SUNKEN RAISED GROOVE RIDGE FLAT
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
state #Widget state NORMAL ACTIVE DISABLED'''

add_definition( buttonStr)

commonPropertiesStr = """width #Width in pixels or characters
height #Height in pixels or text lines
text #Text displayed on the widget.
font #The font used for text on the widget.
cursor #The shape of the cursor when the cursor is over the widget."""

add_definition( commonPropertiesStr )

specialtyPropertiesStr = """from_ #Constrain the values to a numeric range. For example, from_=-10 and to=10
to #Value that defines one end of the scale's range
value #The initial value of the widget's variable
length #Number of pixels for the x dimension if the scale is horizontal, or the y dimension if vertical
label #An optional text label
orient #Orientation options HORIZONTAL VERTICAL
padx #Additional padding left and right of the text.
pady #Additional padding above and below the text.
sticky #Justification of widget within grid cell N S E W
rowspan #Number of rows a widget spans (must be integer)
columnspan #Number of columns a widget spans (must be integer)
row_weights #Weight values used in rowconfigure on resize
col_weights #Weight values used in columnconfigure on resize
scrolly #Enable scrolling in y direction YES NO
scrollx #Enable scrolling in x direction YES NO
style #TTK style"""

add_definition( specialtyPropertiesStr )

SortedPropertyNamesL = sorted( WidgetPropertyDefinitionsD.keys() )

partial_cursorL = ["arrow","circle","clock","cross","dotbox","exchange","fleur","heart","hand1","hand2",
                   "man","mouse","pirate","plus","shuttle","sizing","spider","spraycan","star","target",
                   "tcross","trek","watch"]

if __name__ == "__main__":
    
    print("test_propsD = {", end='')
    for name in SortedPropertyNamesL:
        print( '    "%s"'%name, ' '*(14-len(name)), ':', '("" ,"%s"),'%WidgetPropertyDefinitionsD[name] )
        
    print("}")
        