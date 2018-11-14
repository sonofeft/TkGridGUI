#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
import sys

import copy

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'

# change all non-legal letters to underscore
goodset = str(letters+digits+'_')

def legal_char( c ):
    if c in goodset:
        return c
    else:
        return '_'

def legalPythonIdentifier( name ):
    name = str(name)
    #legalName = name.translate(legalTranTab) 
    legalName = ''.join( [legal_char(c) for c in name] )
    
    if legalName:
        if legalName[0] in digits:
            legalName = 'x'+legalName

    return legalName

def legalQuotedString( s ): # precede any quotes with backslash
    val = str(s)
    val = val.replace("'","\\'")
    val = val.replace('"','\\"')
    return val

def legalWidgetName(name, ctype):
    lcname = name#.lower()
    lctype = ctype#.lower()
    
    if lcname.find( lctype ) > -1:
        legalName = lcname#.title()
    else:
        #legalName = '%s_%s'%(lcname.title(), lctype.title())
        legalName = '%s_%s'%(lcname, lctype)

    legalName = legalPythonIdentifier(legalName)

    return legalName
    
def makeOptionString( opDict, startComma=1 ):
    if opDict:
        sL = []
        for k,v in list(opDict.items()):
            # precede any quotes in the value with a backslash
            val = legalQuotedString(v)
            sL.append( '%s="%s"'%(k,val) )
        s = ', '.join(sL)
        if len(s)>0 and startComma:
            s = ', ' + s
    else:
        s = ''
    
    return s


sInit = '''class %s:
    def __init__(self, master):
    
        grid_frame = Frame( master %s)
        self.grid_frame = grid_frame
        grid_frame.pack(expand=1, fill=BOTH)
        self.master = master
        
        self.x, self.y, self.w, self.h = %i, %i, %i, %i
'''
def beginSourceFile(className, width=300, height=300, opDict=None, x=10, y=10):
    return sInit%(className, makeOptionString( opDict ), x, y, width, height)
    #return sInit%(className.title(), makeOptionString( opDict ), x, y, width, height)

#-------------------------------------------------------------
sHideOkBtn = '''
    def buttonbox(self):
        pass
        # this dummy routine overrides the standard "OK" and "Cancel" buttons
        # REMEMBER!!! to call self.ok() and self.cancel() in User Code
'''

sInitDialog = '''
if sys.version_info < (3,):
    from tkSimpleDialog import Dialog
else:
    from tkinter.simpledialog import Dialog

class _Dialog(Dialog):
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptions=None):
    
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class %s(_Dialog):
%s
    def body(self, master):
        dialogframe = Frame(master, width=%i, height=%i%s)
        self.dialogframe = dialogframe
        dialogframe.pack()
'''
def beginDialogSourceFile(className, hideOkBtn, width=300, height=300, opDict=None):
    if hideOkBtn:
        s = sHideOkBtn
    else:
        s = ''
    return sInitDialog%(className,s, width, height, makeOptionString( opDict ))
    #return sInitDialog%(className.title(),s, width, height, makeOptionString( opDict ))

#-------------------------------------------------------------
sDialogValidate = '''    def validate(self):
        self.result = {} # return a dictionary of results
    '''
def getDialogValidate():
    return sDialogValidate
#-------------------------------------------------------------
sEnd = '''
def main():
    root = Tk()
    app = %s(root)
    root.mainloop()

if __name__ == '__main__':
    main()
'''
def endSourceFile(className):
    return sEnd%(className,)
    #return sEnd%(className.title(),)

#-------------------------------------------------------------
sEndDialog = '''

    def apply(self):
        pass
        #print( 'apply called' )

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
        dialog = %s(self.master, "Test Dialog")
        print( '===============Result from Dialog====================' )
        print( dialog.result )
        print( '=====================================================' )

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
'''
def endDialogSourceFile(className):
    return sEndDialog%(className,)
    #return sEndDialog%(className.title(),)
#----------------------------------------------------------------
# create weight statements: columnconfigure(col, weight=wt) and  rowconfigure(row, weight=wt)

