#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function

from tkgridgui.src_templates import createWidget, gridWidget, makeStringVar, \
                          makeOptionString, traceStringVar, bindWidget

create_callD = {} # index=widget_type: value=Tk call
create_callD['Button']      = 'Button' 
create_callD['Canvas']      = 'Canvas' 
create_callD['Checkbutton'] = 'Checkbutton' 
create_callD['Combobox']    = 'Combobox' 
create_callD['Entry']       = 'Entry' 
create_callD['Frame']       = 'Frame'
create_callD['Label']       = 'Label' 
create_callD['LabelFrame']  = 'LabelFrame'
create_callD['Listbox']     = 'Listbox' 
create_callD['Message']     = 'Message' 
create_callD['Menubutton']  = 'Menubutton' 
create_callD['Notebook']    = 'Notebook '
create_callD['OptionMenu']  = 'OptionMenu'
create_callD['Progressbar'] = 'Progressbar'
create_callD['Radiobutton'] = 'Radiobutton' 
create_callD['RadioGroup']  = 'LabelFrame'  # <== note that RadioGroup is a LabelFrame 
create_callD['Scale']       = 'Scale' 
create_callD['Separator']   = 'Separator' 
create_callD['Spinbox']     = 'Spinbox' 
create_callD['Text']        = 'Text' 
create_callD['Treeview']    = 'Treeview'

create_callD['Tab']         = 'Frame'


# widget with bind events don't also have traceStringVar
widget_bindD = {} # index=widget_type: value=bind option (e.g. "<ButtonRelease-1>" )
widget_bindD['Button']   = "ButtonRelease-1" # left click release
widget_bindD['Canvas']   = "ButtonRelease-1" # left click release
widget_bindD['Listbox']  = "ButtonRelease-1" # left click release
widget_bindD['Treeview'] = "ButtonRelease-1" # left click release

stringvar_set = set(['Entry', 'OptionMenu', 'Combobox', 'Checkbutton', 
                     'Menubutton', 'Radiobutton', 'Scale', 'Spinbox'])

sv_monikerD = {} # option name of StringVar.  either 'textvariable' or 'variable'
sv_monikerD['Entry']       = 'textvariable'
sv_monikerD['OptionMenu']  = 'textvariable'
sv_monikerD['Combobox']    = 'textvariable'
sv_monikerD['Checkbutton'] = 'variable'
sv_monikerD['Menubutton']  = 'textvariable'
sv_monikerD['Radiobutton'] = 'variable'
sv_monikerD['Scale']       = 'variable'
sv_monikerD['Spinbox']     = 'textvariable'

sv_config_D = {} # index=widget_type: value=dict of config statements. e.g. ('onvalue="yes"', 'offvalue="no"')
sv_config_D['Entry'] = {}
sv_config_D['OptionMenu'] = {}
sv_config_D['Combobox'] = {}
sv_config_D['Checkbutton'] = {'onvalue':"yes", 'offvalue':"no"}
sv_config_D['Menubutton'] = {'text':"Select"}
sv_config_D['Radiobutton'] = {}
sv_config_D['Scale'] = {}
sv_config_D['Spinbox'] = {'from_':"1", 'to':'10'}

