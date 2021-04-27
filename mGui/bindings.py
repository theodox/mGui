"""
Created on Feb 16, 2014

@author: Stephen Theodore
"""
import sys

import maya.cmds as cmds
import weakref
from collections import Mapping
from mGui.properties import LateBoundProperty

# these are primarily intended for debugging.
# Generally you want to break on access failure, since the Binding
# will then invalidate itself and not run again, but you don't want
# to break on bind failure, so the GUI can run without crashing
# Use this with caution, since they are effectively globals

BREAK_ON_ACCESS_FAILURE = False  # break when an accessor fails (eg, a deleted object)
BREAK_ON_BIND_FAILURE = True  # break when a binding fails (instead of silently deleting bad binding)


class BindingError(ValueError):
    pass


class Accessor(object):
    """
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
    """

    def __init__(self, datum, field_name):
        try:
            self.target = weakref.proxy(datum)
        except TypeError:
            self.target = datum
        self.field_name = field_name

    def _set(self, *args, **kwargs):
        setattr(self.target, self.field_name, args[0])

    def _get(self, *args, **kwargs):
        return getattr(self.target, self.field_name)

    def push(self, *args, **kwargs):
        """
        Set the value in <args> on <Target.FieldName>. Return true if the set
        was done without excepting.

        If BREAK_ON_ACCESS_FAILURE is true, pass any exceptions; otherwise they
        are silently ignored
        """
        try:
            self._set(*args, **kwargs)
            return True
        except:
            if BREAK_ON_ACCESS_FAILURE:
                raise
            else:
                return False

    def pull(self, *args, **kwargs):
        """
        Returns the value from <Target.Fieldname>

        If BREAK_ON_ACCESS_FAILURE is true, pass any exceptions; otherwise, return 0
        """
        try:
            return self._get(*args, **kwargs)
        except:
            if BREAK_ON_ACCESS_FAILURE:
                raise
            else:
                return 0

    @classmethod
    def can_access(cls, datum, field_name):
        """
        Return true if the supplied object / field_name combination can be accessed from this class

        Derived classes should implement this so that the AccessorFactory can
        pick the correct Accessor for a given object
        """
        return field_name and hasattr(datum, field_name) and not callable(getattr(datum, field_name))

    def __bool__(self):
        try:
            return self.target is not None
        except ReferenceError:
            return False

    def __str__(self):
        try:
            return "<%s.%s>" % (self.target, self.field_name)
        except ReferenceError:
            return "<invalid accessor>"


class DictAccessor(Accessor):
    """
    Accessor for a dictionary entry
    """

    def __init__(self, datum, field_name):
        self.target = datum
        self.field_name = field_name

    def _set(self, *args, **kwargs):
        self.target[self.field_name] = args[0]

    def _get(self, *args, **kwargs):
        return self.target[self.field_name]

    @classmethod
    def can_access(cls, datum, field_name):
        return isinstance(datum, Mapping) or (hasattr(datum, "__getitem__") and hasattr(datum, "__setitem__"))


class PyNodeAccessor(Accessor):
    """
    Accessor fpr  an attribute on a PyNode
    """

    def _set(self, *args, **kwargs):
        getattr(self.target, self.field_name).set(args[0])

    def _get(self, *args, **kwargs):
        return self.target.attr(self.field_name).get()

    @classmethod
    def can_access(cls, datum, field_name):
        return hasattr(datum, "__melcmd__") and hasattr(datum, field_name)


class PyAttributeAccessor(Accessor):
    """
    Accessor for a PyNode attribute

    Note this creates a _strong_ reference to the attribute, so it may leak
    """

    def __init__(self, datum, field_name):
        pyAttr = datum
        self.target = pyAttr.node()
        self.field_name = pyAttr.plugAttr()
        self.attrib = pyAttr

    def _set(self, *args, **kwargs):
        self.attrib.set(args[0])

    def _get(self, *args, **kwargs):
        return self.attrib.get()

    @classmethod
    def can_access(cls, datum, field_name):
        return "Attribute" in datum.__class__.__name__


class CmdsAccessor(Accessor):
    """
    Accessor for a maya attribute string

    Unlike the other accessors the target is just a string, not a weakref
    """

    def __init__(self, datum, field_name):
        self.target = str(datum)
        self.field_name = str(field_name)
        self._attrib = "%s.%s" % (self.target, self.field_name)

    def _set(self, *args, **kwargs):
        cmds.setAttr(self._attrib, args[0])

    def _get(self, *args, **kwargs):
        return cmds.getAttr(self._attrib)

    @classmethod
    def can_access(cls, datum, field_name):
        try:
            return cmds.ls(datum) and cmds.attributeQuery(field_name, node=datum, w=True)
        except RuntimeError:
            return False
        except TypeError:
            return False