def createWeightStatement(guiType, parent_frame, is_row, rc_val, wt):
    
    if guiType=='dialog':
        master = 'self.dialogframe'
    else:
        if parent_frame=="Main":
            master = 'self.grid_frame'
        else:
            master = 'self.'+parent_frame
    
    if is_row:
        return "        %s.rowconfigure(%s, weight=%s)\n"%(master, rc_val, wt)
    else:
        return "        %s.columnconfigure(%s, weight=%s)\n"%(master, rc_val, wt)
        
#----------------------------------------------------------------
# create list box... needs special treatment for y scroller
sCreateWidgetWScroll_Y='''
        lbframe = Frame( {master} )
        self.{wName}_frame = lbframe
        vbar=Scrollbar(lbframe, orient=VERTICAL)
        self.{wName} = {widget_type}(lbframe, {opStr} yscrollcommand=vbar.set)
        vbar.config(command=self.{wName}.yview)
        
        vbar.grid(row=0, column=1, sticky='ns')        
        self.{wName}.grid(row=0, column=0)
'''

sCreateWidgetWScroll_X='''
        lbframe = Frame( {master} )
        self.{wName}_frame = lbframe
        hbar=Scrollbar(lbframe, orient=HORIZONTAL)
        self.{wName} = {widget_type}(lbframe, {opStr} xscrollcommand=hbar.set)
        hbar.config(command=self.{wName}.xview)
        
        hbar.grid(row=1, column=0, sticky='ew')        
        self.{wName}.grid(row=0, column=0)
'''

sCreateWidgetWScroll_XY='''
        lbframe = Frame( {master} )
        self.{wName}_frame = lbframe
        vbar=Scrollbar(lbframe, orient=VERTICAL)
        hbar=Scrollbar(lbframe, orient=HORIZONTAL)
        
        self.{wName} = {widget_type}(lbframe, {opStr} xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        hbar.config(command=self.{wName}.xview)
        vbar.config(command=self.{wName}.yview)
        
        hbar.grid(row=1, column=0, sticky='ew')  
        vbar.grid(row=0, column=1, sticky='ns')                
        self.{wName}.grid(row=0, column=0)
'''

sCreateWidgetWOScroll='''
        self.%s = %s(%s, %s)
'''
def createWidgetwName(wName, widget_type, guiType, parent_frame, opDict=None):
    
    if opDict is None:
        myOpDict = {}
    else:
        myOpDict = copy.deepcopy( opDict )
    
    def remove_option( op_name ):
        if op_name in myOpDict:
            del( myOpDict[op_name] )
    
    remove_option("docstring")
    if guiType=='dialog':
        master = 'self.dialogframe'
    else:
        if parent_frame=="Main":
            master = 'self.grid_frame'
        else:
            master = 'self.'+parent_frame

    doscroll = 0
    if myOpDict:
        if 'scrolly' in myOpDict:
            if myOpDict['scrolly'].lower()=='yes':
                doscroll += 1
        remove_option('scrolly')

        if 'scrollx' in myOpDict:
            if myOpDict['scrollx'].lower()=='yes':
                doscroll += 2
        remove_option('scrollx')

    opStr = makeOptionString( myOpDict, startComma=0 ) 
    if opStr:
        opStr += ','
                
    if doscroll:
        if doscroll == 1:
            return sCreateWidgetWScroll_Y.format(master=master,wName=wName, widget_type=widget_type, opStr=opStr)
        elif doscroll == 2:
            rtn_str = sCreateWidgetWScroll_X.format(master=master,wName=wName, widget_type=widget_type, opStr=opStr)
            if widget_type=='Text':
                rtn_str += "\n        self.%s.config( wrap=NONE ) # x scroll implies no wrap\n\n"%wName
            return rtn_str
        else:
            rtn_str = sCreateWidgetWScroll_XY.format(master=master,wName=wName, widget_type=widget_type, opStr=opStr)
            if widget_type=='Text':
                rtn_str += "\n        self.%s.config( wrap=NONE ) # x scroll implies no wrap\n\n"%wName
            return rtn_str
        
    else:
        return sCreateWidgetWOScroll%( wName, widget_type, master, opStr)
        #return sCreateWidgetWOScroll%( wName, widget_type.title(), master, opStr)
