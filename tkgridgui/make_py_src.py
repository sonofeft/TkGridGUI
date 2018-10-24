#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function

from tkgridgui.src_templates import *
import tkgridgui.SourceCode as SourceCode
import tkgridgui.make_menu_src as make_menu_src
#from tkgridgui.src_templates import legalPythonIdentifier
from tkgridgui.comp_tree import CNode, ComponentTree
from tkgridgui.component_src_gen import CompSrcGen

class FormSource( object ):
    
    def __init__(self, target_app, MainWin, grid_gui):
        self.target_app = target_app
        self.MainWin = MainWin
        self.grid_gui = grid_gui
                
        if self.MainWin.mainOrDialog.get() == "dialog":
            self.pyFile = grid_gui.current_fileFullName[:-4] + '_Dialog.py'
            self.imADialog = 1
        else:
            self.pyFile = grid_gui.current_fileFullName[:-3] + 'py'
            self.imADialog = 0
        self.sourceFile = SourceCode.SourceFile( self.pyFile )
        self.getClassAndInit()
    
    def saveToFile(self):
        self.sourceFile.saveToFile()
    
    def getClassAndInit(self):
    
        # make class statement and top of __init__
        w = self.target_app.app_attrD['width']
        h = self.target_app.app_attrD['height']
        name = '_'+self.target_app.app_attrD['name'] # add underscore to beginning (preclude name collision)
        
        #self.importSectionL = ['from Tkinter import *\n']
        
        # include standard dialog imports if flags are set.
        self.importSectionL = [ get_top_imports( self.MainWin.stdDialMessChkBox_StringVar.get()=='yes', 
                                                 self.MainWin.stdDialFileChkBox_StringVar.get()=='yes', 
                                                 self.MainWin.stdDialColorChkBox_StringVar.get()=='yes') ]
        
        self.classInitUserSectionL = []

        if self.imADialog:
            if self.MainWin.hideOkChkBox_StringVar.get()=="yes":
                self.classInitL = [beginDialogSourceFile(name, 1, w, h, self.target_app.tkOptionD)]
            else:
                self.classInitL = [beginDialogSourceFile(name, 0, w, h, self.target_app.tkOptionD)]
                
            # don't let the widow be too small
            if w<=300 and h<=200:
                self.classInitL.append('        self.geometry("300x200")\n' )
        else:
            self.classInitL = [beginSourceFile(name, w, h, self.target_app.tkOptionD)]
            
            # don't let the widow be too small
            if w<=300 and h<=200:
                self.classInitL.append('        self.master.geometry("300x200")\n' )
            
            self.classInitL.append('        self.master.title("%s")\n'%(self.target_app.app_attrD['name'],))

        guiType = self.MainWin.mainOrDialog.get()

        # make end code while name is right
        if guiType == "dialog":
            self.endCode = endDialogSourceFile(name)
        else:
            self.endCode = endSourceFile(name)
        
        # dictionary of radio groups (need to detect and assign groups to single StringVar)
        radio_group_D = {}
        # =====================================================================================
        # sort widgets into parent dependency and alphabetical order
        
        ct = ComponentTree()
        for widget_name, c in self.target_app.compObjD.items():
            ct.add_node( CNode(widget_name, c.tab_label, c) )
                
        cnodeL = ct.get_ordered_components()
        dependency_sorted_compL = []
        for cn in cnodeL:
            c = cn.component
            dependency_sorted_compL.append( (c.widget_type, c.widget_name, c) )
                
        
        # create list of source gen components
        comp_srcgenL = []
        rg_svarL = [] # any radio group StringVar
        makeL = [] # all the make calls for Widgets
        for widget_type, widget_name, comp in dependency_sorted_compL:
            
            c = CompSrcGen(widget_name, widget_type, guiType, 
                           comp.tab_label, comp.row, comp.col, comp.user_tkOptionD, 
                           target_app=self.target_app)
            
            if comp.widget_type == "Radiobutton":
                if comp.tab_label.startswith('RadioGroup'):
                    gName = comp.tab_label
                else:
                    gName = 'RG_' + comp.tab_label # if not explicitly in a RadioGroup, assign to tab_label group
                    
                # set CompSrcGen StringVar name to common RadioGroup
                c.svar_name = gName + '_StringVar'
                
                # only create one callback routine for all of the radio buttons in the group
                if not radio_group_D.has_key( gName ):
                    radio_group_D[ gName ] = comp.widget_name.split('_')[-1] # set to 1st encountered
                    
                    rg_svarL.append( '        self.%s_StringVar = StringVar()\n'%gName )
                           
            comp_srcgenL.append( c ) # a list of all CompSrcGen objects
            
            makeL.append( c.get_call_make_stmt() )
        
        if rg_svarL:
            self.classInitL.append('\n')
            self.classInitL.extend( rg_svarL )
        
        self.classInitL.append('\n')
        self.classInitL.extend( makeL )
        self.classInitL.append('\n')
        
        # add any columnconfigure(col, weight=wt) or rowconfigure(row, weight=wt)
        wts_rowD, wts_colD = self.target_app.get_a_full_desc_of_weights()
        
        for (tab_label, row_target), wt in wts_rowD.items():
            #print('Need to Row configure ',(tab_label, row_target),' to ',wt)
            self.classInitL.append( createWeightStatement(guiType, tab_label, True, row_target, wt) )
        
        for (tab_label, col_target), wt in wts_colD.items():
            #print('Need to Column configure ',(tab_label, col_target),' to ',wt)
            self.classInitL.append( createWeightStatement(guiType, tab_label, False, col_target, wt) )
        
        # if not resizable, set resizable to NO
        if self.MainWin.resizableChkBox_StringVar.get()=='no':
            if self.imADialog:
                self.classInitL.append('        self.resizable(0,0) # Linux may not respect this\n')
            else:
                self.classInitL.append('        self.master.resizable(0,0) # Linux may not respect this\n')
        self.classInitL.append('\n')
            
            
        # ======================================================================================
        
        # add a status bar if desired
        if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
            if self.imADialog:
                self.classInitL.append( getDialogStatusBarSource() )
            else:
                self.classInitL.append( getStatusBarSource() )
                
            self.classInitL.append('\n')
            appName = self.target_app.app_attrD['name']
            self.classInitUserSectionL.append('        self.statusMessage.set("Welcome to %s")\n'%appName)
            self.classInitUserSectionL.append('\n')

        # import section is placed 1st
        self.sourceFile.addSection('imports', self.importSectionL, defaultUserCodeL='# Place any user import statements here\n\n')
        # place top_of_init sections of code
        
        # any RadioGroup StringVar should be set
        for gName,gValue in radio_group_D.items():
            self.classInitL.append( '        self.%s.set("%s")\n'%(gName+ '_StringVar', gValue) )
            
            self.classInitL.append( '        self.%s_StringVar_traceName = self.%s_StringVar.trace_variable("w", self.%s_StringVar_Callback)\n'%\
                  (gName, gName, gName))
        
        # put Menu info in    
        if self.MainWin.menuChkBox_StringVar.get()=='yes':
            self.classInitL.append('\n')
            menuL = make_menu_src.buildMenuSource( self.target_app.getSpecialOption('menu') )
            
            add_ctrl_keys = self.target_app.getSpecialOption('add_menu_ctrl_keys') == 'yes'
            menuSrcL = make_menu_src.getMenuSource( menuL, rootName='master', imADialog=self.imADialog,
                                                    add_ctrl_keys=add_ctrl_keys)
                
            
            self.classInitL.extend( menuSrcL )
            
            #genCodeL = menuSrcL
            #defaultUserCodeL = []
            #self.sourceFile.addSection('menuStructure', genCodeL, defaultUserCodeL=defaultUserCodeL)
        
        
        
        self.sourceFile.addSection('top_of_init', self.classInitL, defaultUserCodeL=self.classInitUserSectionL)
    
        # add make widget routines
        for c in comp_srcgenL: # a list of all CompSrcGen objects
            self.sourceFile.addSection( 'make_%s'%c.widget_name, c.get_top_of_make_def(), 
                                        defaultUserCodeL=c.get_user_part_of_make_def() )
        
        # add any bind routines
        for c in comp_srcgenL: # a list of all CompSrcGen objects
            topL = c.get_top_of_bind_def()
            if topL:
                methodName = c.get_click_name()
                self.sourceFile.addSection( methodName, topL, 
                                            defaultUserCodeL=c.get_user_part_of_bind_def() )
        
        # add any StringVar trace routines
        for c in comp_srcgenL: # a list of all CompSrcGen objects
            if c.widget_type != "Radiobutton": # Radiobutton done by RadioGroup
                topL = c.get_top_of_trace_def()
                if topL:
                    methodName = c.get_trace_name()
                    self.sourceFile.addSection( methodName, topL, 
                                                defaultUserCodeL=c.get_user_part_of_trace_def() )

        # any RadioGroup StringVar need Callback method
        for gName,gValue in radio_group_D.items():
            mock_radio = CompSrcGen(gName, 'Radiobutton', guiType, 
                                    "Main",       1,  1,     {},     target_app=self.target_app)
        #                           widget_name, widget_type, guiType,  
        #                           parent_frame, row, col, opDict=None, target_app=None):
            mock_radio.svar_name = gName + '_StringVar'
                                    
            topL = mock_radio.get_top_of_trace_def()
            if topL:
                methodName = mock_radio.get_trace_name()
                self.sourceFile.addSection( methodName, topL, 
                                            defaultUserCodeL=mock_radio.get_user_part_of_trace_def() )


        if self.MainWin.menuChkBox_StringVar.get()=='yes':
            def addMenuToSource( mItem ):
                for s in mItem.subLabelL:
                    genCodeL = []
                    defaultUserCodeL = []
                    if s.lenSubmenu()==0:
                        name = legalPythonIdentifier('menu_%s_%s'%(mItem.label, s.label))
                        genCodeL.append('    def %s(self):\n'%name)
                        genCodeL.append('        pass\n')
                        defaultUserCodeL.append('        # replace, delete, or comment-out the following\n')
                        
                        if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
                            defaultUserCodeL.append('        self.statusMessage.set("called %s")\n'%name)
                            
                        defaultUserCodeL.append('        print( "called %s" )\n\n'%name)
                        self.sourceFile.addSection(name, genCodeL, defaultUserCodeL=defaultUserCodeL)
                    else:
                        addMenuToSource( s )
                        
            for mItem in menuL:
                addMenuToSource( mItem )
                
                if mItem.lenSubmenu()==0:
                        genCodeL = []
                        defaultUserCodeL = []
                        name = legalPythonIdentifier('menu_%s'%(mItem.label))
                        genCodeL.append('    def %s(self):\n'%name)
                        genCodeL.append('        pass\n')
                        defaultUserCodeL.append('        # replace, delete, or comment-out the following\n')
                        
                        if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
                            defaultUserCodeL.append('        self.statusMessage.set("called %s")\n'%name)
                        defaultUserCodeL.append('        print( "called %s" )\n\n'%name)
                        
                        self.sourceFile.addSection(name, genCodeL, defaultUserCodeL=defaultUserCodeL)
        
            

            
        # standard message dialogs
        if self.MainWin.stdDialMessChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardMessageDialogs()]
            defaultUserCodeL = []
            self.sourceFile.addSection('standard_message_dialogs', genCodeL, defaultUserCodeL=defaultUserCodeL)
        # standard file dialogs
        if self.MainWin.stdDialFileChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardFileDialogs()]
            defaultUserCodeL = []
            self.sourceFile.addSection('standard_file_dialogs', genCodeL, defaultUserCodeL=defaultUserCodeL)
        # color dialog
        if self.MainWin.stdDialColorChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardColorDialog()]
            defaultUserCodeL = []
            self.sourceFile.addSection('standard_color_dialog', genCodeL, defaultUserCodeL=defaultUserCodeL)
        # alarm logic
        if self.MainWin.stdAlarmChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardAlarmDialog()]
            defaultUserCodeL = ['        print( "Alarm called" )\n']
            self.sourceFile.addSection('standard_alarm', genCodeL, defaultUserCodeL=defaultUserCodeL)
        
            
        # if making a dialog, need to put in user-editable validate function
        if guiType == "dialog":
            genCodeL = [getDialogValidate()]
            genCodeL.append('\n')
            
            svar_set = set()
            for c in comp_srcgenL: # a list of all CompSrcGen objects
                if c.svar_name:
                    if c.svar_name not in svar_set:# only do each StringVar once.
                        if c.widget_type == "Radiobutton":
                            name = c.svar_name.replace("_StringVar","") # want group name, not individual radio button name
                        else:
                            name = c.widget_name
                        
                        genCodeL.append( '        self.result["%s"] = self.%s.get()\n'%(name, c.svar_name) )
                    svar_set.add( c.svar_name ) # remember this StringVar is done.
            genCodeL.append('\n')
            
            
            defaultUserCodeL = ['        # set values in "self.result" dictionary for return\n',
                '        # for example...\n',
                '        # self.result["age"] = self.Entry_2_StringVar.get() \n\n',
                '        self.result["test"] = "test message" \n',
                '        return 1\n']
            self.sourceFile.addSection('dialog_validate', genCodeL, defaultUserCodeL=defaultUserCodeL)
        
        #self.topCode = ''.join(self.classInitL)
        self.sourceFile.addSection('end',self.endCode, allowUserCode=0)


