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
import time


class FormList(object):
    """
    Adds a BoundCollection to a Layout class. Will call the owning class's
    layout() method when the collection changes, and will prune the layouts
    control sets as items are added to or removed from the bound collection.
    """
    SCROLL_WIDTH = 33

    def __init_bound_collection__(self, kwargs):
        """
        initialize the mixin. Call after the layout constructor, eg:

            super(MyBoundFormClass, self).__init__(key, *args, **kwargs)
            self.__init_bound_collection__()

        """
        self.template = kwargs.pop('itemTemplate', ItemTemplate)(self)
        self.sync = kwargs.pop('synchronous', True)
        self.redraw_options = {}

        event_class = events.Event
        collection_class = observable.ImmediateBoundCollection

        if not self.sync:
            event_class = events.MayaEvent
            collection_class = observable.BoundCollection

        self.collection = collection_class()
        self.onWidgetCreated = event_class(type='widget created')
        self.onUpdated = event_class(type='updated')

        self.collection.CollectionChanged += self.redraw  # automatically forward collection changes

    def redraw(self, *args, **kwargs):
        """
        NOTE: depends on the LIST_CLASS being set in the actual class!
        """
        try:
            cmds.waitCursor(st=1)

            self.named_children = {}
            self.controls = []

            seed = int(time.time())

            cmds.setParent(self)
            with self:
                with layouts.ScrollLayout( childResizable=True) as inner_scroll:
                    with self.LIST_CLASS( **self.redraw_options) as inner_list:
                        for item in self.collection:
                            w = self.template.widget(item)
                            self.widget_added(w)

            cmds.setParent(self)
            cmds.setParent("..")

            # controls only includes 'inner_scroll' for layout
            self.named_children['inner_scroll'] = inner_scroll
            self.named_children['inner_list'] = inner_list
            self.controls = [inner_scroll]


        finally:
            self.layout()
            cmds.waitCursor(st=0)

    def widget_added(self, templated_item):
        """
        by default, raise the NewWidget event
        but can be overridden to handle here instead
        """
        self.onWidgetCreated(item=templated_item)

    def gui_contents(self):
        for item in self.inner_list.controls:
            yield item

    def contents(self):
        for item in self.collection:
            yield item


class VerticalList(forms.FillForm, FormList):
    """
    A vertical list of items with an automatic scrollbar
    """

    LIST_CLASS = forms.VerticalForm

    def __init__(self, key=None, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(VerticalList, self).__init__(key, *args, **kwargs)
        self.redraw()

    def redraw(self, *args, **kwargs):
        super(VerticalList, self).redraw()
        self.inner_list.width = max(self.width - 33, 33)


class HorizontalList(forms.FillForm, FormList):
    """
    A horizontal list of Items with an automatic scrollbar
    """

    LIST_CLASS = forms.HorizontalForm

    def __init__(self, key=None, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(HorizontalList, self).__init__(key, *args, **kwargs)
        self.redraw()

    def redraw(self, *args, **kwargs):
        super(HorizontalList, self).redraw()
        self.inner_list.height = max(self.width - 33, 33)


class ColumnList(forms.FillForm, FormList):
    LIST_CLASS = layouts.ColumnLayout

    def __init__(self, key=None, *args, **kwargs):
        self.__init_bound_collection__(kwargs)
        super(ColumnList, self).__init__(key, *args, **kwargs)
        self.redraw()

    def redraw(self, *args, **kwargs):
        super(ColumnList, self).redraw()
        self.inner_list.width = max(self.width - 33, 33)


class WrapList(forms.FillForm, FormList):
    """
    A flowLayout based list of items with optional wrapping. This will clip if
    the width exceeds the layout width unles 'wrap' is set to true
    """
    LIST_CLASS = layouts.FlowLayout

    def __init__(self, key=None, *args, **kwargs):
        self.wrap = kwargs.pop('wrap', False)
        self.__init_bound_collection__(kwargs)
        self.redraw_options['wrap'] = self.wrap

        super(WrapList, self).__init__(key, *args, **kwargs)
        self.redraw()

    def redraw(self, *args, **kwargs):
        super(WrapList, self).redraw()
        self.inner_list.height = max(self.height - 33, 33)
        self.inner_list.width = max(self.width - 33, 33)


class Templated(object):
    """
    contains the original data item, the widget represents it, and any named event objects it exposes
    """

    def __init__(self, datum, widget, **named_events):
        self.datum = datum
        self.widget = widget
        self.events = named_events

    def get_event(self, key):
        """
        Return the named event, if present
        """
        return self.events.get(key, None)


class ItemTemplate(object):
    """
    Base class for item template classes.

    The job of an itemTemplate is to provide a GUI widget (which can be a single
    control or a layout with other controls) that represents the underying data    item in the bound data collection.

    """

    def __init__(self, owner):
        self.owner = owner

    def widget(self, item):
        """
        returns the topmost mGui item of a templated list item, along with any events defined in the widget
        """

        with forms.HorizontalForm() as root:
            r = controls.Button(label=str(item))
        return Templated(item, root, command=r.command)

    def __call__(self, item):
        return self.widget(item)