#----------------------------------------------------------------

# create widget
#        self.<name> = <widget>( <options> )
sCreateWidget = '        self.%s = %s( %s %s)\n'
def createWidget(wName, widget_type, guiType, parent_frame, opDict=None):

    if opDict is None:
        myOpDict = {}
    else:
        myOpDict = copy.deepcopy( opDict )
    
    def remove_option( op_name ):
        if op_name in myOpDict:
            del( myOpDict[op_name] )

    remove_option("docstring")
    remove_option("columnspan")
    remove_option("rowspan")
    
    remove_option("row_weights")
    remove_option("col_weights")
    remove_option("tab_labels")

    if widget_type.lower() in ('entry','text','listbox','frame'):
        remove_option('text')

    # the ttk widgets can't accept style inputs
    if widget_type.lower() in ('combobox', 'progressbar', 'separator', 'treeview', 'notebook', 'optionmenu'):
        remove_option('width')
        remove_option('height')
        remove_option('background')

    if widget_type.lower() =='combobox':
        remove_option('selection')

    if widget_type.lower() in ('frame','labelframe','notebook','radiogroup'):
        remove_option('row_weights')
        remove_option('col_weights')

    # sticky option belongs in .grid statement
    if 'sticky' in myOpDict:
        del(myOpDict['sticky'])  # delete from copy of original dictionary

    #print("widget_type =",widget_type)
    #if widget_type.lower()=='labelframe':
    #    Constructor = 'LabelFrame'
    #else:
    Constructor = widget_type#.title()

    doscroll = 0
    if myOpDict:
        if 'scrolly' in myOpDict:
            if (myOpDict['scrolly'].lower()=='yes'):
                doscroll = 1
        if 'scrollx' in myOpDict:
            if (myOpDict['scrollx'].lower()=='yes'):
                doscroll = 1
        #remove_option('scrolly')
    # scrolly is a "special" option
    #if myOpDict.has_key('scrolly'):
    #    del(myOpDict['scrolly'])  # delete from copy of original dictionary
                
    if doscroll:
        return createWidgetwName(wName, widget_type, guiType, parent_frame, myOpDict)
    else:
        remove_option('scrolly')
        remove_option("scrollx")

        if guiType=='dialog':
            return sCreateWidget%(wName, Constructor,'frame', makeOptionString( myOpDict, startComma=1 ))
        else:
            if parent_frame=="Main":
                return sCreateWidget%(wName, Constructor,'self.grid_frame', makeOptionString( myOpDict, startComma=1 ))
            else:
                return sCreateWidget%(wName, Constructor, 'self.'+parent_frame, makeOptionString( myOpDict, startComma=1 ))
    
#----------------------------------------------------------------

# place widget into grid
#        self.<name>.grid( row=<x>, column=<y> )
sGridWidget = '        self.%s.grid(row=%i, column=%i)\n'
sGridWidgetFrame = '        self.%s_frame.grid(row=%i, column=%i)\n'
#def gridWidget(wName, ctype, row, col, is_gridWidgetFrame, sticky=''):
def gridWidget(wName,         row, col, is_gridWidgetFrame, sticky='', rowspan='', columnspan=''):
    
    #print("In gridWidget, wName=%s, ctype=%s, row=%s, col=%s, is_gridWidgetFrame=%s, sticky=%s"%\
    #      (wName, ctype, row, col, is_gridWidgetFrame, sticky))
    
    if is_gridWidgetFrame:
        s = sGridWidgetFrame%(wName, int(row), int(col))
    else:
        s = sGridWidget%(wName, int(row), int(col))
    
    if sticky:
        s = s.replace( ')',', sticky="%s")'%sticky )
    
    if rowspan:
        s = s.replace( ')',', rowspan="%s")'%rowspan )
    
    if columnspan:
        s = s.replace( ')',', columnspan="%s")'%columnspan )
        
    #print( "    s =",s )
    return s
        