class CompSrcGen( object ):
    
    def __init__(self, widget_name, widget_type, guiType, parent_name, 
                 row, col, opDict=None, target_app=None):
        """Source Generation for individual Widgets"""
        
        self.widget_name = widget_name
        self.widget_type = widget_type
        self.guiType = guiType
        self.parent_name = parent_name
        self.target_app = target_app # holds application data
    
        if guiType=='dialog':
            if parent_name=="Main":
                self.master = 'self.dialogframe'
            else:
                self.master = 'self.'+parent_name
        else:
            if parent_name=="Main":
                self.master = 'self.grid_frame'
            else:
                self.master = 'self.'+parent_name
        
        
        self.row = row
        self.col = col
        
        if opDict is None:
            opDict = {}
        self.opDict = opDict
        
        if widget_type in stringvar_set:
            self.svar_name = widget_name + '_StringVar'
        else:
            self.svar_name = ''
    
    def set_stringvar_name( self, svar_name ):
        """Radiobutton widgets need a common svar_name."""
        self.svar_name = svar_name
    
    def get_call_make_stmt(self):
        """Use this like: self.make_Button_1() in Tk app __init__ """
        s = '        self.make_%s( %s )'%(self.widget_name, self.master)
        if len(s) < 55:
            s = s + " "*(55-len(s))
            
        docstring =  self.target_app.compObjD[self.widget_name].get_docstring()
            
        s = s + '#%s\n'%docstring
        return s
        
    def get_top_of_make_def(self):
        s = '    def make_%s(self, frame):\n'%self.widget_name
        ansL = [s]
        
        docstring =  self.target_app.compObjD[self.widget_name].get_docstring()
        ansL.append('        """%s"""\n'%docstring)
        
        # need special logic for OptionMenu
        if self.widget_type == "OptionMenu":
            ansL.append( makeStringVar( self.widget_name ) )
            ansL.append( '        choicesT = ("Pie", "Cake", "Kale")\n' )
            s = self.get_create_widget()
            s = s.replace(')',', self.%s, *choicesT)'%(self.svar_name,)  )
            ansL.append( s )
            
            opstr = makeOptionString( {'width':self.opDict.get('width','20'),
                                       'height':self.opDict.get('height','2')}, startComma=0 )
            s = '        self.%s.configure( %s )\n'%( self.widget_name, opstr)
            ansL.append( s )
            
            ansL.append( self.get_grid_stmt() )
        
        elif self.widget_type == "Radiobutton":
            ansL.append( self.get_create_widget() )
            ansL.append( self.get_grid_stmt() )
            # assume that common svar_name is placed elsewhere
        
        elif self.widget_type == "Tab":
            ansL.append( self.get_create_widget() )
            ansL.append( '        self.{parent_name}.add( self.{widget_name}, text="{tab_label}" )'.\
                         format(parent_name=self.parent_name, widget_name=self.widget_name, tab_label=self.opDict['text'] ))
        
        else:
            ansL.append( self.get_create_widget() )
            
            if self.opDict.get('scrolly',''):
                ansL[-1] = ansL[-1].replace(', scrolly="yes"', '')
            
            ansL.append( self.get_grid_stmt() )
            
            if self.svar_name:
                ansL.append( makeStringVar( self.widget_name ) )
        
        ansL.append('\n')
        return ansL
    
    def get_callback_name(self):
        """for bind options, need a callback method"""
        return '%s_Callback'%self.svar_name
    
    def get_user_part_of_make_def(self):
        ansL = ['\n']
        
        if self.widget_type == "OptionMenu":
            
            ansL.append( "        self.%s.set('')\n"%self.svar_name )
            ansL.append( "        self.%s['menu'].delete(0, 'end')\n"%self.widget_name )
            ansL.append( "        \n" )
            ansL.append( "        new_choiceT = ('Pop1','Pop2','Weasel')\n" )
            ansL.append( "        for choice in new_choiceT:\n" )
            ansL.append( "            self.%s['menu'].add_command(label=choice, "%self.widget_name +\
                         "command=set_command(self.%s, choice))\n"%self.svar_name )

            ansL.append( "        self.%s.set('%%s'%%new_choiceT[0])\n"%(self.svar_name, ) )

            ansL.append("\n")
            ansL.append("        # add trace last so above changes do not trigger trace\n")
            ansL.append( traceStringVar( self.widget_name ) ) 
        
        elif self.widget_type == "Radiobutton":
            # connect widget to StringVar and configure any StringVar options (e.g. onvalue, from_, etc.)
            wn, wt = self.widget_name, self.widget_type
            opDict = sv_config_D[wt]
            opstr = makeOptionString( opDict )
            s = '        self.%s.configure(%s=self.%s%s)\n'%(wn, sv_monikerD[wt], self.svar_name, opstr)
            ansL.append( s )
            
            # trace is done with common StringVar
        
        elif self.svar_name:
            wn, wt = self.widget_name, self.widget_type
            
            # connect widget to StringVar and configure any StringVar options (e.g. onvalue, from_, etc.)
            opDict = sv_config_D[wt]
            opstr = makeOptionString( opDict )
            s = '        self.%s.configure(%s=self.%s%s)\n'%(wn, sv_monikerD[wt], self.svar_name, opstr)
            ansL.append( s )
            
            # may want to set StringVar before traceStringVar is enabled.
            s = self.get_string_var_set_stmt()
            if s: 
                ansL.append( s )
            
            # set StringVar for Combobox
            if wt=="Combobox":
                val = self.target_app.compObjD[wn].user_tkOptionD.get('selection','')
                if not val:
                    val = self.target_app.compObjD[wn].user_tkOptionD['values'].split()[0]
                
                ansL.append( '        self.%s.set( "%s" )\n'%(self.svar_name, val) )
            
            # set trace option on StringVar to call xxx_Callback whenever StringVar changes
            ansL.append( traceStringVar( self.widget_name ) )

        if self.widget_type == "Listbox":
            wn, wt = self.widget_name, self.widget_type
            ansL.extend(['\n','        # Edit the Listbox Entries\n',
            '''        self.%s.insert(END, "apples")\n'''%wn,
            '''        self.%s.insert(END, "oranges")\n'''%wn,
            '''        self.%s.insert(END, "grapes")\n'''%wn,   '\n'] )
        
        elif self.widget_type == "Canvas":
            ansL.append( "        self.%s.config(bg='#ffffcc')\n"%self.widget_name )

        elif self.widget_type == "Treeview":
            wn, wt = self.widget_name, self.widget_type
            
            ansL.extend(['\n',
                """        self.%s.insert('', 'end', 'widgets', text='Widget Tour')\n"""%wn,
                """        # Same thing, but inserted as first child:\n""",
                """        self.%s.insert('', 0, 'gallery', text='%s')\n"""%(wn,wn),
                """        # Inserted underneath an existing node:\n"""])
            
            for item_name in sorted( create_callD.keys() ):
                ansL.append( """        self.%s.insert('widgets', 'end', text='%s')\n"""%(wn, item_name) )
            
            ansL.extend(['\n',
                """        # Treeview chooses the id:\n""",
                """        id = self.%s.insert('', 'end', text='Tutorial')\n"""%wn,
                """        self.%s.insert(id, 'end', text='Tree')\n"""%wn,
                '\n'])

        # maybe attach a bind statement 
        s = self.get_bind_stmt()
        if s:
            ansL.append( s )
        
        if len(ansL)>1:
            ansL.append('\n')
        return ansL
    
    def get_create_widget(self):
        """initial widget creation statement e.g. b=Button(frame)"""
        
        s = createWidget(self.widget_name, create_callD[self.widget_type], 
                         self.guiType, self.parent_name, self.opDict)
        return s.replace( self.master, 'frame' )
    
    def get_click_name(self):
        """for bind options, need a callback method"""
        return '%s_Click'%self.widget_name
    
    def get_bind_stmt(self):
        if self.widget_type in widget_bindD:
            wn, wt = self.widget_name, self.widget_type
            return bindWidget( wn, widget_bindD[wt] , self.get_click_name() )
        else:
            return ''
        
    
    def get_grid_stmt(self):
        """create grid statement e.g.  self.Canvas.grid(row=1, column=1)"""
        
        sticky = self.opDict.get('sticky','')
        rowspan = self.opDict.get('rowspan','')
        columnspan = self.opDict.get('columnspan','')
        
        # gridWidget(wName,    row, col, is_gridWidgetFrame, sticky='', rowspan='', columnspan='')
        if (self.opDict.get('scrolly','')=='yes') or (self.opDict.get('scrollx','')=='yes'):
            return gridWidget(self.widget_name+'_frame', self.row, self.col, False, 
                              sticky, rowspan, columnspan)
        else:
            return gridWidget(self.widget_name, self.row, self.col, False, 
                              sticky, rowspan, columnspan)
    
    def get_string_var_set_stmt(self):
        
        if self.svar_name:
            wn, wt = self.widget_name, self.widget_type
            opDict = sv_config_D[wt]
            if opDict:
                keyL = sorted( opDict.keys() )
                val = opDict[keyL[0]] # take 1st option in alphabetically sorted keys
                return '        self.%s.set("%s")\n'%(self.svar_name, val)
            else:
                return ''
        else:
            return ''
    
    def get_string_var_stmts(self):
        """"""
        ansL = []
        
        if self.svar_name:
            wn, wt = self.widget_name, self.widget_type
            
            # create a StringVar
            ansL.append( makeStringVar( wn ) )
            
            # connect widget to StringVar and configure any StringVar options (e.g. onvalue, from_, etc.)
            opDict = sv_config_D[wt]
            opstr = makeOptionString( opDict )
            s = '        self.%s.configure(%s=self.%s%s)\n'%(wn, sv_monikerD[wt], self.svar_name, opstr)
            ansL.append( s )
            
            # may want to set StringVar before traceStringVar is enabled.
            s = self.get_string_var_set_stmt()
            if s: 
                ansL.append( s )
            
            # set trace option on StringVar to call xxx_Callback whenever StringVar changes
            ansL.append( traceStringVar( self.widget_name ) )
        return ansL


    def get_top_of_bind_def(self):
        """get the top code for the bind method def statement """
        
        if self.widget_type in widget_bindD:
            ansL = []
            wn, wt = self.widget_name, self.widget_type
            methodName = self.get_click_name()
            
            ansL.append('    def %s(self, event): #bind method for component ID=%s\n'%(methodName, wn))
                    
            docstring =  self.target_app.compObjD[self.widget_name].get_docstring()
            ansL.append('        """%s"""\n'%docstring)
            
            ansL.append('        pass\n')
            
            return ansL
        else:
            return []
        
    
    def get_user_part_of_bind_def(self):
        """get the user code for the bind method def statement """
        ansL = []
        
        if self.widget_type in widget_bindD:
            ansL = []
            wn, wt = self.widget_name, self.widget_type
            methodName = self.get_click_name()
            
            ansL.append('        # replace, delete, or comment-out the following\n')
            ansL.append('        print( "executed method %s" )\n'%methodName)
            
            if self.target_app.getSpecialOption('hasstatusbar')=='yes':
                ansL.append('        self.statusMessage.set("executed method %s")\n'%methodName )
            
            ansL.append('\n')
            
        if self.widget_type == 'Listbox':
            ansL.append('        print( "current selection(s) =",self.%s.curselection() )\n'%wn )
            ansL.append('        labelL = []\n' )
            ansL.append('        for i in self.%s.curselection():\n'%wn )
            ansL.append('            labelL.append( self.%s.get(i))\n'%wn )
            ansL.append('        print( "current label(s) =",labelL )\n')
            ansL.append('        # use self.%s.insert(0, "item zero")\n'%wn)
            ansL.append('        #     self.%s.insert(index, "item i")\n'%wn)
            ansL.append('        #            OR\n')
            ansL.append('        #     self.%s.insert(END, "item end")\n'%wn)
            ansL.append('        #   to insert items into the list box\n')
            
        elif self.widget_type == 'Canvas':
            ansL.append('        print( "clicked in canvas at x,y =",event.x,event.y )\n')
            ansL.append('        w = int(self.%s.cget("width"))\n'%(wn,))
            ansL.append('        h = int(self.%s.cget("height"))\n'%(wn,))
            ansL.append('        self.%s.create_rectangle((2, 2, w+1, h+1), outline="blue")\n'%(wn,))
            ansL.append('        self.%s.create_line(0, 0, w+2, h+2, fill="red")\n'%(wn,))
            ansL.append('        x = int(event.x)\n')
            ansL.append('        y = int(event.y)\n')
            ansL.append('        print( "event x,y=",x,y )\n')
            ansL.append('        self.%s.create_text(x,y, text="NE", fill="green", anchor=NE)\n'%(wn,))
            ansL.append('        self.%s.create_text(x,y, text="SW", fill="magenta", anchor=SW)\n'%(wn,))

            
        elif self.widget_type == 'Treeview':
            ansL.append('        curItem = self.%s.focus()\n'%wn )
            ansL.append('        print( "current Treeview item(s) =",self.%s.item( curItem ) )\n'%wn )


        return ansL
        
    
    def get_trace_name(self):
        return '%s_StringVar_traceName'%self.widget_name
        
    def get_top_of_trace_def(self):
        """get the top code for the trace method def statement """
        
        if self.svar_name:
            ansL = []
            
            methodName = self.get_callback_name()
            ansL.append('    def %s(self, varName, index, mode):\n'%methodName)
                    
            docstring =  self.target_app.compObjD[self.widget_name].get_docstring()
            ansL.append('        """%s"""\n'%docstring)
            
            ansL.append('        pass\n')
            
            ansL.append('\n')
            return ansL
        else:
            return []
                    
        
    def get_user_part_of_trace_def(self):
        """get the user code for the trace method def statement """
                
        if self.svar_name:
            ansL = []

            methodName = self.get_callback_name()
            ansL.append('        # replace, delete, or comment-out the following\n')
            ansL.append('        print( "%s varName, index, mode",varName, index, mode )\n'%methodName)
        
            if self.target_app.getSpecialOption('hasstatusbar')=='yes':
                ansL.append('        self.statusMessage.set("    %s = "+self.%s.get())\n'%(self.svar_name,self.svar_name))
            ansL.append('        print( "    new StringVar value =",self.%s.get() )\n\n'%self.svar_name )


            ansL.append('\n')
            return ansL
        else:
            return []
        
        

