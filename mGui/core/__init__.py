import maya.cmds as cmds

import inspect
from collections import OrderedDict
from mGui.bindings import BindableObject, BindingContext
from mGui.properties import CtlProperty, CallbackProperty
from mGui.scriptJobs import ScriptJobCallbackProperty
from mGui.styles import Styled
from weakref import ref

"""
# MGui.Core
A system for defininng proxies that make it easier to work with maya GUI controls.

Proxies are created using the ControlMeta metaclass, which maps existing maya
GUI commands so that they look like proper object-oriented properties:

   example = Button('buttontest')
   example.width = 120
   example.backgroundColor = (1,0,0)

creates a 120 pixel wide red button. The properties work both ways, so you can
query them:

   print example.width
   # 120


## Base Classes
This module defines the base classes Control and Layout, which are used by all
wrapper classes. They use the same property-wrapping stategy but Layouts also work as
context managers, allowing them to call SetParent() when needed and also to
maintain links to child control wrappers:

   with mGui.core.layouts.ColumnLayout('main'):
       for n in range (5):
           with mGui.core.Layout.RowLayout('row_%i' % n, nc = 2):
               mGui.core.controls.Text('t_%i', label = 'label)
               mGui.core.controls.CheckBox('b_%i')
        mGui.core.controls.Button('btn', label = 'big button')

would create a columnLayout with 4 rows with a text and a checkbox, followed by a button.

@note:  in actual practice, its easier to import mGui.gui which contains all of
the contents of core.layouts and core.controls

@Note: One minor drawback to using Metaclasses is that Maya's reload mechanism
does not preserve the types created by a metaclass when you call reload(module).
This manifests as a TypeError in code that calls super() -- in this case,
typically in __init__ methods.  This problem is ONLY related to reload - if you
restart Maya rather than using reload() it will disappear.
"""

# use this for condtional checks if there are version differences
MAYA_VERSION = cmds.about(version=True).split(' ')[0]

REGISTRY = {}

class ControlMeta(type):
    """
    Metaclass which creates CtlProperty and CallbackProperty objects for Control classes
    """

    def __new__(mcs, name, parents, kwargs):

        maya_cmd = kwargs.get('CMD', None)
        _READ_ONLY = kwargs.get('_READ_ONLY', [])
        _ATTRIBS = kwargs.get('_ATTRIBS', [])
        _CALLBACKS = kwargs.get('_CALLBACKS', [])
        if not kwargs.get('CMD'):
            maya_cmd = parents[0].CMD

        _overridden = ('parent',)
        for item in _READ_ONLY:
            if item not in _overridden:
                kwargs[item] = CtlProperty(item, maya_cmd, writeable=False)
        for item in _ATTRIBS:
            if item not in _overridden:
                kwargs[item] = CtlProperty(item, maya_cmd)
        for item in _CALLBACKS:
            kwargs[item] = CallbackProperty(item)

        kwargs['__bases__'] = parents

        completed_type =  super(ControlMeta, mcs).__new__(mcs, name, parents, kwargs)
        if maya_cmd:
            REGISTRY[maya_cmd.__name__] = completed_type

        return completed_type


class Control(Styled, BindableObject):
    """
    Base class for all mGui controls.  Provides the necessary frameworks for
    CtlProperty and CallbackProperty access to the underlying widget.

    Control inherits from bindings.BindableObject, so it supports binding
    operators.  All controls will have _bind_src and _bind_tgt fields, and
    if a derived control class indicates default(s) they will be used.

    Control inherits from styles.Styled, so it supports styling.

    """
    CMD = cmds.control
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'enable', 'enableBackground', 'exists',
                'fullPathName', 'height', 'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray',
                'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']
    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus']
    __metaclass__ = ControlMeta

    onDeleted = ScriptJobCallbackProperty('onDeleted', 'uiDeleted')

    def __init__(self, key=None, **kwargs):
        # apply Styled, and filter out any CSS tags
        super(Control, self).__init__(kwargs)

        # arbitrary tag data. Use with care to avoid memory leaks
        self.tag = kwargs.pop('tag', None)

        maya_kwargs = self.format_maya_arguments(**kwargs)

        # widget holds the actual maya gui string
        self.widget = self.CMD(key, **maya_kwargs)

        # key is our internal name
        self.key = self.widget.split("|")[-1]

        # Event objects
        self.callbacks = {}

        # a weak reference to our parent, will be added when
        # this widget is added to a control
        self._parent = None

        # add us to the current layout under our own key name
        Layout.add_current(self)
        self.onDeleted += self.forget

    def register_callback(self, callback_name, event):
        """
        when a callback property is first accessed this creates an Event named <callback_name> for the specified
        callback and hooks it to the gui widget's callback function
        """
        kwargs = {'e': True, callback_name: event}
        self.CMD(self.widget, **kwargs)

    def __nonzero__(self):
        return self.exists

    def __repr__(self):
        if self:
            return self.widget
        else:
            return "<deleted UI element %s>" % self.__class__

    def __str__(self):
        return self.widget

    def __iter__(self):
        yield self

    @classmethod
    def wrap(cls, control_name, key=None):

        def _spoof_create(*_, **__):
            return control_name

        try:
            cache_CMD = cls.CMD
            cls.CMD = _spoof_create

            # allow wrapping of abstract types, but make sure derived types are correct
            if cls.__name__ not in ('Control', 'Layout', 'Nested', 'Panel'):
                if not cmds.objectTypeUI(control_name, isType = cache_CMD.__name__):
                    raise RuntimeError( "{} is not an instance of {}".format(control_name, cache_CMD.__name__))
            return cls(key=control_name)

        finally:
            cls.CMD = cache_CMD

    def forget(self, *args, **kwargs):
        self.callbacks.clear()
        self.tag = None

    @classmethod
    def delete(cls, instance):
        cmds.deleteUI(instance.widget)

    @property
    def parent(self):
        """
        the mGui parent of this object.  This will be None if:
            * this object has no parent (eg, a top level window)
            * this object's parent has fallen out of scope
            * this layout context for this object has not yet closed.

        """
        if self._parent is None:
            return None
        return self._parent()


