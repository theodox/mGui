import maya.cmds as cmds
from .events import MayaEvent


class CtlProperty (object):
    '''
    Property descriptor.  When applied to a Control-derived class, invokes the correct Maya command under the hood to get or set values
    '''

    def __init__(self, flag, cmd, writeable=True):
        assert callable(cmd), "cmd flag must be a maya command for editing gui objects"
        self.Flag = flag or self.FLAG
        self.Writeable = writeable
        self.Command = cmd

    def __get__(self, obj, objtype):
        return self.Command(obj.Widget, **{'q':True, self.Flag:True})

    def __set__(self, obj, value):
        if not self.Writeable:
            raise AttributeError('attribute .%s is not writable' % self.Flag)
        return self.Command(obj.Widget, **{'e':True, self.Flag:value})


class CallbackProperty(object):
    '''
    Property descriptor for callbacks.  When accessed, returns the appropriate Event object from a Control-derived class's Callback dictionary. This property cannot be 'set' or 'unset' - instead use the += or -= methods on the underlying Event object:
    
    button.click += doSomething
    button.click -= doSomething
    
    NOT
    
    button.click = dosomething
    '''
    def __init__(self, key):
        self.Key = key

    def __get__(self, obj, objtype):
        cb = obj.Callbacks.get(self.Key, None)
        if not cb:
            obj.Callbacks[self.Key] = MayaEvent()
            obj.register_callback(self.Key, obj.Callbacks[self.Key])
        return obj.Callbacks[self.Key]



class ControlMeta(type):
    '''
    Metaclass which creates CtlProperty and CallbackProperty objects for Control classes
    '''

    def __new__(cls, name, parents, kwargs):


        CMD = kwargs.get('CMD', None)
        _READ_ONLY = kwargs.get('_READ_ONLY', [])
        _ATTRIBS = kwargs.get('_ATTRIBS', [])
        _CALLBACKS = kwargs.get('_CALLBACKS', [])

        if not kwargs.get('CMD'):
            CMD = parents[0].CMD

        for item in _READ_ONLY:
            kwargs[item] = CtlProperty(item, CMD, writeable=False)
        for item in _ATTRIBS:
            kwargs[item] = CtlProperty(item, CMD)
        for item in _CALLBACKS:
            kwargs[item] = CallbackProperty(item)

        return super(ControlMeta, cls).__new__(cls, name, parents, kwargs)

class Control(object):
    '''
    Base class for all mGui controls.  Provides the necessary frameworks for CtlProperty and CallbackProperty access to the underlying widget
    '''
    CMD = cmds.control
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'dragCallback', 'dropCallback', 'enable', 'enableBackground', 'exists', 'fullPathName', 'height', 'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']
    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus']
    __metaclass__ = ControlMeta


    def __init__(self, name, *args, **kwargs):

        self.Name = name

        self.Style = kwargs.get('style', self.__class__.__name__)
        if 'style' in kwargs: del kwargs['style']


        self.Widget = self.CMD(*args, **kwargs)
        '''
        Widget is the gui element in the scene
        '''
        self.Callbacks = {}
        '''
        A dictionary of Event objects
        '''

        Layout.add_current(self)

    def register_callback(self, callbackName, event):
        '''
        when a callback property is first accessed this creates an Event for the specified callback and hooks it to the gui widget's callback function
        '''
        kwargs = {'e':True, callbackName:event}
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




# IMPORTANT NOTE
# this intentionally duplicates redundant property names from Control. That forces the metaclass to re-define the CtlProperties using cmds.layout
# instead of cmds.control. In Maya 2014, using cmds.control to query a layout fails, evem for flags they have in common

class Layout(Control):

    CMD = cmds.layout
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'dragCallback', 'dropCallback', 'enable', 'enableBackground', 'exists', 'fullPathName', 'height', 'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']
    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus', 'childArray', 'numberOfChildren']
    ACTIVE_LAYOUT = None

    def __init__(self, name, *args, **kwargs):
        super (Layout, self).__init__(self, name, *args, **kwargs)
        self.Controls = []
        self.__cache_layout = self.ACTIVE_LAYOUT
        Layout.ACTIVE_LAYOUT = self

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        cmds.setParent("..")  # @UndefinedVariable
        self.ACTIVE_LAYOUT = self.__cache_layout
        self.layout()

    def layout(self):
        pass

    def add(self, control):
        if control.Name in self.__dict__:
            raise RuntimeError, 'Children of a layout must have unique IDs'
        self.Controls.append(control)
        self.__dict__[control.Name] = control

    def remove(self, control):
        self.Controls.remove(control)
        k = [k for k , v in self.__dict__.items() if v == control]
        if k: del[self.__dict__ [k[0]]]

    def __iter__(self):
        for item in self.Controls:
            for sub in item:
                yield sub
        yield self

    @classmethod
    def add_current(cls, control):
        if control.Name and cls.ACTIVE_LAYOUT:
            cls.ACTIVE_LAYOUT.add(control)
