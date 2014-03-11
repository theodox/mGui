import maya.cmds as cmds
from .events import MayaEvent
from .bindings import BindableObject
from .styles import CSS, Styled

class CtlProperty (object):
    '''
    Property descriptor.  When applied to a Control-derived class, invokes the correct Maya command under the hood to get or set values
    '''
    
    def __init__(self, flag, cmd, writeable = True):
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
        _READ_ONLY = kwargs.get('_READ_ONLY',[])
        _ATTRIBS = kwargs.get('_ATTRIBS',[])
        _CALLBACKS = kwargs.get('_CALLBACKS',[])
        
        if not kwargs.get('CMD'):
            CMD = parents[0].CMD
            
        for item in _READ_ONLY:
            kwargs[item] = CtlProperty(item, CMD, writeable = False)           
        for item in _ATTRIBS:
            kwargs[item] = CtlProperty(item, CMD)
        for item in _CALLBACKS:
            kwargs[item] = CallbackProperty(item)

        return super(ControlMeta, cls).__new__(cls, name, parents, kwargs)

class Control(Styled, BindableObject):
    '''
    Base class for all mGui controls.  Provides the necessary frameworks for
    CtlProperty and CallbackProperty access to the underlying widget.
    
    Control inherits from BindableObject, so it supports binding operators.  All control will have the _
    
    Contropl inherits from Styled, so it supports styling.
    
    '''
    CMD = cmds.control
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'dragCallback', 'dropCallback', 'enable', 'enableBackground', 'exists', 'fullPathName', 'height',  'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']
    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus']
    __metaclass__ = ControlMeta
    
    
    def __init__(self, key, *args, **kwargs):
        
        _style = dict( (k,v) for k,v in self.Style.items() if k in self._ATTRIBS or k in Control._ATTRIBS)    
        _style.update(kwargs)

        self.Key = key
        self.Widget = self.CMD(*args, **_style)
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
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'dragCallback', 'dropCallback', 'enable', 'enableBackground', 'exists', 'fullPathName', 'height',  'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']
    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus', 'childArray', 'numberOfChildren']
    ACTIVE_LAYOUT = None
    
    def __init__(self, key,  *args, **kwargs):
        self.Controls = []
        super (Layout, self).__init__(key, *args, **kwargs)
        
    def __enter__( self ):
        self.__cache_layout = Layout.ACTIVE_LAYOUT
        Layout.ACTIVE_LAYOUT = self
        return self

    def __exit__( self, typ, value, traceback ):
        self.layout()
        Layout.ACTIVE_LAYOUT = self.__cache_layout
        self.__cache_layout = None
        cmds.setParent( ".." ) 

    def layout(self):
        return len(self.Controls)
        
    def add(self, control):
        self.Controls.append(control)
        if control.Key in self.__dict__:
            raise RuntimeError, 'Children of a layout must have unique IDs'
        self.__dict__[control.Key] = control
        
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
        if control.Key and cls.ACTIVE_LAYOUT:
            cls.ACTIVE_LAYOUT.add(control)
    