#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import print_function

"""Generates a list of Component objects in order of tab_label dependence."""

class CNode( object ):
    
    def __init__(self, comp_name, tab_label, component):
        
        self.comp_name = comp_name
        self.tab_label = tab_label
        self.component = component

    def __str__(self):
        return '<%s, %s>'%(self.comp_name, self.tab_label)
        
class ComponentTree(object):
    """Creates a Tree of interdependent Component objects"""
    def __init__(self):
        
        self.containerD = {'Main':[]} # index=container_name: value=list of CNode components in container
        self.compD = {} # index=comp_name: value=CNode
        
        
    def add_node(self, node):
        
        # if container is not in containerD, put it in
        if node.tab_label not in self.containerD:
            self.containerD[ node.tab_label ] = []
            
        self.containerD[ node.tab_label ].append( node )
        self.compD[ node.comp_name ] = node
        
    def get_ordered_components(self):
        """Generates a list of Component objects in order of tab_label dependence."""
        def get_next( tab_label, resultL ):
            if tab_label is None:
                tab_label = "Main"
                
            compL = sorted( self.containerD[tab_label], key=lambda c: c.comp_name )
            #print( tab_label, [str(c) for c in compL] )
            #print()
            resultL.extend( compL )
            
            nextL = []
            for c in compL:
                if c.comp_name in self.containerD:
                    nextL.append( c )
            
            for c in nextL:
                get_next(c.comp_name, resultL)
        
        ansL = []
        get_next( None, ansL )
        #print('Sorted Comp:', [c.comp_name for c in ansL] )
        
        # need to resort Tab objects for order added to Notebook
        final_ansL = []
        tabL = []
        for cn in ansL:
            
            if cn.comp_name.startswith('Tab'):
                c = cn.component
                tabL.append( (c.row, c.col, c.widget_name, c.user_tkOptionD['text'], cn) )
                tabL = sorted( tabL )
            else:
                if tabL:
                    for _,_,widget_name,_,cn_tab in tabL:
                        final_ansL.append( cn_tab )
                    tabL = []
                
                final_ansL.append( cn )
        # maybe clean up strggler Tab objects
        if tabL:
            for _,_,widget_name,_,cn_tab in tabL:
                final_ansL.append( cn_tab )
        #print('Final Sorted Comp:', [c.comp_name for c in final_ansL] )
        
        return final_ansL


if __name__ == "__main__":
    
    ct = ComponentTree()
    ct.add_node( CNode('Frame_3', 'Main', 'Frame_3_Component') )

    ct.add_node( CNode('Button_4', 'Main', 'Button_4_Component') )

    ct.add_node( CNode('Button_2', 'Main', 'Button_2_Component') )
    ct.add_node( CNode('Button_3', 'Frame_1', 'Button_3_Component') )
    
    ct.add_node( CNode('Button_1', 'Main', 'Button_1_Component') )
        
    ct.add_node( CNode('Frame_1', 'Main', 'Frame_1_Component') )
    ct.add_node( CNode('Frame_2', 'Main', 'Frame_2_Component') )

    ct.add_node( CNode('Button_5', 'Frame_3', 'Button_5_Component') )
    
    print('ct.containerD.keys() =',ct.containerD.keys())
    print('-'*55)
    
    for key,valL in  ct.containerD.items():
        print(key, [str(val) for val in valL])
    print('-'*55)
    
    compL = ct.get_ordered_components()
    for c in compL:
        print( c )

    
    
        
        