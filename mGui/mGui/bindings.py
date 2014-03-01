'''
Created on Feb 16, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds
from collections import Mapping
import weakref

BINDABLE_VALUES = ['value', 'label']

BREAK_ON_BIND_FAILURE = False


class BindingError(ValueError):
    pass


class Binding(object):
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

    def update(self, *args, **kwargs):
        try:
            self._set(*args, **kwargs)
        except:
            if BREAK_ON_BIND_FAILURE:
                raise


class DictBinding(Binding):
    '''Bind to a dictionary entry'''
    def _set(self, *args, **kwargs):
        self.Target[self.FieldName] = args[0]

    def _get(self, *args, **kwargs):
        return self.Target[self.FieldName]


class PyNodeBinding(Binding):
    '''Bind to an attribute on a PyNode'''
    def _set(self, *args, **kwargs):
        getattr(self.Target, self.FieldName).set(args[0])

    def _get(self, *args, **kwargs):
        return self.Target.attr(self.FieldName).get()


class CmdsBinding(Binding):
    '''Bind to a maya attribute string'''
    def __init__(self, datum, fieldName):
        super(CmdsBinding, self).__init__(datum, fieldName)
        self._attrib = self.Target + "." + self.FieldName

    def _set(self, *args, **kwargs):
        cmds.setAttr(self._attrib, args[0])

    def _get(self, *args, **kwargs):
        return cmds.getAttr(self._attrib)


class MethodBinding(Binding):
    '''
    Bind to a method
    '''
    def _set(self, *args, **kwargs):
        getattr(self.Target, self.FieldName)(args[0])


def binding(target, targetField):
    '''
    Returns an appropriate Binding object for the supplied target and target
    field.
    '''
    if isinstance(target, Mapping):
        return DictBinding(target, targetField)
    if hasattr(target, '__melcmd__'):
        return PyNodeBinding(weakref.proxy(target), targetField)
    if hasattr(target, targetField):
        if callable(getattr(target, targetField)):
            return MethodBinding(weakref.proxy(target), targetField)
        else:
            return Binding(weakref.proxy(target), targetField)
    try:
        cmds.attributeQuery(targetField, node=target, w=True)
        return CmdsBinding(target, targetField)
    except RuntimeError:
        raise BindingError ("%s is not a bindable attribute of %s" % (targetField, target))

