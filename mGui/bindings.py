'''
Created on Feb 16, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds
from collections import Mapping
import weakref

BINDABLE_VALUES = ['value', 'label']

BREAK_ON_BIND_FAILURE = True

class BindingError(ValueError):
    pass

class Setter(object):
    '''
    Bind to an object field. 
    '''
    def __init__(self, datum, fieldName):
        self.Source = datum
        self.FieldName = fieldName
        
    def _set(self, *args, **kwargs):
        setattr(self.Source, self.FieldName, args[0])
    
    def do_set(self, *args, **kwargs):
        try:
            self._set(*args, **kwargs)
        except:
            if BREAK_ON_BIND_FAILURE:
                raise
            
class DictSetter(Setter):
    '''Bind to a dictionary entry'''
    def _set(self, *args, **kwargs):
        self.Source[self.FieldName] = args[0]
        
class PyNodeSetter(Setter):
    '''Bind to an attribute on a PyNode'''
    def _set(self, *args, **kwargs):
        getattr(self.Source, self.FieldName).set(args[0])
    
class CmdsSetter(Setter):
    '''Bind to a maya attribute string'''    
    def __init__(self, datum, fieldName):
        super(CmdsSetter, self).__init__(datum, fieldName)
        self._attrib = self.Source + "." + self.FieldName

    def _set(self, *args, **kwargs):
        cmds.setAttr(self._attrib, args[0])
        
class MethodSetter(Setter):
    
    def _set(self, *args, **kwargs):
        getattr(self.Source, self.FieldName)(args[0])
        
        
def setter(target, targetField):
    '''
    Returns an appropriate Setter object for the supplied target and target field.
    '''
    if isinstance(target, Mapping): return DictSetter(target, targetField)
    if hasattr(target, '__melcmd__'): return PyNodeSetter(weakref.proxy(target), targetField)
    if hasattr(target, targetField):
        if callable(getattr(target, targetField)):
            return MethodSetter (weakref.proxy(target), targetField)
        else:
            return Setter(weakref.proxy(target), targetField)
    try:
        cmds.attributeQuery(targetField, node=target, w=True)
        return CmdsSetter(target, targetField)
    except (RuntimeError, AttributeError): # AttributeError may get fired on string lookup if maya is not loaded
        raise BindingError ("%s is not a bindable attribute of %s" % (targetField, target))
        
class Getter(object):
    '''
    Bind to an object field. 
    '''
    def __init__(self, datum, fieldName):
        self.Source = datum
        self.FieldName = fieldName
        
    def _get(self, *args, **kwargs):
        return getattr(self.Source, self.FieldName)
    
    def do_get(self, *args, **kwargs):
        try:
            return self._get(*args, **kwargs)
        except:
            if BREAK_ON_BIND_FAILURE:
                raise
            
class DictGetter(Getter):
    '''Bind to a dictionary entry'''
    def _get(self, *args, **kwargs):
        return self.Source[self.FieldName]
        
class PyNodeGetter(Getter):
    '''Bind to an attribute on a PyNode'''
    def _get(self, *args, **kwargs):
        return getattr(self.Source, self.FieldName).get()
    
class CmdsGetter(Getter):
    '''Bind to a maya attribute string'''    
    def __init__(self, datum, fieldName):
        super(CmdsGetter, self).__init__(datum, fieldName)
        self._attrib = self.Source + "." + self.FieldName

    def _get(self, *args, **kwargs):
        return cmds.getAttr(self._attrib)
        
class MethodGetter(Getter):
    '''Bind to a method'''
    def _get(self, *args, **kwargs):
        return getattr(self.Source, self.FieldName)(*args, **kwargs)
    
def getter(target, targetField):
    '''
    Returns an appropriate Setter object for the supplied target and target field.
    '''
    if isinstance(target, Mapping): return DictGetter(target, targetField)
    if hasattr(target, '__melcmd__'): return PyNodeGetter(weakref.proxy(target), targetField)
    if hasattr(target, targetField):
        if callable(getattr(target, targetField)):
            return MethodGetter (weakref.proxy(target), targetField)
        else:
            return Getter(weakref.proxy(target), targetField)
    try:
        cmds.attributeQuery(targetField, node=target, w=True)
        return CmdsGetter(target, targetField)
    except (RuntimeError, AttributeError):
        raise BindingError ("%s is not a bindable attribute of %s" % (targetField, target))
    
class Binding(object):
    BINDINGS = []
    
    def __init__(self, source, target, *extra):
        try:
            if extra:
                src = (source, target)
                tgt = (extra[0:2])
            else:
                src = source
                tgt = target
        
            self.Getter = getter(*src)
            self.Setter = setter(*tgt)
            self.BINDINGS.append(self)
        except IndexError:
            raise BindingError('binding requires 2 or 4 arguments')
        
    def __call__(self):
        try:
            self.Setter.do_set(self.Getter.do_get())
            return True
        except ReferenceError:
            return False

    @classmethod
    def update(cls):
        delenda = [i for i in cls.BINDINGS if not i()]
        for item in delenda:
            cls.BINDINGS.remove(item)
        return len(cls.BINDINGS)


class Bindable (object):

    def site(self):
        return self
    
    
    def __rshift__(self, other):
        if not self.bind_source:
            raise BindingError("bind source is not set for %s" % self)
        if hasattr(other, 'bind_target'):
            return Binding(self.site(), self.bind_source, other.site(), other.bind_target ) 
        elif len(other) == 2:
            return Binding ((self.site(), self.bind_source), other)
        raise BindingError("Invalid bind target %s" % str(other))
    
    def __lshift__(self, other):
        if not self.bind_target:
            raise BindingError("bind target is not set for %s" % self)
        if hasattr(other, 'bind_source'):
            return Binding(other.site(), other.bind_source, self.site(), self.bind_target) 
        elif len(other) == 2:
            return Binding (other, (self.site(), self.bind_target))
        raise BindingError("Invalid bind target %s" % str(other))
        
    def __floordiv__ (self, other):
        return BindProxy(self, other)

class BindableObject(Bindable):
    _BIND_SRC = None
    _BIND_TGT = None
    
    def __new__(self, *args, **kwargs):
        obj = object.__new__(self)
        self.bind_source = self._BIND_SRC
        self.bind_target = self._BIND_TGT
        return obj

class BindProxy(Bindable):
    def __init__(self, item, attrib):
        self.Item = item
        self.bind_source = self.bind_target = attrib
        
    def site(self):
        return self.Item
    
    
        

class Example( BindableObject):
    _BIND_SRC = 'Name'
    _BIND_TGT = 'Val'
    
    def __init__(self, name, val):
        self.Name = name
        self.Val = val
        
    def __str__(self):
        return 'Name %s Val %s' % (self.Name, self.Val)


        
import types
        
def test():
    import maya.standalone
    maya.standalone.initialize()
    cmds.polyCube()
    
    dino = Example("dino", 99)
    dino.food = "bone"
    barney = Example("barney", "rubble")
    barney.hair = "yellow"
    fred = Example("fred", "flintstone")
    def test(self, val): self.Name = val.upper()
    def zzz (self): return self.Name + "_" + self.Val
    fred.up = types.MethodType(test, fred)
    fred.down = types.MethodType(zzz, fred)
    dino // 'Val' >> ('pCube1', 'tx')
    barney << fred
    barney >> dino
    wilma = {'wilma':'wilma'}
    wilma['wilma'] = 'nope'
    barney // 'Val' << (wilma, 'wilma')
    q = Binding(fred, 'down', wilma, 'down')
    
    Binding.update()
    
    print fred
    print barney
    print dino
    print wilma
    print cmds.getAttr('pCube1.t')
    
test()
print Binding.BINDINGS
Binding.update()
print Binding.BINDINGS