class MethodAccessor(Accessor):
    """
    Accessor for a method
    """

    def _set(self, *args, **kwargs):
        getattr(self.target, self.field_name)(*args, **kwargs)

    def _get(self, *args, **kwargs):
        return getattr(self.target, self.field_name)(*args, **kwargs)

    @classmethod
    def can_access(cls, datum, field_name):
        return field_name and hasattr(datum, field_name) and callable(getattr(datum, field_name))


class AccessorFactory(object):
    """
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
    """

    def __init__(self, *acccessor_classes):

        self.tests = [cls for cls in acccessor_classes] + [
            PyAttributeAccessor,
            PyNodeAccessor,
            Accessor,
            MethodAccessor,
            DictAccessor,
            CmdsAccessor,
        ]

    def accessor_class(self, *args):
        """
        Finds an Accessor class which can access the supplied object and field.
        If no appropriate class is found, returns None
        """
        datum = args[0]
        field_name = args[-1]

        for fclass in self.tests:
            if fclass.can_access(datum, field_name):
                return fclass
        return None


_DEFAULT_FACTORY = AccessorFactory()


def get_accessor(datum, field_name=None, factory_class=None):
    """
    Returns an appropriate Accessor object for the supplied datum and datum
    field.

    If an AccessorFactory instance is provided in <factory_class>, it will be
    used to find the correct Accessors; otherwise a default AccessorFactory will
    be used


    """

    factory = factory_class or _DEFAULT_FACTORY
    site = datum
    if isinstance(datum, BindProxy):
        site = datum.item
        field_name = datum.attribute

    target_class = factory.accessor_class(site, field_name)
    if target_class:
        return target_class(site, field_name)

    raise BindingError("%s is not a bindable attribute of %s" % (field_name, site))


class BindingContext(object):
    """
    When bindings are created they will automatically be added to the active
    BindingContext, so that they can easily be managed in groups.

    BindingContexts can be hierarchical, so a new BindingContext becomes a child
    of the active context

    By default all bindings in a context will be invoked when the context exits.
    To avoid this create the context with the auto-update flag set to false

    """

    ACTIVE = None

    def __init__(self, auto_update=True):
        self.bindings = []
        self.children = []
        self._cache_context = None
        self.auto_update = auto_update

    def __enter__(self):
        self._cache_context = BindingContext.ACTIVE
        BindingContext.ACTIVE = self
        return self

    def __exit__(self, typ, value, traceback):
        BindingContext.ACTIVE = self._cache_context
        if self._cache_context:
            self._cache_context.children.append(self)
        if self.auto_update:
            self.update(False)

    def update(self, recurse=True):
        """
        update all bindings in this context.  If recurse is True, update all bindings in child contexts

        """
        delenda = [i for i in self.bindings if not i()]
        for item in delenda:
            self.bindings.remove(item)
        if recurse:
            for item in self.children:
                item.update(recurse)
        return len(self.bindings)

    @classmethod
    def add(cls, binding):
        """
        Add a binding to the currently active BindingContext
        """
        if cls.ACTIVE is not None:
            cls.ACTIVE.bindings.append(binding)

    def invalidate(self):
        for b in self.bindings:
            b.invalidate()
        for c in self.children:
            c.invalidate()


def passthru(arg):
    """
    default nullop for un-translated bindings
    """
    return arg


