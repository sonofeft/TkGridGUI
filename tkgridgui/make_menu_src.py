#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function

from tkgridgui.src_templates import legalPythonIdentifier, letters, digits
sampleMenuStr='''
File
    New
        Worksheet
        Text File
    Open
    Save
    
    Exit
Edit
    Find
    Copy
    Cut
    Paste
    '''

class myMenuItem( object ):
    
    def __init__(self, label):
        self.label = label
        self.subLabelL = []
        self.parent = None
        self.underline = -1
        self.ctrl_char = ''
    
    def addSubItem(self, subItem):
        self.subLabelL.append( subItem )
        subItem.parent = self
    def lenSubmenu(self):
        return len(self.subLabelL)
        
    def getSubItemAtLevel(self, N):
        m = self
        for i in range(N-1):
            if len(m.subLabelL)>0:
                m = m.subLabelL[-1]
        return m
    
    def make_ctrl_key(self, taken_uc_charL):
        """taken_uc_charL is the list of upper case characters already taken by other myMenuItem objects"""
        
        # only submenu items get a ctrl_char
        if len(self.subLabelL) > 0:
            for s in self.subLabelL:
                s.make_ctrl_key( taken_uc_charL )
        else:
            for ic,c in enumerate( self.label ):
                c = c.upper()
                if c in letters:
                    if c not in taken_uc_charL:
                        self.underline = ic
                        self.ctrl_char = c
                        taken_uc_charL.append( c )
                        return
            # since no letter was found, try a number
            for ic,d in enumerate(digits):
                if d not in taken_uc_charL:
                    self.underline = id
                    self.ctrl_char = d
                    taken_uc_charL.append( d )
                    return
            # if here then no good ctrl_char found... return without one.
            
    def printSum(self):
        
        sSubs = ''
        for sub in self.subLabelL:
            sSubs += sub.label + ' -- '
        
        print( '------------ start -----------------' )
        print( '"%s"'%self.label, 'len list =',len(self.subLabelL),sSubs )
        print( '------------- end -----------------' )
        for sub in self.subLabelL:
            sub.printSum()
        print( '----' )

def  numIndentSpaces( s ):
    return len(s) - len(s.lstrip())
    
def buildMenuSource( descStr ):
    
    # prune beginning and ending blank lines
    #print('descStr =', descStr)
    #print('repr(descStr) =', repr(descStr) )
    descL = descStr.split('\n')
    
    #print( 'len(descL)=',len(descL) )
    for i in range( len(descL)-1, -1, -1):
        if descL[i].strip() != '':
            break
        del descL[i]
    #print( 'len(descL)=',len(descL) )
    for i in range( len(descL)):
        if descL[i].strip() != '':
            break
        del descL[i]
    #print( 'len(descL)=',len(descL) )
    #print( 'descL =',descL )
    #print()
    # now interpret the pruned list for indentation
    
    if len(descL)==0:
        return ''
    
    i = 0
    nspaceLast = numIndentSpaces( descL[0] )
    indentL = []
    for label in descL:
        
        # assume a blank line is simply a seperator at the same indent level
        if label.strip() == '':
            nspace = nspaceLast
        else:
            nspace = numIndentSpaces( label )
            
        if nspace > nspaceLast:
            i += 1
        elif nspace < nspaceLast:
            i -= 1
        
        if i<0: i=0
        indentL.append( [i,label.strip()] )
        nspaceLast = nspace
        
    #print( 'indentL',indentL )
    #print()
    
    # make list of menu Items
    menuL = []
    for N,label in indentL:
        m = myMenuItem(label)
        if N==0:
            menuL.append(m)
        else:
            try:
                mtop = menuL[-1]
                madd = mtop.getSubItemAtLevel(N)
                madd.addSubItem(m)
            except:
                menuL.append(m)
        
    #for mItem in menuL:
    #    mItem.printSum()
        
    return menuL

sMenuBar = '        self.menuBar = Menu(%s, relief = "raised", bd=2)\n'
sMenu    = '\n        top_%s = Menu(self.menuBar, tearoff=0)\n'
sItem    = '        top_%s.add("command", label = "%s", command = self.%s)\n'
sItemAcc = '        top_%s.add("command", label = "%s", command=self.%s, underline=%i, accelerator="Ctrl+%s")\n'