if __name__ == '__main__':
    import sys
    from tkgridgui.target_tk_app_def import TargetTkAppDef
    from tkgridgui.src_templates import beginSourceFile, get_top_imports, endSourceFile
    import tkgridgui.SourceCode as SourceCode
    sourceFile = SourceCode.SourceFile( 'component_src_gen_test.py' )
    
    tkOptionD = {}
    
    class Dummy(object):
        def __init__(self):
            self.user_tkOptionD = {'values':'One Two Three'}
        def get_docstring(self):
            return 'ima_docstring'
    dummy = Dummy()
        
    target_app = TargetTkAppDef( 'myTestApp' )
    target_app.tkOptionD['background']='yellow'
    target_app.app_attrD = {'hasstatusbar':'no'}
        
    
    # make import section
    sourceFile.addSection('imports', get_top_imports(1,1,1), defaultUserCodeL='# Place any user import statements here\n\n')

    # body of __init__
    classInitL = [beginSourceFile('_MyApp', 400, 300, tkOptionD)]
    classInitL.append('        self.master.title("%s")\n'%"MyApp"  )
    
    classInitUserSectionL = []
    
    widget_typeL = sorted( create_callD.keys() )
    sortL = []
    for i,widget_type in enumerate(widget_typeL):
        guiType = 'main'
        parent_name = 'Main'
        opDict = [ {}, {'sticky':'se'}, {'sticky':'nw'}][i % 3]
        opDict['text'] = 'text'
        row, col = divmod( i, 5 )
        
        c = CompSrcGen(widget_type+'_1', widget_type, guiType, parent_name, row, col, opDict, 
            target_app=target_app)
        sortL.append( c )
        target_app.compObjD[ widget_type+'_1' ] = dummy # simulate an active target_app
        
        classInitL.append( c.get_call_make_stmt() )
    sourceFile.addSection('top_of_init', classInitL, defaultUserCodeL=classInitUserSectionL)
    
    # add make widget routines
    for c in sortL:
        sourceFile.addSection( 'make_%s'%c.widget_name, c.get_top_of_make_def(), 
                               defaultUserCodeL=c.get_user_part_of_make_def() )
    
    # add any bind routines
    for c in sortL:
        topL = c.get_top_of_bind_def()
        if topL:
            methodName = c.get_click_name()
            sourceFile.addSection( methodName, topL, 
                                   defaultUserCodeL=c.get_user_part_of_bind_def() )
    
    # add any StringVar trace routines
    for c in sortL:
        topL = c.get_top_of_trace_def()
        if topL:
            methodName = c.get_trace_name()
            sourceFile.addSection( methodName, topL, 
                                   defaultUserCodeL=c.get_user_part_of_trace_def() )



    sourceFile.addSection('end', endSourceFile('_MyApp') , allowUserCode=0)


    sourceFile.saveToFile( sys.stdout ) # simulate a save with stdout


    sys.exit()
    # ====================================================================================
    def show_create(   widget_name, widget_type, guiType, parent_name, row, col, opDict ):
        c = CompSrcGen(widget_name, widget_type, guiType, parent_name, row, col, opDict, target_app=target_app)
        
        print( c.get_call_make_stmt().rstrip() )
        print( c.get_create_widget().rstrip() )
        print( c.get_grid_stmt().rstrip() )
        
        s = c.get_bind_stmt()
        if s:
            print( s.rstrip() )
        
        ansL = c.get_string_var_stmts()
        for line in ansL:
            print( line.rstrip() )
        print('  - - - - - - - ')

    #show_create('Button_1',    'Button',    'main','Main',    1,2,{'sticky':'se'})
    #show_create('RadioGroup_1','RadioGroup','main','Frame_1', 3,4,None)
    #show_create('Entry_1',     'Entry',     'main','Frame_1', 5,6,None)

    cL = sorted( create_callD.keys() )
    for ic,c in enumerate(cL):
        
        guiType = ['main','dialog'][ic % 2]
        parent_name = ['Main','Frame_1'][ic % 2]
        opDict = [None, {}, {'sticky':'se'}][ic % 3]
        
        row, col = divmod( ic, 5 )
        show_create( c+'_1', c, guiType, parent_name, row, col, opDict )
        