#----------------------------------------------------------------
# bind widget
#        self.<name>.bind("<event>", self.<callback>)
sBindWidget = '        self.%s.bind("<%s>", self.%s)\n'
def bindWidget(wName, eventName, callBack):
    return sBindWidget%( wName, eventName, callBack)
#----------------------------------------------------------------
# make string variable
#        self.<name>_StringVar = StringVar()
sMakeStringVar = '        self.%s_StringVar = StringVar()\n'
def makeStringVar( wName ):
    return sMakeStringVar%wName

#----------------------------------------------------------------
# connect string variable to widget
#        self.<name>.configure(variable=self.<name>_StringVar, <options>)
sConnectStringVar = '        self.%s.configure(variable=self.%s_StringVar%s)\n'
def connectStringVar(wName, opDict=None):
    return sConnectStringVar%(wName, wName, makeOptionString( opDict ))

# special for Entry widget
sConnectEntryStringVar = '        self.%s.configure(textvariable=self.%s_StringVar%s)\n'
def connectEntryStringVar(wName, opDict=None):
    return sConnectEntryStringVar%(wName, wName, makeOptionString( opDict ))
#----------------------------------------------------------------
# turn on trace for string variable
#        self.<name>_StringVar_traceName = self.<name>_StringVar.trace_variable("w", self.<name>_StringVar_Callback)
sTraceStringVar = '        self.%s_StringVar_traceName = self.%s_StringVar.trace_variable("w", self.%s_StringVar_Callback)\n'
def traceStringVar(wName):
    return sTraceStringVar%(wName, wName, wName)
#----------------------------------------------------------------
# statusbar
sStatusBar = '''        
        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.master, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
'''
def getStatusBarSource():
    return sStatusBar

sStatusBarDialog = '''        
        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.dialogframe, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.grid(row=99, column=0, columnspan=99, sticky='ew')
'''
def getDialogStatusBarSource():
    return sStatusBarDialog

#----------------------------------------------------------------
# standard message dialogs
sMessageDialogs = '''
    # standard message dialogs... showinfo, showwarning, showerror
    def ShowInfo(self, title='Title', message='your message here.'):
        tkinter.messagebox.showinfo( title, message )
        return
    def ShowWarning(self, title='Title', message='your message here.'):
        tkinter.messagebox.showwarning( title, message )
        return
    def ShowError(self, title='Title', message='your message here.'):
        tkinter.messagebox.showerror( title, message )
        return
        
    # standard question dialogs... askquestion, askokcancel, askyesno, or askretrycancel
    # return True for OK, Yes, Retry, False for Cancel or No
    def AskYesNo(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askyesno( title, message )
    def AskOK_Cancel(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askokcancel( title, message )
    def AskRetryCancel(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askretrycancel( title, message )
        
    # return "yes" for Yes, "no" for No
    def AskQuestion(self, title='Title', message='your question here.'):
        return tkinter.messagebox.askquestion( title, message )
    # END of standard message dialogs
'''
def getStandardMessageDialogs():
    return sMessageDialogs
#----------------------------------------------------------------
sFileDialogs = '''    # standard file dialogs... askdirectory, askopenfile, asksaveasfilename

    # return a string containing directory name
    def AskDirectory(self, title='Choose Directory', initialdir="."):
        dirname = tkinter.filedialog.askdirectory(parent=%s,initialdir=initialdir,title=title)
        return dirname # <-- string
        
    # return an OPEN file type object OR None (opened using mode, 'r','rb','w','wb')
    # WARNING... opening file with mode 'w' or 'wb' will erase contents
    def AskOpenFile(self, title='Choose File', mode='rb', initialdir='.', filetypes=None):
        if filetypes==None:
            filetypes = [
                ('Text File','*.txt'),
                ('Data File','*.dat'),
                ('Output File','*.out'),
                ('Any File','*.*')]
        fileobj = tkinter.filedialog.askopenfile(parent=%s,mode=mode,title=title,
            initialdir=initialdir, filetypes=filetypes)
        
        # if opened, then fileobj.name contains the name string
        return fileobj # <-- an opened file, or the value None
        
    # return a string containing file name (the calling routine will need to open the file)
    def AskSaveasFilename(self, title='Save File', filetypes=None, initialfile=''):
        if filetypes==None:
            filetypes = [
                ('Text File','*.txt'),
                ('Data File','*.dat'),
                ('Output File','*.out'),
                ('Any File','*.*')]

        fileName = tkinter.filedialog.asksaveasfilename(parent=%s,filetypes=filetypes, initialfile=initialfile ,title=title)
        return fileName # <-- string
        
    # END of standard file dialogs
'''
def getStandardFileDialogs(guiType='main'):
    if guiType=='dialog':
        master = 'self'
    else:
        master = 'self.master'
        
    return sFileDialogs%(master, master, master)