class Nested(Control):
    """
    Base class for all the nested context-manager classes which automatically parent themselves

    Every NestedObject creates an ScriptJobCallbackProperty attached to a uiDeleted scriptJob,
    so it's possible to use standard event mechanisms to react to, eg, a window closing. The
    scriptJob will be started with default arguments the first time you attempt to add a handler
    to it.

    """
    ACTIVE_LAYOUT = None

    def __init__(self, key=None, **kwargs):
        self.controls = []
        self.named_children = OrderedDict()
        self.ignore_exceptions = False
        self.modal = False
        super(Nested, self).__init__(key, **kwargs)

    def __enter__(self):
        self.__cache_layout = Nested.ACTIVE_LAYOUT
        if self.__cache_layout is not None:
            self.modal = self.modal or self.__cache_layout.modal
        Nested.ACTIVE_LAYOUT = self
        return self

    def __exit__(self, typ, value, tb):
        # by default, allow inner exceptions to propagate up
        # you can turn this off in production by
        # setting ignore_exceptions to true
        # if this is suppresed you should expect misleading
        # error messages if child controls error out; parent controls
        # may get fewer controls than they expect, but the real
        # problem is in the suppressed exception
        if typ and not self.ignore_exceptions:
            return False

        # look into the local namespace for Control-derived
        # objects with named vars. If they are children of the context manager
        # that is closing, add them with variable name as a key
        # this supports a more natural, keyless idiom (see 'add')

        owning_scope = inspect.currentframe().f_back
        if owning_scope.f_locals.get('mGui_expand_stack'):
            owning_scope = owning_scope.f_back
        for key, value in owning_scope.f_locals.items():
            if value in self:
                self.add(value, key)

        # restore the layout level
        Nested.ACTIVE_LAYOUT = self.__cache_layout
        self.__cache_layout = None
        self.layout()

        # restore gui parenting
        cmds.setParent(Nested.ACTIVE_LAYOUT)

    def layout(self):
        """
        this is called at the end of a context, it can be used to (for example) perform attachments
        in a formLayout.  Override in derived classes for different behaviors.
        """
        return len(self.controls)

    def add(self, control, key=None):
        """
        Add the supplied control (an mGui object) to the both the Controls list  and the _named_children dictionary
        in this item.  If the control has a unique key.

        named_children allows for dot notation access:

            with gui.ColumnLayout('items') as items:
                first = gui.Button(label = 'a button')
                second = gui.Button( label = 'another button')

            print items.first.label
            # a button

        named_children will contain a reference to the key name (the optional first argument) of any mGui control. It
        will also close over any local variable names in a layout context.  Thus

            with Window() as outer:
                with ColumnLayout() as column:
                    Button('first')
                    second = Button()

        produces  both

            outer.column.first

        and

            outer.column.second

        the first one via explicit naming and the second via closure.

        Controls contains all of the *physical* widgets under this object (layouts, controls, etc).
        Non-physical entities -- such as a RadioButtonCollection -- are available with dot notation but *not*
        in the Controls field. This allows the layout() functions in various layouts to rely on the presence of
        controls that can be manipulated.
        """

        # @ this is a change in behavior from mGui 1
        # we now overwrite existing children instead of excepting
        # we also DON'T explicitly check to ensure that <control> is a kind of this widget
        control_key = key or control.key
        self.named_children[control_key] = control
        if control not in self.controls:
            self.controls.append(control)

        control._parent = ref(self)

    def replace(self, key, control):
        """
        replace the control at <key> with the supplied control, and redo the layout for this item.

        @note this will only work if the existing item has a key
        """
        original = self.named_children.get(key)
        if original:
            self.controls.remove(original)
            Control.delete(original)
        self.add(control, key)
        self.layout()

    def remove(self, control):
        """
        remove <control> from my children
        """
        if control not in self.controls:
            raise KeyError('{0} is not a child of {1}'.format(control, self))
        self.controls.remove(control)
        control.delete(control)
        for key, ctrl in self.named_children.items():
            if ctrl == control:
                self.named_children.pop(key)

    def clear(self):
        delenda = (i for i in self.controls)
        for d in delenda:
            self.remove(d)
        self.named_children.clear()

    def __setattr__(self, key, value):
        if isinstance(value, Control) and not key.startswith("_"):
            self.add(value, key=key)
        else:
            super(Nested, self).__setattr__(key, value)

    def __getattr__(self, item):
        if item in self.named_children:
            return self.named_children[item]
        super(Nested, self).__getattribute__(item)

    def __iter__(self):
        for sub in self.controls:
            yield sub
        yield self

    def __contains__(self, item):
        return item in self.controls

    def recurse(self):
        for item in self.controls:
            if hasattr(item, 'recurse'):
                for grandchild in item.recurse():
                    yield grandchild
            yield item

    # note: both of these explicitly use Nested instead of cls
    # so that there is only one global layout stack...

    @classmethod
    def add_current(cls, control):
        active = Nested.current()
        if active:
            Nested.ACTIVE_LAYOUT.add(control)

    @classmethod
    def current(cls):
        """
        return the active layout if it exists
        """
        if Nested.ACTIVE_LAYOUT:
            return Nested.ACTIVE_LAYOUT

    def forget(self, *args, **kwargs):
        super(Nested, self).forget()
        if self.controls:
            self.controls = []
        if self.named_children:
            self.named_children = {}
        if Nested.ACTIVE_LAYOUT == self:
            Nested.ACTIVE_LAYOUT = None

    def as_parent(self):
        try:
            cmds.setParent(self)
        except RuntimeError as e:
            cmds.setParent(self, menu=True)
        return self



