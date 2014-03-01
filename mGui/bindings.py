'''
Created on Feb 16, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds
from collections import Mapping
import weakref


BREAK_ON_BIND_FAILURE = True


class BindingError(ValueError):
    pass


class Accessor(object):
    '''
    Bind to an object field.
    '''
    def __init__(self, datum, fieldName):
        self.Target = datum
        self.FieldName = fieldName

    def _set(self, *args, **kwargs):
        setattr(self.Target, self.FieldName, args[0])

    def _get(self, *args, **kwargs):
        return getattr(self.Target, self.FieldName)

    def push(self, *args, **kwargs):
        '''
        Set the value in <args> on <Target.FieldName>
        '''
        try:
            self._set(*args, **kwargs)
        except:
            if BREAK_ON_BIND_FAILURE:
                raise

    def pull(self, *args, **kwargs):
        '''
        Returns the value from <Target.Fieldname>
        '''
        try:
            return self._get(*args, **kwargs)
        except:
            if BREAK_ON_BIND_FAILURE:
                raise
            else:
                return ''


class DictAccessor(Accessor):
    '''
    Accessor for a dictionary entry
    '''
    def _set(self, *args, **kwargs):
        self.Target[self.FieldName] = args[0]

    def _get(self, *args, **kwargs):
        return self.Target[self.FieldName]


class PyNodeAccessor(Accessor):
    '''
    Accessor fpr  an attribute on a PyNode
    '''
    def _set(self, *args, **kwargs):
        getattr(self.Target, self.FieldName).set(args[0])

    def _get(self, *args, **kwargs):
        return self.Target.attr(self.FieldName).get()


class CmdsAccessor(Accessor):
    '''
    Accessor for a maya attribute string
    '''
    def __init__(self, datum, fieldName):
        super(CmdsAccessor, self).__init__(datum, fieldName)
        self._attrib = self.Target + "." + self.FieldName

    def _set(self, *args, **kwargs):
        cmds.setAttr(self._attrib, args[0])

    def _get(self, *args, **kwargs):
        return cmds.getAttr(self._attrib)


class MethodAccessor(Accessor):
    '''
    Accessor for a method
    '''
    def _set(self, *args, **kwargs):
        getattr(self.Target, self.FieldName)(*args, **kwargs)

    def _get(self, *args, **kwargs):
        return getattr(self.Target, self.FieldName)(*args, **kwargs)


def get_accessor(target, targetField):
    '''
    Returns an appropriate Accessor object for the supplied target and target
    field.
    '''
    if isinstance(target, Mapping):
        return DictAccessor(target, targetField)
    if hasattr(target, '__melcmd__'):
        return PyNodeAccessor(weakref.proxy(target), targetField)
    if hasattr(target, targetField):
        if callable(getattr(target, targetField)):
            return MethodAccessor(weakref.proxy(target), targetField)
        else:
            return Accessor(weakref.proxy(target), targetField)
    try:
        cmds.attributeQuery(targetField, node=target, w=True)
        return CmdsAccessor(target, targetField)
    except RuntimeError:
        tgt_string = '%s.%s' % (targetField, target)
        raise BindingError("%s is not a bindable attribute of %s" % tgt_string)


class BindingContext(object):

    ACTIVE = None

    def __init__(self, update_on_close=True):
        self.Bindings = []
        self._cache_context = None
        self._update_on_close = update_on_close

    def __enter__(self):
        self._cache_context = self.ACTIVE
        BindingContext.ACTIVE = self
        return self

    def __exit__(self, typ, value, traceback):
        BindingContext.ACTIVE = self._cache_context
        if self._update_on_close:
            self.update()

    def update(self):
        '''
        update all bindings in thie context
        '''
        delenda = [i for i in self.Bindings if not i()]
        for item in delenda:
            self.Bindings.remove(item)
        return len(self.Bindings)

    @classmethod
    def add(cls, binding):
        print cls, binding, cls.ACTIVE.Bindings
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

    def __call__(self):
        try:
            self.Setter.push(self.Translator(self.Getter.pull()))
            return True
        except ReferenceError:
            return False


class Bindable (object):

    def site(self):
        return self

    def __rshift__(self, other):
        if not self.bind_source:
            raise BindingError("bind source is not set for %s" % self)
        if hasattr(other, 'bind_target'):
            return Binding(self.site(), self.bind_source, other.site(), other.bind_target)
        elif len(other) == 2:
            return Binding((self.site(), self.bind_source), other)
        raise BindingError("Invalid bind target %s" % str(other))

    def __lshift__(self, other):
        if not self.bind_target:
            raise BindingError("bind target is not set for %s" % self)
        if hasattr(other, 'bind_source'):
            return Binding(other.site(), other.bind_source, self.site(), self.bind_target)
        elif len(other) == 2:
            return Binding(other, (self.site(), self.bind_target))
        raise BindingError("Invalid bind target %s" % str(other))

    def __floordiv__(self, other):
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


class Example(BindableObject):
    _BIND_SRC = 'Name'
    _BIND_TGT = 'Val'

    def __init__(self, name, val):
        self.Name = name
        self.Val = val

    def __str__(self):
        return 'Name %s Val %s' % (self.Name, self.Val)



import types

def test():

    with BindingContext() as ggg:
        dino = Example("dino", 99)
        dino.food = "bone"
        barney = Example("barney", "rubble")
        barney.hair = "yellow"
        fred = Example("fred", "flintstone")
        def test(self, val): self.Name = val.upper()
        def zzz (self): return self.Name + "_" + self.Val
        fred.up = types.MethodType(test, fred)
        fred.down = types.MethodType(zzz, fred)
        barney << fred
        barney // 'hair' >> dino
        wilma = {'wilma':'wilma'}
        wilma['wilma'] = 'nope'
        barney // 'Val' << (wilma, 'wilma')
        q = Binding(fred, 'down', wilma, 'down', translate=str.upper)

    # #ggg.update()
    print ggg.Bindings

    print fred
    print barney
    print dino
    print wilma

test()

