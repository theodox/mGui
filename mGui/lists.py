"""
Lists are a bindable containers.

All list classes include an internal BoundCollection (see obervable.py) The
BoundCollections will automatically populate the list with widgets as the
underlying collection changes.

By default, entries will appear as Buttons (the labels will display the string
representation of the underlying objects). However most often users will create
custom widgets -- which can be entire miniature layouts of their own with
layouts and controls-- using custom subclasses of the ItemTemplate class (for an
example of this in action see 'modMgr.py' in the examples)

There are a variety of List classes to handle vertical, horizontal and more
complex layout needs. Lists come with inherent scollbars if their contents are
too large to display.
"""
import maya.cmds as cmds

import mGui.forms as forms
import mGui.observable as observable
import mGui.core.controls as controls
import mGui.core.layouts as layouts
import mGui.events as events


class LayoutContext(object):
    """
    Use this to spoof the generic layout context mechanism when adding things
    like lists, where the GUI root (a scrollbar) and the logical root (the list
    collection) differ. The context will add the control reference to the dict
    of parent layout without adding the underlying widget, which would mess up
    layouts
    """

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
    """
    Adds a BoundCollection to a Layout class. Will call the owning class's
    layout() method when the collection changes, and will prune the layouts
    control sets as items are added to or removed from the bound collection.
    """

    def __init_bound_collection__(self, kwargs):
        """
        initialize the mixin. Call after the layout constructor, eg:

            super(MyBoundFormClass, self).__init__(key, *args, **kwargs)
            self.__init_bound_collection__()

        """
        self.Template = ItemTemplate(self)  # default
        if 'itemTemplate' in kwargs:
            self.Template = kwargs['itemTemplate'](self)
            del kwargs['itemTemplate']

        if 'synchronous' in kwargs:
            self.Collection = observable.ImmediateBoundCollection(self.Template)
            self.NewWidget = events.Event(type='widget created')
        else:
            self.Collection = observable.BoundCollection(self.Template)
            self.NewWidget = events.MayaEvent(type='widget created')

        self.Collection.CollectionChanged += self.redraw  # automatically forward collection changes
        self.Collection.WidgetCreated += self.widget_created

    def redraw(self, *args, **kwargs):
        """
        redraw the GUI for this item when the collection changes
        """
        try:
            cmds.waitCursor(st=1)
            self.manage = False
            old_contents = set(self.Controls)
            _collection = set(self.Collection.Contents)

            delenda = list(old_contents.difference(_collection))
            self.Controls = [i for i in self.Collection.Contents] + delenda

            an = []
            for item in self.Controls:
                item.visible = item not in delenda
                an.append((item, 'right'))
                an.append((item, 'bottom'))

            self.attachNone = an
            fudge = 16

            if kwargs.get('horizontal', False):
                if len(self.Controls):
                    fudge = (self.Controls[0].width or 1) * (len(self.Controls) + 1)
                    try:
                        self.width = fudge
                    except AttributeError:
                        pass  # I think this excepts if the previous collection was empty and we're resetting it
            else:
                if len(self.Controls):
                    fudge = self.Controls[0].height * (len(self.Controls) + 1)
                    try:
                        self.height = fudge
                    except AttributeError:
                        pass  # I think this excepts if the previous collection was empty and we're resetting it

            self.layout()
            self.manage = True

        finally:
            cmds.waitCursor(st=0)

    def widget_created(self, *args, **kwargs):
        self.NewWidget(item=args[0])


class VerticalList(forms.VerticalForm, FormList):
    """
    A vertical list of items with an automatic scrollbar
    """

    def __init__(self, key, *args, **kwargs):
        self.Key = key
        with LayoutContext(self):
            self.ScrollLayout = layouts.ScrollLayout("_scroll", width=kwargs.get('width', 1024))
            self.Widget = self.ScrollLayout.Widget + "|temp"
            self.ScrollLayout.__enter__()
            self.__init_bound_collection__(kwargs)
            if 'synchronous' in kwargs:
                kwargs.pop('synchronous')
            super(VerticalList, self).__init__(key, *args, **kwargs)

            self.__enter__()
            self.__exit__(None, None, None)
            self.ScrollLayout.__exit__(None, None, None)

        # # the enter/exits make sure that you can place a listForm as a single control without it
        # # trying to gobble up subsequent objects
        self.width = self.ScrollLayout.width - 24


class HorizontalList(forms.HorizontalForm, FormList):
    """
    A horizontal list of Items with an automatic scrollbar
    """

    def __init__(self, key, *args, **kwargs):
        self.Key = key
        with LayoutContext(self):
            self.ScrollLayout = layouts.ScrollLayout("_scroll")
            self.Widget = self.ScrollLayout.Widget + "|temp"
            self.ScrollLayout.__enter__()
            self.__init_bound_collection__(kwargs)
            super(HorizontalList, self).__init__(key, *args, **kwargs)
            self.__enter__()
            self.__exit__(None, None, None)
        self.height = self.ScrollLayout.height - 24

    def redraw(self, *args, **kwargs):
        kwargs.update({'horizontal': True})
        super(HorizontalList, self).redraw(*args, **kwargs)


class ColumnList(layouts.ColumnLayout, FormList):
    def __init__(self, key, *args, **kwargs):
        self.Key = key
        with LayoutContext(self):
            self.ScrollLayout = layouts.ScrollLayout("_scroll")
            self.Widget = self.ScrollLayout.Widget + "|temp"
            self.ScrollLayout.__enter__()
            self.__init_bound_collection__(kwargs)
            super(ColumnList, self).__init__(key, *args, **kwargs)
            self.__enter__()
            self.__exit__(None, None, None)
        self.width = self.ScrollLayout.width - 24


class WrapList(layouts.FlowLayout, FormList):
    """
    A flowLayout based list of items with optional wrapping. This will clip if
    the width exceeds the layout width unles 'wrap' is set to true

    @note no scrollbars, so no need for LayoutContext
    """

    def __init__(self, key, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(WrapList, self).__init__(key, *args, **kwargs)
        self.__enter__()
        self.__exit__(None, None, None)


class Templated(object):
    def __init__(self, datum, widget, **events):
        self.Datum = datum
        self.Widget = widget
        self.Events = events

    def get_event(self, key):
        '''
        Return the named event, if present
        '''
        return self.Events.get(key, None)


class ItemTemplate(object):
    """
    Base class for item template classes.

    The job of an itemTemplate is to provide a GUI widget (which can be a single
    control or a layout with other controls) that represents the underying data
    item in the bound data collection.

    """

    def __init__(self, parent):
        self.Parent = parent

    def widget(self, item):
        """
        returns the topmost mGui item of a templated list item, along with any events defined in the widget
        """
        cmds.setParent(self.Parent.Widget)
        with forms.HorizontalForm(None) as root:
            r = controls.Button(None, label=str(item))
        return Templated(item, root, command=r.command)

    def __call__(self, item):
        return self.widget(item)

