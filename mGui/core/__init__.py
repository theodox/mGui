import maya.cmds as cmds

from mGui.bindings import BindableObject, BindingContext
from mGui.styles import Styled
from mGui.properties import CtlProperty, CallbackProperty
from mGui.scriptJobs import ScriptJobCallbackProperty


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

        for item in _READ_ONLY:
            kwargs[item] = CtlProperty(item, maya_cmd, writeable=False)
        for item in _ATTRIBS:
            kwargs[item] = CtlProperty(item, maya_cmd)
        for item in _CALLBACKS:
            kwargs[item] = CallbackProperty(item)

        return super(ControlMeta, mcs).__new__(mcs, name, parents, kwargs)


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

    def __init__(self, key, *args, **kwargs):
        # arbitrary tag data. Use with care to avoid memory leaks
        self.Tag = kwargs.get('tag', None)
        if 'tag' in kwargs:
            del kwargs['tag']

        # this applies any keywords in the current style that are part of the Maya gui flags
        # other flags (like float and margin) are ignored
        _style = dict((k, v) for k, v in self.Style.items() if k in self._ATTRIBS or k in Control._ATTRIBS)
        _style.update(kwargs)

        # if the style dict contains an 'html' keyword, treate it as a
        # callable which modifies the incoming 'label'
        if 'css' in _style:
            css = _style['css']
            if 'html' in css and 'label' in _style:
                _style['label'] = css['html'](_style['label'])
            del _style['css']

        if not args:
            args = (key,)

        self.Widget = self.CMD(*args, **_style)
        self.Key = key or "__" + self.Widget.split("|")[-1]

        """
        Widget is the gui element in the scene
        """
        self.Callbacks = {}
        """
        A dictionary of Event objects
        """
        Layout.add_current(self)

    def register_callback(self, callbackName, event):
        """
        when a callback property is first accessed this creates an Event for the specified callback and hooks it to the
        gui widget's callback function
        """
        kwargs = {'e': True, callbackName: event}
        self.CMD(self.Widget, **kwargs)

    def __nonzero__(self):
        return self.exists

    def __repr__(self):
        if self:
            return self.Widget
        else:
            return "<deleted UI element %s>" % self.__class__

    def __str__(self):
        return self.Widget

    def __iter__(self):
        yield self

    @classmethod
    def wrap(cls, control_name, key=None):

        def _spoof_create(*args, **kwargs):
            return control_name

        try:
            cache_CMD = cls.CMD
            cls.CMD = _spoof_create
            key = key or control_name
            return cls(key, control_name)
        finally:
            cls.CMD = cache_CMD


    @classmethod
    def from_existing(cls, key, widget):
        """
        Create an instance of <cls> from an existing widgets
        """

        def fake_init(self, *args, **kwargs):
            return widget

        _cmd = cls.CMD
        try:
            cls.CMD = fake_init
            return cls(key)
        finally:
            cls.CMD = _cmd


