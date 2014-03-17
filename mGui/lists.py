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
    def __init_bound_collection__(self, kwargs):
        '''
        initialize the mixin. Call after the layout constructor, eg:
        
            super(MyBoundFormClass, self).__init__(key, *args, **kwargs)
            self.__init_bound_collection__()
        
        '''
        self.Template = ItemTemplate(self)  # default
        if 'template' in kwargs:
            self.ItemTemplate = kwargs['template']
            del kwargs['template']
        
        self.Collection = observable.BoundCollection(self.Template)
        self.Collection.CollectionChanged += self.redraw
  
        
    def redraw(self, *args, **kwargs):
        '''
        redraw the GUI for this item when the collection changes
        '''
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
        
    def set_template(self, template):
        '''
        sets the item template for this list
        '''
        self.Template = template
        


class VerticalList(forms.VerticalForm, ListFormBase):
    '''
    A vertical list of items with an automatic scrollbar
    '''

    def __init__(self, key, *args, **kwargs):
        
        self.ScrollLayout = layouts.ScrollLayout(key = "_scroll", *args)
        self.ScrollLayout.__enter__()

        self.__init_bound_collection__(kwargs)    
        super(VerticalList, self).__init__(key, *args, **kwargs)
        
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
    '''
    A horizontal list of Items with an automatic scrollbar
    '''
    def __init__(self, key, *args, **kwargs):
        self.ScrollLayout = layouts.ScrollLayout(key = "_scroll", *args)
        self.ScrollLayout.__enter__()
        self.__init_bound_collection__(kwargs)    
        super(HorizontalList, self).__init__(key, *args, **kwargs)
        self.__enter__()
        self.__exit__(None, None, None)
        self.ScrollLayout.__exit__(None, None, None)
        
    def layout(self):
        super(HorizontalList, self).layout()
        if len(self.Controls):
            self.attachNone = (self.Controls[-1], 'right')

class WrapList(layouts.FlowLayout, ListFormBase):
    '''
    A flowLayout based list of items with optional wrapping. This will clip if
    the width exceeds the layout width unles 'wrap' is set to true
    '''
    def __init__(self, key, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(WrapList, self).__init__(key, *args, **kwargs)

        self.__enter__()
        self.__exit__(None, None, None)


class ItemTemplate(object):
    '''
    Base class for item template classes.
    
    The job of an itemTemplate is to provide a GUI widget (which can be a single
    control or a layout with other controls) that represents the underying data
    item in the bound data collection.  
    
    '''
    def __init__(self, parent, **handlers):
        self.Parent = parent
        self.Handlers = handlers
        
    def widget(self, item):
        r = controls.Button(0, label=str(item), parent = self.Parent) 
        for message, handler in self.Handlers.items():
           r_event = getattr(r, message)
           r_event += handler
        return r
    
    def __call__ (self, item):
        return self.widget(item)
        
        