if __name__ == '__main__':
    import os
    from tkgridgui.target_tk_app_def import TargetTkAppDef
    
    target_app = TargetTkAppDef( 'myTestApp' )
    
    target_app.maybe_add_component( widget_type="Button", widget_name="Button_1", tab_label="Main", 
                                    row=1, col=1)
    target_app.maybe_add_component( widget_type="Entry", widget_name="Entry_1", tab_label="Main", 
                                    row=2, col=1)
    target_app.maybe_add_component( widget_type="Text", widget_name="Text_1", tab_label="Main", 
                                    row=3, col=1)
    
    class GetFunc( object ):
        def __init__(self, const):
            self.const = const
        def get(self):
            return self.const
    
    class MockMainWin( object ):
        def __init__(self):
            
            if 0:
                self.mainOrDialog = GetFunc( "main" )
                self.menuChkBox_StringVar = GetFunc( "yes" )
                self.hideOkChkBox_StringVar = GetFunc( "yes" )
            else:
                self.mainOrDialog = GetFunc( "dialog" )
                self.menuChkBox_StringVar = GetFunc( "no" )
                self.hideOkChkBox_StringVar = GetFunc( "no" )
            
            self.stdDialMessChkBox_StringVar = GetFunc( "yes" )
            self.stdDialFileChkBox_StringVar = GetFunc( "yes" )
            self.statusBarChkBox_StringVar = GetFunc( "yes" )
            self.stdDialColorChkBox_StringVar = GetFunc( "yes" )
            self.stdAlarmChkBox_StringVar = GetFunc( "yes" )
            self.resizableChkBox_StringVar = GetFunc( "yes" )
    
    class MockGridGUI( object ):
        def __init__(self):
            full_fname = os.path.abspath( "./mock.def" )
            head,tail = os.path.split( full_fname )
            
            self.current_fileFullName = full_fname
            self.current_filePath = head
            self.current_fileName = tail
    
    sf = FormSource( target_app, MockMainWin(), MockGridGUI() )
    sf.saveToFile()
    
    print
    #print( sf.topCode )
    #print( sf.endCode )