'''
mGui.properties

Defines Descriptor objects for getting and setting GUI properties
'''

from events import MayaEvent

class CtlProperty (object):
    '''
    Property descriptor.  When applied to a Control-derived class, invokes the
    correct Maya command under the hood to get or set values
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
    Property descriptor for callbacks.  When accessed, returns the appropriate
    Event object from a Control-derived class's Callback dictionary. This
    property cannot be 'set' or 'unset' - instead use the += or -= methods on
    the underlying Event object:
    
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
            obj.Callbacks[self.Key] = MayaEvent(gui = obj)
            obj.register_callback(self.Key, obj.Callbacks[self.Key])
        return obj.Callbacks[self.Key]
