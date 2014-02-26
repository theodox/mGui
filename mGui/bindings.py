'''
Created on Feb 16, 2014

@author: Stephen Theodore
'''
import maya.cmds as cmds

BINDABLE_VALUES = ['value', 'label'
                   ]


class TargetBinding(object):
    '''
    Provides a simple way for GUI controls to update the underlying model objects when their values change.
    
    Sample usage:
    
        start_field = cmds.intField(v=datum.Start, cc = mvc.Binding(datum, "Start"))

    as long as datum is a reference type with a field named "Start", the binding will update the datum with the new values
    '''
    def __init__(self, datum, fieldName):
        
        self.Target = datum
        self.FieldName = fieldName
        
    def __call__(self,*args, **kwargs):
        if isinstance(self.Target, dict):
            self.Target[self.FieldName] = args[0]
        else:
            try:
                v = getattr(self.Target, self.FieldName)
                if callable(v):
                    v(args[0])
                    return
            except AttributeError:
                if hasattr(self.Target, 'attr'):
                    self.Target.attr(self.FieldName).set(args[0])
                    return
                try:
                    cmds.setAttr("%s.%s" % (self.Target, self.FieldName), args[0])
                except RuntimeError:
                    setattr(self.Target, self.FieldName, args[0])
                
    def update(self):
        self()
        

class SourceBinding(object):
    def __init__(self, sourceObject, sourceAttr, targetObject, targetAttr):
        self.SourceObject = sourceObject
        self.SourceAttr = sourceAttr
        self._binding_type = None
        self.TargetObject = targetObject
        self.TargetAttr = targetAttr
        

    def update(self):
        
        def py_object_value():
            v =  getattr(self.SourceObject, self.SourceAttr)
            if callable (v):
                return v()
            else:
                return v
            
        def maya_object_value():
            return cmds.getAttr("%s.%s" % (self.SourceObject, self.SourceAttr))
        
        if not self._binding_type:
            try:
                setattr(self.TargetObject, self.TargetAttr, maya_object_value())
                self._binding_type = maya_object_value
            except RuntimeError:
                setattr(self.TargetObject, self.TargetAttr, maya_object_value())
                self._binding_type = py_object_value
        else:
            setattr(self.TargetObject, self.TargetAttr,  self._binding_type()) 
    