class Binding(object):
    """
    Encapsulates a data binding (get accessor and  a set accessor)
    """

    def __init__(self, source, target, **kwargs):

        if not source:
            raise BindingError("invalid source binding")
        if not target:
            raise BindingError("invalid target binding")

        self.getter = source
        self.setter = target

        self.translator = kwargs.get("translator", passthru)
        assert callable(self.translator), "Translator must be a single argument callable"

        BindingContext.add(self)
        if hasattr(self.getter.target, "bindings"):
            self.getter.target.bindings.append(self)
            if hasattr(self.getter.target, "_BIND_TRIGGER"):
                cb = getattr(self.getter.target, self.getter.target._BIND_TRIGGER)
                cb += self.proxy_update

        if hasattr(self.setter.target, "bindings"):
            self.setter.target.bindings.append(self)

    def invalidate(self):
        """
        Mark the current binding as invalid. Typically it will be deleted on the next update
        """
        self.getter = None
        self.setter = None

    def __bool__(self):
        if self.setter:
            if self.getter:
                return True
        return False

    def __call__(self):
        """
        The bindings call method gets the value in the Getter and applies it to
        the Setter. If the operation is successful, returns True; otherwise
        returns False.

        In ordinary operation bindings should be exception safe, however you can
        set BREAK_ON_BIND_FAILURE to true for debugging purposes or stricter compliance.

        Typically the owning BindingContext will mark failed binds and delete
        them once they fail. If you wanted to create binding which could survive
        transient failures you'd want to make sure its __call__ would always
        return a True value
        """

        def safe_binding():
            if not self:
                return False

            try:
                val = self.getter.pull()
                self.setter.push(self.translator(val))
                return True

            except (ReferenceError, BindingError, RuntimeError):
                if BREAK_ON_BIND_FAILURE:
                    raise BindingError("Bind failure: %s" % str(sys.exc_info()[1]))
                return False

        return safe_binding()
        # this causes a hang
        # return utils.executeInMainThreadWithResult(safe_binding)

    def proxy_update(self, *args, **kwargs):
        return self()


class TwoWayBinding(Binding):
    """
    A two way binding caches the results of the last pull requests from both the
    getter and the setter, and then pushes the value which changed to the value
    which did not. If both values have changed or neither has changed, the
    'getter' value wins.
    """

    def __init__(self, source, target, *extra, **kwargs):
        super(TwoWayBinding, self).__init__(source, target, *extra, **kwargs)
        if hasattr(self.setter.target, "_BIND_TRIGGER"):
            cb = getattr(self.setter.target, self.setter.target._BIND_TRIGGER)
            cb += self.proxy_update
        self._last_getter_value = self.getter.pull()
        self._last_setter_value = self.setter.pull()

    def __call__(self):
        if not self:
            return False

        try:
            getter_val = self.getter.pull()
            new_getter = getter_val != self._last_getter_value
            setter_val = self.setter.pull()
            new_setter = setter_val != self._last_setter_value

            if new_getter and not new_setter:
                self.setter.push(self.translator(getter_val))
                self._last_setter_value = getter_val

            if new_setter and not new_getter:
                self.getter.push(self.translator(setter_val))
                self._last_getter_value = setter_val

            if not new_getter and not new_setter:
                # getter wins if both are undefined
                self.getter.push(self.translator(setter_val))
                self._last_getter_value = setter_val

            if new_setter and new_getter:
                # 'getter' > setter wins
                self.setter.push(self.translator(getter_val))
                self._last_getter_value = getter_val
                self._last_setter_value = getter_val
            return True

        except (ReferenceError, BindingError, RuntimeError):
            if BREAK_ON_BIND_FAILURE:
                raise BindingError("Bind failure: %s" % str(sys.exc_info()[1]))
            return False


class BindingExpression(object):
    """
    Allows the creation of a binding using the following syntax

         object-and-property < BindingExpression(translator) < object-and-property

    or
         object-and-property  > BindingExpression(translator) > object-and-property

    or

         object-and-property | BindingExpression(translator) | object-and-property

    The first two are equivalent except for the direction of the binding, the
    third produces as TwoWayBinding. 'Translator' is a single argument callable
    that will be used by the binding to convert the results. If not supplied, the
    binding will pass the values unchanged.

    The object-and-property items to either side of the BindingExpression can
    be any one of:

    - a BindableObject with a bind_source or bind_target set, as appropriate:

        has_default_source > bind() > has_default_target  # where both ends are BindableObjects

    - a Bindable accessed using the object.bind.property

       object.bind.property > bind() > other.bind.otherProperty

    - a Pynode Attribue (eg 'pCube1.tx' where pCube1 is a pynode)

       pCube1.tx > bind() > Button1.bind.label
       # this could be two PyNodes too, but in that case its
       # better to use driven keys or expressions which are
       # more performant

    - a Maya object/attribute string, ie ('pCube1.tx')

       'pCube1.tx' > bind() > Button1.bind.label
        # again, this could work for two object/attr strings
        # but it won't be as fast as normal maya methods

    The most general form is just tuples of (object, propertyname) :

         (object, 'property') < BindingExpression(translator) < (object, 'property')

    In that case the parens are there to make sure that the object, property pairs are tupled
    before being bound; you could do

        src = object, 'property'
        tgt = object, 'otherProperty'
        src > BindingExpression() > tgt

    for the same results.
    """

    def __gt__(self, other):
        self.right = self._flatten(other, target=True)
        if self.left and self.right:
            return self._binding()
        return self

    def __lt__(self, other):
        self.left = self._flatten(other, target=False)
        if self.left and self.right:
            return self._binding()
        return self

    def __init__(self, translator=passthru):
        self.left = None
        self.right = None
        self.isTwoWay = False
        self.translator = translator

    def __or__(self, other):
        self.right = self._flatten(other, target=False)
        self.isTwoWay = True
        if self.left and self.right:
            return self._binding()
        return self

    def __ror__(self, other):
        self.left = self._flatten(other, target=False)
        self.isTwoWay = True
        if self.left and self.right:
            return self._binding()
        return self

    def _flatten(self, other, target):
        """
        parse the binding expression and return an appropriate accessor
        """

        # BindProxy
        if isinstance(other, BindProxy):
            return get_accessor(other)

        # default bindings
        if hasattr(other, "bind_source"):
            if target and other.bind_target:
                return get_accessor(other, other.bind_target)
            elif other.bind_source:
                return get_accessor(other, other.bind_source)

        # pynodes & pyattrs
        if hasattr(other, "__melobject__") or hasattr(other, "__melcommand__"):
            return get_accessor(other, None)

        # strings
        if hasattr(other, "split") and "." in other:
            return get_accessor(*other.split("."))

        # obj, attr tuples
        if hasattr(other, "__iter__"):
            return get_accessor(*other)

        return get_accessor(other)

    def _binding(self):
        if self.isTwoWay:
            return TwoWayBinding(self.left, self.right, translator=self.translator)
        return Binding(self.left, self.right, translator=self.translator)


