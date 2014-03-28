'''
Created on Mar 15, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds
import mGui.forms as forms
import mGui.observable as observable
import mGui.core.controls as controls
import mGui.core.layouts as layouts
import mGui.events as events


class LayoutContext(object):
    '''
    Use this to spoof the generic layout context mechanism when adding things
    like lists, where the GUI root (a scrollbar) and the logical root (the list
    collection) differ. The context will add the control reference to the dict
    of parent layout without adding the underlying widget, which would mess up
    layouts
    '''
    def __init__(self, item):
        self.items = [item]

    def __enter__(self):
        self.temp_layout = layouts.Layout.ACTIVE_LAYOUT
        return self

    def add(self, *items):
        self.items += list(items)

    def __exit__(self, exc, value, tb):
        map(self.temp_layout.add, self.items)


class FormList(object):
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
        if 'itemTemplate' in kwargs:
            self.Template = kwargs['itemTemplate'](self)
            del kwargs['itemTemplate']

        self.Collection = observable.BoundCollection(self.Template)
        self.Collection.CollectionChanged += self.redraw  # automatically forward collection changes
        self.NewWidget = events.MayaEvent()
        self.Collection.WidgetCreated += self.NewWidget


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
            an.append((item, 'left'))
            an.append((item, 'right'))
            an.append((item, 'top'))
            an.append((item, 'bottom'))
        self.attachNone = an
        self.layout()


class VerticalList(forms.VerticalForm, FormList):
    '''
    A vertical list of items with an automatic scrollbar
    '''

    def __init__(self, key, *args, **kwargs):

        with LayoutContext(self):
            self.ScrollLayout = layouts.ScrollLayout(key="_scroll", *args)
            self.ScrollLayout.__enter__()

            self.__init_bound_collection__(kwargs)
            super(VerticalList, self).__init__(key, *args, **kwargs)
            self.__enter__()
            self.__exit__(None, None, None)

            self.ScrollLayout.__exit__(None, None, None)

        # # the enter/exits make sure that you can place a listForm as a single control without it
        # # trying to gobble up subsequent objects


class HorizontalList(forms.HorizontalForm, FormList):
    '''
    A horizontal list of Items with an automatic scrollbar
    '''
    def __init__(self, key, *args, **kwargs):

        with LayoutContext(self):
            self.ScrollLayout = layouts.ScrollLayout(key="_scroll", *args)
            self.ScrollLayout.__enter__()

            self.__init_bound_collection__(kwargs)
            super(HorizontalList, self).__init__(key, *args, **kwargs)
            self.__enter__()
            self.__exit__(None, None, None)

            self.ScrollLayout.__exit__(None, None, None)


class WrapList(layouts.FlowLayout, FormList):
    '''
    A flowLayout based list of items with optional wrapping. This will clip if
    the width exceeds the layout width unles 'wrap' is set to true

    @note no scrollbars, so no need for LayoutContext
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
    def __init__(self, parent):
        self.Parent = parent

    def widget(self, item):
        r = controls.Button(0, label=str(item), parent=self.Parent)
        return {'widget': r}

    def __call__(self, item):
        return self.widget(item)

