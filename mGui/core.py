import maya.cmds as cmds
from .bindings import BindableObject
from .styles import Styled
from .properties import CtlProperty, CallbackProperty

'''
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

   with mGui.layouts.ColumnLayout('main'):
       for n in range (5):
           with mGui.Layout.RowLayout('row_%i' % n, nc = 2):
               mGui.controls.Text('t_%i', label = 'label)
               mGui.controls.CheckBox('b_%i')
        mGui.controls.Button('btn', label = 'big button')
        
would create a columnLayout with 4 rows with a text and a checkbox, followed by a button.

@Note: One minor drawback to using Metaclasses is that Maya's reload mechanism
does not preserve the types created by a metaclass when you call reload(module).
This manifests as a TypeError in code that calls super() -- in this case,
typically in __init__ methods.  This problem is ONLY related to reload - if you
restart Maya rather than using reload() it will disappear.
'''


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
    
    Control inherits from bindings.BindableObject, so it supports binding
    operators.  All controls will have _bind_src and _bind_tgt fields, and 
    if a derived control class indicates default(s) they will be used.
    
    Control inherits from styles.Styled, so it supports styling.
    
    '''
    CMD = cmds.control
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag',  'enable', 'enableBackground', 'exists', 'fullPathName', 'height',  'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']
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
        _style = dict( (k,v) for k,v in self.Style.items() if k in self._ATTRIBS or k in Control._ATTRIBS)    
        _style.update(kwargs)
        


        self.Widget = self.CMD(*args, **_style)
        self.Key = key or "__" + self.Widget.split("|")[-1]

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
        
    




class Nested(Control):
    '''
    Base class for all the nested context-manager classes which automatically parent themselves
    '''
    ACTIVE_LAYOUT = None
   
   
    def __init__(self, key,  *args, **kwargs):
        self.Controls = []
        super (Nested, self).__init__(key, *args, **kwargs)
   
    def __enter__( self ):
        self.__cache_layout = Nested.ACTIVE_LAYOUT
        Nested.ACTIVE_LAYOUT = self
        return self

    def __exit__( self, typ, value, traceback ):
        self.layout()
        Nested.ACTIVE_LAYOUT = self.__cache_layout
        self.__cache_layout = None
        cmds.setParent( ".." ) 

    def layout(self):
        '''
        this is called at the end of a context, it can be used to (for example) perform attachments
        in a formLayout.  Override in derived classes for different behaviors.
        '''
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
            Nested.ACTIVE_LAYOUT.add(control)


# IMPORTANT NOTE
# this intentionally duplicates redundant property names from Control. That forces the metaclass to re-define the CtlProperties using cmds.layout
# instead of cmds.control. In Maya 2014, using cmds.control to query a layout fails, evem for flags they have in common

class Layout(Nested):
    
    CMD = cmds.layout
    _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'dragCallback', 'dropCallback', 'enable', 'enableBackground', 'exists', 'fullPathName', 'height',  'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']
    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus', 'childArray', 'numberOfChildren']



class Window(Nested):
    '''
 
    Window inherits from bindings.BindableObject, so it supports binding
    operators.  All controls will have _bind_src and _bind_tgt fields, and 
    if a derived control class indicates default(s) they will be used.
    
    Window inherits from styles.Styled, so it supports styling.
    
    '''
    CMD = cmds.window
    _ATTRIBS = ["backgroundColor", "defineTemplate", "docTag", "exists", "height", "iconify", "iconName", "leftEdge", "menuBarVisible", "menuIndex", "mainMenuBar", "minimizeButton", "maximizeButton",  "resizeToFitChildren", "sizeable", "title", "titleBar", "titleBarMenu", "topEdge", "toolbox", "topLeftCorner", "useTemplate", "visible", "width", "widthHeight"]
    _CALLBACKS = ["minimizeCommand", "restoreCommand"]
    _READ_ONLY = [ "numberOfMenus", "menuArray", "menuBar",  "retain"]


class Menu(Nested):
    CMD = cmds.menu
    _ATTRIBS = ['allowOptionBoxes', 'deleteAllItems', 'defineTemplate', 'docTag',  'enable', 'enableBackground', 'exists', 'familyImage', 'helpMenu',   'label', 'mnemonic', 'parent',  'useTemplate', 'visible']
    _CALLBACKS = ['postMenuCommand', 'postMenuCommandOnce']
    _READ_ONLY = ['itemArray', 'numberOfItems']


class MenuItem(Control):
    CMD = cmds.menuItem
    _ATTRIBS= ["altModifier","annotation","allowOptionBoxes","boldFont","checkBox","collection","commandModifier","ctrlModifier","divider","data","defineTemplate","docTag","echoCommand","enableCommandRepeat","enable","exists","familyImage","image","insertAfter","imageOverlayLabel","italicized","keyEquivalent","label","mnemonic","optionBox","optionBoxIcon","optionModifier","parent","radioButton","radialPosition","shiftModifier","subMenu","sourceType","tearOff","useTemplate", "version"]
    _READ_ONLY = ['isCheckBox', 'isOptionBox', 'isRadioButton']             
    _CALLBACKS = ['command', 'dragDoubleClickCommand', 'dragMenuCommand','postMenuCommand', 'postMenuCommandOnce']
    


    