sSpacer  = '        top_%s.add_separator()\n'
sCascade = '        self.menuBar.add("cascade", label="%s", menu=top_%s)\n'
sCascade2= '        top_%s.add("cascade", label="%s", menu=top_%s)\n'
sMenuConfig = '\n        %s.config(menu=self.menuBar)\n'
def getSubmenuSource( mItem ):
    topName = legalPythonIdentifier( mItem.label )
    sL = [sMenu%topName]
    bindL = []
    
    for s in mItem.subLabelL:
        if s.lenSubmenu()==0:
            if s.label.strip() != '':
                name = 'menu_%s_%s'%(mItem.label, s.label)
                name = legalPythonIdentifier( name )
                if s.ctrl_char:
                    sL.append(sItemAcc%(topName, s.label, name, s.underline, s.ctrl_char))
                    bindL.append('        self.master.bind("<Control-%s>", lambda event: self.%s())\n'%(s.ctrl_char, name) )
                    bindL.append('        self.master.bind("<Control-%s>", lambda event: self.%s())\n'%(s.ctrl_char.lower(), name) )
                else:
                    sL.append(sItem%(topName, s.label, name))
            else:
                sL.append(sSpacer%topName)
        else:
            s2L, b2L = getSubmenuSource(s)
            sL.extend( s2L )
            bindL.extend( b2L )
    
    if mItem.parent:
        topNameParent = legalPythonIdentifier( mItem.parent.label )
        sL.append(sCascade2%(topNameParent, mItem.label, topName))
    else:
        sL.append(sCascade%(mItem.label, topName))
    return sL, bindL
    

def getMenuSource( menuL, rootName='MainWin', add_ctrl_keys=True, imADialog=False ):
    
    if imADialog:
        srcList = [sMenuBar%'self']
    else:
        srcList = [sMenuBar%rootName]
    
    bindL = ['        # use both upper and lower characters for keyboard accelerator options.\n'] # any ctrl_char bindings that might happen
    
    if add_ctrl_keys:
        taken_uc_charL = []
        for m in menuL:
            m.make_ctrl_key( taken_uc_charL )
    
    for m in menuL:
        # most top level menu items will have subitems
        if m.lenSubmenu()>0:
            s2L, b2L = getSubmenuSource(m)
            srcList.extend( s2L )
            bindL.extend( b2L )
        else:
            name = 'menu_%s'%(legalPythonIdentifier( m.label ))
            if m.ctrl_char:
                sTopItem= '        self.menuBar.add("command", label = "%s", command=self.%s, underline=%i, accelerator="Ctrl+%s")\n'
                srcList.append( sTopItem%( m.label, name, m.underline, m.ctrl_char) )
                bindL.append('        self.master.bind("<Control-%s>", lambda event: self.%s())\n'%(m.ctrl_char, name) )
                bindL.append('        self.master.bind("<Control-%s>", lambda event: self.%s())\n'%(m.ctrl_char.lower(), name) )
            else:
                sTopItem= '        self.menuBar.add("command", label = "%s", command = self.%s)\n'
                srcList.append( sTopItem%( m.label, name) )
    
    if imADialog:
        srcList.append( sMenuConfig%'self' )
    else:
        srcList.append( sMenuConfig%rootName )
    
    srcList.append('\n\n')
    
    if imADialog:
        target = 'self.' + rootName
        bindL = [b.replace(target,'self') for b in bindL]
            
    srcList.extend( bindL )
    
    #print('In getMenuSource')
    #for src in srcList:
    #    print(src)
    #print()
    
    return srcList


def getMenuFunctionSource( menuL, rootName='MainWin' ):
    pass

if __name__ == "__main__":
    
    descStr='''
File
    New
        Worksheet
        Text File
    Open
    Save
    
    Exit
Edit
    Find
    Copy
    Cut
    Paste
    '''
    
    menuL = buildMenuSource( descStr )
    print( menuL )
    print( '-'*55 )
    
    menuSrcL = getMenuSource( menuL, rootName='master'  )
    for line in menuSrcL:
        print(line, end='')
    print( '======================================================' )
    
    #fOut = file('test.py','w')
    print( '''
from Tkinter import *

class Mytestapp:
    def __init__(self, %s):
'''%'master' )
    for line in menuSrcL:
        print( line, end='')
        
    print( '''root = Tk()
app = Mytestapp(root)
root.mainloop()
''' )

    #fOut.close()
    