#----------------------------------------------------------------
sColorDialog='''
    # returns a color tuple and a string representation of the selected color
    def AskForColor(self,title='Pick Color'): 
        ctuple,cstr = tkinter.colorchooser.askcolor(title=title)
        return ctuple,cstr
'''
def getStandardColorDialog():
    return sColorDialog
#----------------------------------------------------------------
#----------------------------------------------------------------
sAlarmDialog='''
    # alarm function is called after specified number of milliseconds
    def SetAlarm(self, milliseconds=1000):
        self.master.after( milliseconds, self.Alarm )
    def Alarm(self): 
        pass
'''
def getStandardAlarmDialog():
    return sAlarmDialog
#----------------------------------------------------------------
sTopImports='''

from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object

from tkinter.ttk import Combobox, Progressbar, Separator, Treeview, Notebook%s

from tkinter import *
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Label, LabelFrame
from tkinter import Listbox, Message, Radiobutton, Spinbox, Text
from tkinter import OptionMenu
import tkinter.filedialog
from tkinter import _setit as set_command

'''

sDialogImport = '''try:
    from tkSimpleDialog import Dialog
except:
    from tkinter.simpledialog import Dialog
'''
def get_top_imports( incMsgBox, incDialog, incColorCh):
    #py2L = []
    py3L = []
    if incMsgBox:
        #py2L.append('    import tkMessageBox')
        py3L.append('import tkinter.messagebox')
    if incDialog:
        #py2L.append('    from tkSimpleDialog import Dialog')
        py3L.append( sDialogImport )
    if incColorCh:
        #py2L.append('    import tkColorChooser')
        py3L.append('import tkinter.colorchooser')
    
    if py3L:
        #spy2 = '\n' + '\n'.join(py2L)
        spy3 = '\n' + '\n'.join(py3L)
    else:
        #spy2 = ''
        spy3 = ''
    
    return sTopImports%( spy3 )

#----------------------------------------------------------------

if __name__ == '__main__':
    if 1:
        print( beginSourceFile("TestForm1") )
        print( beginSourceFile("TestForm2",opDict={'background':'yellow'}) )
            
        print()
        print( endSourceFile("TestForm1") )
        
        print()
        print( createWidget('Bang_Checkbutton', 'Checkbutton', 'Checkbutton', 'Main', {'bg':'red', 'ddd':'aaa'}) )
            
        print()
        print( gridWidget('Bang_Checkbutton', '22', '55', 0) )
        
        print()
        print( bindWidget('Bang_Button', 'ButtonRelease-1', 'Bang_Button_Click') )
        
        print()
        print( makeStringVar( 'Bang_Checkbutton' ) )
        
        print()
        print( connectStringVar('Bang_Checkbutton', opDict={'onvalue':"yes", 'offvalue':"no"}) )
            
        print()
        print( traceStringVar('Bang_Checkbutton') )
        print()
        print( createWidget('myList', 'Listbox', 'Listbox', 'Frame_1', {'bg':'red', 'ddd':'aaa'}) )
            
        print()
        print( gridWidget('myList', '22', '55', 1) )
            
        print()
        print( gridWidget('myList', '22', '55', 1, sticky='ew') )
        