class Nested(Control):
    """
    Base class for all the nested context-manager classes which automatically parent themselves

    Every NestedObject creates an ScriptJobCallbackProperty attached to a uiDeleted scriptJob,
    so it's possible to use standard event mechanisms to react to, eg, a window closing. The
    scriptJob will be started with default arguments the first time you attempt to add a handler
    to it.

    """
    ACTIVE_LAYOUT = None

    Deleted = ScriptJobCallbackProperty('Deleted', 'uiDeleted')

    def __init__(self, key, *args, **kwargs):
        self.Controls = []
        super(Nested, self).__init__(key, *args, **kwargs)

    def __enter__(self):
        self.__cache_layout = Nested.ACTIVE_LAYOUT
        Nested.ACTIVE_LAYOUT = self
        return self

    def __exit__(self, typ, value, tb):
        if typ:
            raise
        self.layout()
        Nested.ACTIVE_LAYOUT = self.__cache_layout
        self.__cache_layout = None
        abs_parent, sep, _ = self.Widget.rpartition("|")
        if abs_parent == '': abs_parent = _
        cmds.setParent(abs_parent)


    def layout(self):
        """
        this is called at the end of a context, it can be used to (for example) perform attachments
        in a formLayout.  Override in derived classes for different behaviors.
        """
        return len(self.Controls)

    def add(self, control):
        '''
        Add the supplied control (an mGui object) to the Controls list in this item.  If the control has a unique key,
        add the key to this object's __dict__.  This allows dot notation access:

            with gui.ColumnLayout('items') as items:
                gui.Button('first', label = 'a button')
                gui.Button('second', label = 'another button')

            print items.first.label
            # a button

        The Controls field contains all of the *phyiscal* widgets under this object (layouts, controls, etc).
        Non-physical entities -- such as a RadioButtonCollection -- are available with dot notation but *not*
        in the Controls field. This allows the layout() functions in various layouts to rely on the presence of
        controls that can be manipulated.
        '''

        path_difference = control.Widget[len(self.Widget):].count('|') - 1
        if not path_difference and hasattr(control, 'visible'):
            self.Controls.append(control)

        if control.Key and not control.Key[0] == "_":
            if control.Key in self.__dict__:
                raise RuntimeError('Children of a layout must have unique IDs')
            self.__dict__[control.Key] = control

    def replace(self, key, control):
        """
        replace the control at <key> with the supplied control, and redo the layout for this item.

        @note this will only work if the existing item has a key
        """
        original = self.__dict__[key]
        original_idx = self.Controls.index(original)
        self.Controls.insert(original_idx, control)
        self.__dict__[key] = control
        self.Controls.remove(original)
        cmds.deleteUI(original)
        self.layout()

    def remove(self, control):
        self.Controls.remove(control)
        k = [k for k, v in self.__dict__.items() if v == control]
        if k:
            del self.__dict__[k[0]]

    def __iter__(self):
        for item in self.Controls:
            for sub in item:
                yield sub
        yield self

    @classmethod
    def add_current(cls, control):
        if Nested.ACTIVE_LAYOUT:
            Nested.ACTIVE_LAYOUT.add(control)


# IMPORTANT NOTE
# this intentionally duplicates redundant property names from Control.
# That forces the metaclass to re-define the CtlProperties using cmds.layout
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

    """
    ACTIVE_WINDOWS = []

    CMD = cmds.window
    _ATTRIBS = ["backgroundColor", "defineTemplate", "docTag", "exists", "height", "iconify", "iconName", "leftEdge",
                "menuBarVisible", "menuIndex", "mainMenuBar", "minimizeButton", "maximizeButton", "resizeToFitChildren",
                "sizeable", "title", "titleBar", "titleBarMenu", "topEdge", "toolbox", "topLeftCorner", "useTemplate",
                "visible", "width", "widthHeight"]
    _CALLBACKS = ["minimizeCommand", "restoreCommand"]
    _READ_ONLY = ["numberOfMenus", "menuArray", "menuBar", "retain"]

    def __init__(self, key, *args, **kwargs):
        super(Window, self).__init__(key, *args, **kwargs)
        self.ACTIVE_WINDOWS.append(self)
        self.Deleted += self.forget

    @classmethod
    def forget(cls, *args, **kwargs):
        cls.ACTIVE_WINDOWS.remove(kwargs['sender'])

    def show(self):
        cmds.showWindow(self.Widget)

    def hide(self):
        self.visible = False


class BindingWindow(Window):
    """
    A Window with a built in BindingContext
    """

    def __init__(self, key, *args, **kwargs):
        super(BindingWindow, self).__init__(key, *args, **kwargs)
        self.bindingContext = BindingContext()

    def __enter__(self):
        self.bindingContext.__enter__()
        return super(BindingWindow, self).__enter__()

    def __exit__(self, typ, value, traceback):
        super(BindingWindow, self).__exit__(typ, value, traceback)
        self.bindingContext.__exit__(None, None, None)

    def update_bindings(self):
        self.bindingContext.update(True)

