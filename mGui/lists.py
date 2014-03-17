'''
Created on Mar 15, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds
import mGui.forms as forms
import mGui.observable as observable
import mGui.controls as controls
import mGui.bindings as b
import mGui.layouts as layouts

class ListFormBase(object):
    
    '''
    Adds a BoundCollection to a Layout class. Will call the owning class's
    layout() method when the collection changes, and will prune the layouts
    control sets as items are added to or removed from the bound collection.
    '''
    def __init_bound_collection__(self):
        '''
        initialize the mixin. Call after the layout constructor, eg:
        
            super(MyBoundFormClass, self).__init__(key, *args, **kwargs)
            self.__init_bound_collection__()
        
        '''
        self.Collection = observable.BoundCollection(self.create_item)
        self.Collection.CollectionChanged += self.redraw
        
    def create_item(self, item):
        r = controls.IconTextButton(str(id(item)),
                                     label=str(item),
                                      ann = "hello", 
                                      st = "textOnly",
                                      parent = self) 
        r.command += self.clickHandler
        return r
        
    def redraw(self, *args, **kwargs):
        _collection = self.Collection.Contents
        delenda = [i for i in self.Controls if i not in _collection]
        for item in delenda:
            cmds.deleteUI(item)
        self.Controls = [i for i in self.Collection]

        an = []
        for item in self.Controls:
            an.append ((item, 'left'))
            an.append ((item, 'right'))          
            an.append ((item, 'top'))
            an.append ((item, 'bottom'))
        self.attachNone = an
        self.layout()
        
    def clickHandler(self, *args, **kwargs):
        print args, kwargs
        
class VerticalList(forms.VerticalForm, ListFormBase):

    def __init__(self, key, *args, **kwargs):
        self.ScrollLayout = layouts.ScrollLayout(key = "_scroll", *args, **kwargs)
        self.ScrollLayout.__enter__()
        super(VerticalList, self).__init__(key, *args, **kwargs)
        self.__init_bound_collection__()
        self.__enter__()
        self.__exit__(None, None, None)
        self.ScrollLayout.__exit__(None, None, None)
        ## the enter/exits make sure that you can place a listForm as a single control without it
        ## trying to gobble up subsequent objects
        
    def layout(self):
        super(VerticalList, self).layout()
        if len(self.Controls):
            self.attachNone = (self.Controls[-1], 'bottom')

class HorizontalList(forms.HorizontalForm, ListFormBase):

    def __init__(self, key, *args, **kwargs):
        self.ScrollLayout = layouts.ScrollLayout(key = "_scroll", *args, **kwargs)
        self.ScrollLayout.__enter__()
        super(HorizontalList, self).__init__(key, *args, **kwargs)
        self.__init_bound_collection__()
        self.__enter__()
        self.__exit__(None, None, None)
        self.ScrollLayout.__exit__(None, None, None)
        
    def layout(self):
        super(HorizontalList, self).layout()
        if len(self.Controls):
            self.attachNone = (self.Controls[-1], 'right')
