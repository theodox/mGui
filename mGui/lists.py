'''
Created on Mar 15, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds
import mGui.forms as forms
import mGui.observable as observable
import mGui.controls as controls
import mGui.bindings as b

class ListForm(forms.VerticalForm):
    
    _BIND_TGT = 'Collection'
    
    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.Collection = observable.BoundCollection(self.create_item)
        self.Collection.CollectionChanged += self.redraw
        
    def create_item(self, item):
        r = controls.Text(str(id(item)), label=str(item), parent = self) 
        (r + 'label' << b.BindProxy(item, 'Name'))()  # NO WORKY
        return r
        
    def redraw(self, *args, **kwargs):
        _collection = self.Collection.Contents
        delenda = [i for i in self.Controls if i not in _collection]
        for item in delenda:
            cmds.deleteUI(item)
        self.Controls = [i for i in self.Collection]
        print delenda, self.Controls
        an = []
        for item in self.Controls:
            an.append ((item, 'left'))
            an.append ((item, 'right'))          
            an.append ((item, 'top'))
            an.append ((item, 'bottom'))
        self.attachNone = an
        self.layout()
        
        
## kind of working for object collections... needs testing and bullet proofing
## after that - need to make sure that the factory functions preserve bindings - the example here does not work