# IMPORTANT NOTE
# this intentionally duplicates redundant property names from Control.
# That forces the metaclass to F-define the CtlProperties using cmds.layout
# instead of cmds.control. In Maya 2014, using cmds.control to query a layout fails,
# even for flags they have in common

class Layout(Nested):
    CMD = cmds.layout
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'dragCallback', 'dropCallback', 'enable',
                'enableBackground', 'exists', 'fullPathName', 'height', 'manage', 'noBackground', 'numberOfPopupMenus',
                'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand',
                'width']
    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus', 'childArray', 'numberOfChildren']



class Window(Nested):
    """

    Window inherits from bindings.BindableObject, so it supports binding
    operators.  All controls will have _bind_src and _bind_tgt fields, and
    if a derived control class indicates default(s) they will be used.

    Window inherits from styles.Styled, so it supports styling.

    @note:
    in Maya 2011 (only, AFAIK) a sizeable = False parameter mis-behaves when
    the window contains a TabLayout which in turn contains a FormLayout. If
    you have to have to use a TabLayout in 2011, don't use any derivative
    of forms, or set 'sizeable' to TRUE.  Bug is not present in 2014 +, not sure
    about 2012 or 2013
    """
    ACTIVE_WINDOWS = []

    CMD = cmds.window
    _ATTRIBS = ["backgroundColor", "defineTemplate", "docTag", "exists", "height", "iconify", "iconName", "leftEdge",
                "menuBarVisible", "menuIndex", "mainMenuBar", "minimizeButton", "maximizeButton", "resizeToFitChildren",
                "sizeable", "title", "titleBar", "titleBarMenu", "topEdge", "toolbox", "topLeftCorner", "useTemplate",
                "visible", "width", "widthHeight"]
    _CALLBACKS = ["minimizeCommand", "restoreCommand"]
    _READ_ONLY = ["numberOfMenus", "menuArray", "menuBar", "retain"]

    def __init__(self, key=None, **kwargs):
        super(Window, self).__init__(key, **kwargs)
        Window.ACTIVE_WINDOWS.append(self)

    def forget(self, *args, **kwargs):
        super(Window, self).forget()
        if self in Window.ACTIVE_WINDOWS:
            Window.ACTIVE_WINDOWS.remove(self)

    def show(self):
        cmds.showWindow(self.widget)

    def hide(self):
        self.visible = False

    @classmethod
    def current(cls):
        if Window.ACTIVE_WINDOWS:
            return Window.ACTIVE_WINDOWS[-1]
        return None


class BindingWindow(Window):
    """
    A Window with a built in BindingContext
    """

    def __init__(self, key=None, **kwargs):
        super(BindingWindow, self).__init__(key, **kwargs)
        self.bindingContext = BindingContext()

    def __enter__(self):
        self.bindingContext.__enter__()
        return super(BindingWindow, self).__enter__()

    def __exit__(self, typ, value, traceback):
        self.bindingContext.__exit__(None, None, None)
        mGui_expand_stack = True
        super(BindingWindow, self).__exit__(typ, value, traceback)

    def update_bindings(self):
        self.bindingContext.update(True)

    def forget(self, *args, **kwargs):
        super(BindingWindow, self).forget()
        self.bindingContext = None

