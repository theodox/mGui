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


class FormList(object):
    """
    Adds a BoundCollection to a Layout class. Will call the owning class's
    layout() method when the collection changes, and will prune the layouts
    control sets as items are added to or removed from the bound collection.
    """
    SCROLL_WIDTH = 25

    def __init_bound_collection__(self, kwargs):
        """
        initialize the mixin. Call after the layout constructor, eg:

            super(MyBoundFormClass, self).__init__(key, *args, **kwargs)
            self.__init_bound_collection__()

        """
        self._scroll = 'not initialized'
        self._list = 'not initialized'

        self.Template = self._extract_kwarg('itemTemplate', kwargs, ItemTemplate)(self)
        self.Sync = self._extract_kwarg('synchronous', kwargs, True)
        self.Redraw_Opts = {}

        event_class = events.Event
        collection_class = observable.ImmediateBoundCollection

        if not self.Sync:
            event_class = events.MayaEvent
            collection_class = observable.BoundCollection

        self.Collection = collection_class()
        self.NewWidget = event_class(type='widget created')
        self.Updated = event_class(type='updated')

        self.Collection.CollectionChanged += self.redraw  # automatically forward collection changes

    def _extract_kwarg(self, key, kwarg, default=None):
        result = kwarg.get(key, default)
        if key in kwarg:
            del kwarg[key]
        return result

    def redraw(self, *args, **kwargs):
        '''
        NOTE: depends on the LIST_CLASS being set in the actual class!
        '''

        if self._scroll != 'not initialized':
            cmds.deleteUI(self._scroll)
            self._scroll = 'not initialized'
            self._list = 'not initialized'

        cmds.setParent(self)
        with layouts.ScrollLayout('_scroll', childResizable=True) as self._scroll:
            with self.LIST_CLASS('_list', **self.Redraw_Opts) as self._list:
                for item in self.Collection:
                    w = self.Template.widget(item)
                    self.widget_added(w)
        cmds.setParent(self.parent)

        self._scroll.Deleted._handlers = set()
        self._list.Deleted._handlers = set()

        self._scroll.Deleted.kill()
        self._list.Deleted.kill()

        self.Controls = [self._scroll]
        self.layout()


    def widget_added(self, templated_item):
        '''
        by default, raise the NewWidget event
        but can be overridden to handle here instead
        '''
        self.NewWidget(item=templated_item)


class VerticalList(forms.FillForm, FormList):
    """
    A vertical list of items with an automatic scrollbar
    """

    LIST_CLASS = forms.VerticalForm

    def __init__(self, key, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(VerticalList, self).__init__(key, *args, **kwargs)
        self._scroll = 'not initialized'
        self._list = 'not initialized'
        self.redraw()


    def redraw(self, *args, **kwargs):
        super(VerticalList, self).redraw()
        self._list.width = max(self.width - 25, 25)


class HorizontalList(forms.FillForm, FormList):
    """
    A horizontal list of Items with an automatic scrollbar
    """

    LIST_CLASS = forms.HorizontalForm

    def __init__(self, key, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(HorizontalList, self).__init__(key, *args, **kwargs)
        self.redraw()


    def redraw(self, *args, **kwargs):
        super(HorizontalList, self).redraw()
        self._list.height = max(self.width - 25, 25)


class ColumnList(forms.FillForm, FormList):
    LIST_CLASS = layouts.ColumnLayout

    def __init__(self, key, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(ColumnList, self).__init__(key, *args, **kwargs)
        self.redraw()


    def redraw(self, *args, **kwargs):
        super(ColumnList, self).redraw()
        self._list.width = max(self.width - 25, 25)


class WrapList(forms.FillForm, FormList):
    """
    A flowLayout based list of items with optional wrapping. This will clip if
    the width exceeds the layout width unles 'wrap' is set to true
    """
    LIST_CLASS = layouts.FlowLayout

    def __init__(self, key, *args, **kwargs):
        self.wrap = self._extract_kwarg('wrap', kwargs, False)
        self.__init_bound_collection__(kwargs)
        self.Redraw_Opts['wrap'] = self.wrap

        super(WrapList, self).__init__(key, *args, **kwargs)
        self.redraw()


    def redraw(self, *args, **kwargs):
        super(WrapList, self).redraw()
        self._list.height = max(self.height - 25, 25)
        self._list.width = max(self.width - 25, 25)


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

    def __init__(self, owner):
        self.owner = owner

    def widget(self, item):
        """
        returns the topmost mGui item of a templated list item, along with any events defined in the widget
        """

        with forms.HorizontalForm(None) as root:
            r = controls.Button(None, label=str(item))
        return Templated(item, root, command=r.command)

    def __call__(self, item):
        return self.widget(item)

