'''
Created on Feb 16, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds
from collections import Mapping
import weakref
import sys

# these are primarily intended for debugging.
# Generally you want to break on access failure, since the Binding
# will then invalidate itself and not run again, but you don't want
# to break on bind failure, so the GUI can run without crashing
# Use thise with caution, since they are effectively globals

BREAK_ON_ACCESS_FAILURE = True   # break when an accessor fails (eg, a deleted object)
BREAK_ON_BIND_FAILURE = False     # break when a binding fails (instead of silently deleting bad binding)


class BindingError(ValueError):
    pass


class Accessor(object):
    '''
    An Accessor abstracts the details of getting or setting an object property,
    so that calling code can get or set values without knowing the precise
    mechanism involved.  
    
    The base Accessor class works on plain python objects. There are derived
    classes for PyNode, maya cmds strings, dictionaries and get-set methods.
    
    In most cases the <Target> field is a weakref rather than a regular object
    reference. This prevents a binding from keeping an object alive in memory if
    it is not accessed anywhere else.  Some classes (such as dictionaries or datettimes)
    cannot be weak referenced so these are stored as ordinary objects.
    
    Truth-testing an accessor returns true if the Accessors <Target> exists.
    '''
    def __init__(self, datum, fieldName):
        try:
            self.Target = weakref.proxy(datum)
        except TypeError:
            self.Target = datum
        self.FieldName = fieldName

    def _set(self, *args, **kwargs):
        setattr(self.Target, self.FieldName, args[0])

    def _get(self, *args, **kwargs):
        return getattr(self.Target, self.FieldName)

    def push(self, *args, **kwargs):
        '''
        Set the value in <args> on <Target.FieldName>. Return true if the set
        was done without excepting.
        
        If BREAK_ON_ACCESS_FAILURE is true, pass any exceptions; otherwise they
        are silenly ignored
        '''
        try:
            self._set(*args, **kwargs)
            return True
        except:
            if BREAK_ON_ACCESS_FAILURE:
                raise
            else:
                return False

    def pull(self, *args, **kwargs):
        '''
        Returns the value from <Target.Fieldname>
        
        If BREAK_ON_ACCESS_FAILURE is true, pass any exceptions; otherwise, return 0
        '''
        try:
            return self._get(*args, **kwargs)
        except:
            if BREAK_ON_ACCESS_FAILURE:
                raise
            else:
                return 0


    @classmethod
    def can_access(cls, datum, fieldname):
        '''
        Return true if the supplied object / fieldname combination can be accessed from this class
        
        Derived classes should implement this so that the AccessorFactory can
        pick the correct Accessor for a given object
        '''
        return hasattr(datum, fieldname) and not callable(getattr(datum, fieldname)) 
    
    def __nonzero__(self):
        try:
            return not self.Target is None
        except ReferenceError:
            return False
        
        
    
    def __str__(self):
        try:
            return "<%s.%s>" % (self.Target, self.FieldName)
        except ReferenceError:
            return "<invalid accessor>"
        
class DictAccessor(Accessor):
    '''
    Accessor for a dictionary entry
    '''
    def __init__(self, datum, fieldName):
        self.Target = datum
        self.FieldName = fieldName
    
    def _set(self, *args, **kwargs):
        self.Target[self.FieldName] = args[0]

    def _get(self, *args, **kwargs):
        return self.Target[self.FieldName]

    @classmethod
    def can_access(cls, datum, fieldname):
        return isinstance (datum, Mapping) or (hasattr(datum, '__getitem__') and hasattr(datum, '__setitem__'))


class PyNodeAccessor(Accessor):
    '''
    Accessor fpr  an attribute on a PyNode
    '''
    def _set(self, *args, **kwargs):
        getattr(self.Target, self.FieldName).set(args[0])

    def _get(self, *args, **kwargs):
        return self.Target.attr(self.FieldName).get()

    @classmethod 
    def can_access(cls, datum, fieldname):
        return hasattr(datum, '__melcmd__') and hasattr(datum, fieldname)
    
class CmdsAccessor(Accessor):
    '''
    Accessor for a maya attribute string
    
    Unlike the other accessors the target is just a string, not a weakref
    '''
    def __init__(self, datum, fieldName):
        self.Target = str(datum)
        self.FieldName = str(fieldName)
        self._attrib = "%s.%s" % (self.Target, self.FieldName)

    def _set(self, *args, **kwargs):
        cmds.setAttr(self._attrib, args[0])
        
    def _get(self, *args, **kwargs):
        return cmds.getAttr(self._attrib)

    @classmethod
    def can_access(self, datum, fieldname):
        try:
            return cmds.ls(datum) and cmds.attributeQuery(fieldname, node=datum, w=True)
        except RuntimeError:
            return False
        except TypeError:
            return False
        
class MethodAccessor(Accessor):
    '''
    Accessor for a method
    '''
    def _set(self, *args, **kwargs):
        getattr(self.Target, self.FieldName)(*args, **kwargs)

    def _get(self, *args, **kwargs):
        return getattr(self.Target, self.FieldName)(*args, **kwargs)

    @classmethod
    def can_access(cls, datum, fieldname):
        return hasattr(datum, fieldname) and callable(getattr(datum, fieldname))


class AccessorFactory(object):
    '''
    The Accessor factory loops through the default Accessor classes and returns
    an appropriate class for a given combination of object and field names.
    
    Ordinarily users will call bindings.get_accessor and use the default factory
    stored in bindings._DEFAULT_FACTORY. However if you want to create new
    bindings (say, for a SQL data row or an http connection) you would create
    new binding classes with their own <can_access> methods and create a custom
    AccessorFactory:
    
        custom_fact = AccessorFactory(MySqlAccessor, HttpAccessor)
        bindings.get_accessor(factory_class = custom_fact
    
    The order in which the tests run is determined by the order in which they
    are added in the constructor. Custom classes will be tested before the
    default classes
    '''
    
    def __init__(self, *accessorClasses ):
        
        self.Tests = [cls for cls in accessorClasses ] + [PyNodeAccessor, Accessor, MethodAccessor, DictAccessor, CmdsAccessor] 

    def accessor_class(self, datum, fieldname):
        '''
        Finds an Accessor class which can access the supplied object and field.
        If no appropriate class is found, returns None
        '''
        for fclass in self.Tests:
            if fclass.can_access(datum, fieldname ):
                return fclass
        
        return None
    
_DEFAULT_FACTORY = AccessorFactory()

def get_accessor(datum, fieldname, factory_class = None):
    '''
    Returns an appropriate Accessor object for the supplied datum and datum
    field.
    
    If an AccessorFactory instance is provided in <factory_class>, it will be
    used to find the correct Accessors; otherwise a default AccessorFactory will
    be used
    
    '''
    
    factory = factory_class or _DEFAULT_FACTORY
    site = datum
    if hasattr(datum, 'site'):
        site = datum.site()
    target_class = factory.accessor_class(site, fieldname)
    if target_class:
        return target_class(datum, fieldname)
    raise BindingError ('%s is not a bindable attribute of %s' % (fieldname, site))



class BindingContext(object):
    '''
    When bindings are created they will automatically be added to the active
    BindingContext, so that they can easily be managed in groups.
    
    BindingContexts can be hierarchical, so a new BindingContext becomes a child
    of the active context
    
    By default all bindings in a context will be invoked when the context exits.
    To avoid this create the context with the auto-update flag set to false
    
    '''

    ACTIVE = None

    def __init__(self, auto_update=True):
        self.Bindings = []
        self.Children = []
        self._cache_context = None
        self.auto_update = auto_update

    def __enter__(self):
        self._cache_context = self.ACTIVE
        if self._cache_context:
            self._cache_context.Children.append(self)
        BindingContext.ACTIVE = self
        return self

    def __exit__(self, typ, value, traceback):
        BindingContext.ACTIVE = self._cache_context
        if self.auto_update:
            self.update(False)

    def update(self, recurse = True):
        '''
        update all bindings in this context.  If recurse is True, update all bindings in child contexts
        
        '''
        delenda = [i for i in self.Bindings if not i()]
        for item in delenda:
            self.Bindings.remove(item)
        if recurse:
            for item in self.Children:
                item.update(recurse)
            
        return len(self.Bindings)
    
        

    @classmethod
    def add(cls, binding):
        '''
        Add a binding to the currently active BindingContext
        '''
        if cls.ACTIVE:
            cls.ACTIVE.Bindings.append(binding)


class Binding(object):
    '''
    Encapsulates a data binding (get accessor and  a set accessor)
    '''

    def __init__(self, source, target, *extra, **kwargs):
        try:
            if extra:
                src = (source, target)
                tgt = (extra[0:2])
            else:
                src = source
                tgt = target

            self.Getter = get_accessor(*src)
            self.Setter = get_accessor(*tgt)

        except IndexError:
            raise BindingError('get_accessor requires 2 or 4 arguments')

        self.Translator = kwargs.get('translate', lambda v: v)
        assert callable(self.Translator), 'Translator must be a single argument callable'

        BindingContext.add(self)
        if hasattr(self.Getter.Target, 'bindings'):
            self.Getter.Target.bindings.append(self)
        if hasattr(self.Setter.Target, 'bindings'):
            self.Setter.Target.bindings.append(self)
            
        
    def invalidate(self):
        '''
        Mark the current binding as invalid. Typically it will be deleted on the next update
        '''
        self.Getter = None
        self.Setter = None

    def __nonzero__(self):
        if self.Setter:
            if self.Getter:
                return True
        return False

    def __call__(self):
        '''
        The bindings call method gets the value in the Getter and applies it to
        the Setter. If the operation is successful, returns True; otherwise
        returns False.
        
        In ordinary operation bindings should be exception safe, however you can
        set BREAK_ON_BIND_FAILURE to true for debugging purposes or stricter compliance.
        
        Typically the owning BindingContext will mark failed binds and delete
        them once they fail. If you wanted to create binding which could survive
        transient failures you'd want to make sure its __call__ would always
        return a True value
        '''
        if self.__nonzero__() == False: return False
        
        
        try:
            val = self.Getter.pull()
            self.Setter.push(self.Translator(val))
            return True
        except (ReferenceError, BindingError, RuntimeError):
            if BREAK_ON_BIND_FAILURE:
                raise BindingError ("Bind failure: %s" % str(sys.exc_info()[1]))
            return False
            


class TwoWayBinding(Binding):
    '''
    A two way binding caches the results of the last pull requests from both the
    getter and the setter, and then pushes the value which changed to the value
    which did not. If both values have changed, the first defined value wins
    '''
    def __init__(self,source, target, *extra, **kwargs):
        super(TwoWayBinding, self).__init__(source, target, *extra, **kwargs)
        self._last_getter_value = self.Getter.pull()
        self._last_setter_value = self.Setter.pull()
        
    def __call__(self):
        if self.__nonzero__() == False: return False
    
    
        try:
            getter_val = self.Getter.pull()
            new_getter = getter_val != self._last_getter_value
            setter_val = self.Setter.pull()
            new_setter = setter_val != self._last_setter_value
            
            
            if new_getter and not new_setter:    
                self.Setter.push(self.Translator(getter_val))
                self._last_setter_value = getter_val
            if new_setter and not new_getter:
                self.Getter.push(self.Translator(setter_val))
                self._last_getter_value = setter_val
            if new_setter and new_getter:
                # 'getter' > setter wins
                self.Setter.push(self.Translator(getter_val))    
                self._last_getter_value = getter_val    
                self._last_setter_value = getter_val
            return True
        except (ReferenceError, BindingError, RuntimeError):
            if BREAK_ON_BIND_FAILURE:
                raise BindingError ("Bind failure: %s" % str(sys.exc_info()[1]))
            return False
            
        

#============================================================================================


class Bindable (object):
    '''
    A Mixin class that adds a binding syntax to an object.
    
    Bindables can create a new binding by using the left-shift (<<) and right
    shift (>>) operators. The addition operator (+) returns a BindProxy, which
    is a quick way to define an object/attribute pair for binding
    
        class Example(BindableObject):
            _BIND_SRC = 'Name'
            _BIND_TGT = 'Val'
        
            def __init__(self, name, val):
                self.Name = name
                self.Val = val
        Fred = Example('Fred', 'Flinstone')
        Barney = Example('Barney', 'Rubble')
        
        test_bind = Fred + Name >> Barney + Name  # create a binding from Fred's name to Barney's name
        test_bind()
        print Barney.Name
        'Fred'
        
    To use the syntax above the first item in the expression MUST inherit from
    Bindable.  The second operand (on the far side of the lshift or rshift) can
    be a bindable pair defined by a + or a tuple of (object, attribute): thus
    
       Barney + 'Name' << Fred + 'Val'  # Two bindables, barney changed fred
       Barney + 'Name' >> Fred + 'Val'  # Two bindables, fred changes barney

       Barney + 'Val' >> (SomeClass, 'someAttr')  # bindable to object, attrib tuple
       Barney + 'Val' << (SomeClass, 'someAttr')  # tuple can update bindable
       
   however this will NOT work:
   
       (SomeClass, 'someAttr')  >> Barney + 'Name'
       
    because the left hand pair is not a Bindable. You can, however, write
    
       BindProxy(SomeClass, 'someAttr') >> Barney + 'Name'
           
    '''

    def site(self):
        return self

    def __rshift__(self, other):
        if not self.bind_source:
            raise BindingError("bind source is not set for %s" % self)
        target = self._get_bindable(other, 'bind_target')
        if not target: 
            raise BindingError("bind target is not set for %s" % other)
        return Binding(self.site(), self.bind_source, target.site(), target.bind_target)

        
    def __lshift__(self, other):
        if not self.bind_target:
            raise BindingError("bind target is not set for %s" % self)
        target = self._get_bindable(other, 'bind_source')
        if not target: 
            raise BindingError("bind source is not set for %s" % other)
        return  Binding( target.site(), target.bind_source,self.site(), self.bind_target)

    def __ne__(self, other):         
        if not self.bind_target:
            raise BindingError("bind target is not set for %s" % self)
        target = self._get_bindable(other, 'bind_source')
        if not target: 
            raise BindingError("bind source is not set for %s" % other)
        return TwoWayBinding(self.site(), self.bind_source, target.site(), target.bind_target)


    def __add__(self, other):
        return BindProxy(self, other)
    
    def _get_bindable(self, other, src_or_target ):
        if hasattr(other, 'site') and hasattr(other, src_or_target):
            return other
        if hasattr(other, '__iter__') and len(other) == 2:
            return BindProxy(*other)

        return None
    
        

class BindableObject(Bindable):
    '''
    BindableObject is an extension of Bindable which defines a default binds
    source and bind target for an object. This is handy for UI objects that
    typically bind only one value at a time.
    
    When a BindableObject is used in a binding expression (see @Bindable), you
    can omit the explicit specification of the attribute.  So for example:
    
        class DefaultBind (BindableObject):
            _BIND_SRC = 'Name'
            _BIND_TGT = 'Name'
            
            def _init_(self, name):
                self.Name = name
                
        
        Fred = DefaultBind('Fred Flinstone')
        OtherGuy = DefaultBind('Barney Rubble')
        
        Fred >> OtherGuy  # is equal to Fred + 'Name' >> OtherGuy + 'Name'
    
    @note: be careful in overriding __new__ in derived classes: this class uses
    __new__ so inheritors don't need to call super in their constructors
        
    '''
    
    
    _BIND_SRC = None
    _BIND_TGT = None

    def __new__(self, *args, **kwargs):
        obj = object.__new__(self)
        self.bind_source = self._BIND_SRC
        self.bind_target = self._BIND_TGT
        self.bindings = []
        return obj

    def get_bindings(self):
        '''
        Returns all of the bindings attached to this object
        '''
        return [i for i in self.bindings]
    
    def update_bindings(self):
        delenda = [i for i in self.bindings if not i()]
        for d in delenda:
            self.bindings.remove(d)

class BindProxy(Bindable):
    '''
    Creates an bindable Object + Attribute pair
    
    Note that bindProxies do NOT maintain an internal bindings list - you'll
    need to capture the bindings created by them in a BindingContext or manually
    
    '''
    
    def __init__(self, item, attrib):
        self.Item = item
        self.bind_source = self.bind_target = attrib

    def site(self):
        if hasattr(self.Item, 'site'): return self.Item.site()
        return self.Item

    