bind = BindingExpression
"""
This is a cheap alias to make the typing less onerous
"""


# ============================================================================================


class Bindable(object):
    """
    A Mixin class that adds a binding syntax to an object.

    Bindable adds a quasi-property, 'bind', which return a BindProxy
    object which is a valid target for a binding. A typical use would look like:

    class Flintstone(Bindable):
        def __init__(self, name, val):
            self.Name = name
            self.Value  = val

    fred = Flintstone("Fred", "Husband")
    wilma = Flinstone("Wilma", "Wife")

    new_binding = fred.bind.Value > bind() > wilma.bind.Name
    new_binding() # call the binding manually
    wilma.Name
    # Husband

    You can also use the '&' symbol as an alternate way of specifying a bindable property:

       object & 'property'

    is the same as

       object.bind.property

    """

    _BINDINGS = []

    # ===========================================================================
    # internal classes
    # ===========================================================================

    class ProxyFactory(object):
        """
        Used as dummy to allow  object.bind.property creation of bindProxies
        """

        def __init__(self, owner):
            self.owner = owner

        def __getattr__(self, name):
            if name != "owner":
                if hasattr(self.owner, name):
                    return BindProxy(self.owner, name)
            raise BindingError("Object %s does not have a bindable attribute named %s" % (self.owner, name))

    class ProxyFactoryProperty(object):
        """
        Descriptor which adds the .bind. syntax to Bindables
        """

        def __get__(self, instance, owner):
            if not hasattr(instance, "_proxy_factory"):
                setattr(instance, "_proxy_factory", Bindable.ProxyFactory(instance))
            return instance._proxy_factory

    # ===========================================================================
    # end internal classes
    # ===========================================================================

    bind = ProxyFactoryProperty()

    def __and__(self, name):
        """
        Allows using the & symbol as a shorthand for the bind syntax:

           object & 'property'

        is the same as

           object.bind.property
        """
        return BindProxy(self, name)


class BindableObject(Bindable):
    """
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
        Fred > bind() > OtherGuy

        # which is equal to
        # Fred.bind.Name > bind() > OtherGuy.bind.Name

    """

    _BIND_SRC = None
    _BIND_TGT = None
    _BINDINGS = []

    bind_source = LateBoundProperty("bind_source", "_BIND_SRC")
    bind_target = LateBoundProperty("bind_target", "_BIND_TGT")
    bindings = LateBoundProperty("bindings", "_BINDINGS")

    def get_bindings(self):
        """
        Returns all of the bindings attached to this object
        """
        return [i for i in self.bindings]

    def update_bindings(self):
        delenda = [i for i in self.bindings if not i()]
        for d in delenda:
            self.bindings.remove(d)

    def clear_bindings(self):
        for item in self.bindings:
            item.invalidate()
        self.bindings[:] = []


class BindProxy(Bindable):
    """
    Creates a bindable Object + Attribute pair

    Note that bindProxies do NOT maintain an internal bindings list - you'll
    need to capture the bindings created by them in a BindingContext or manually

    """

    def __init__(self, item, attrib):
        self.item = item
        self.attribute = attrib
