'''
mGui.properties

Defines Descriptor objects for getting and setting GUI properties
'''

from events import Event, MayaEvent

class CtlProperty (object):
    '''
    Property descriptor.  When applied to a Control-derived class, invokes the
    correct Maya command under the hood to get or set values
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
    Property descriptor for callbacks.  When accessed, returns the appropriate
    Event object from a Control-derived class's Callback dictionary.

    By default, this will create a new MayaEvent (so evalDeferred safe) if 
    you have not created an event manually, so:

    button.command += doSomething
    button.command-= doSomething

    However you can also create events manually and paramaterize them

    button.command = events.MayaEvent(target = 'pCube1', distance = 2.0)
    
    '''
    def __init__(self, key):
        self.Key = key

    def __get__(self, obj, objtype):
        cb = obj.Callbacks.get(self.Key, None)
        # @note: don't use simple truth test here! No-handler event evals to false,
        # so manually assigned events are overwritten!
        if cb is None: 
            obj.Callbacks[self.Key] = MayaEvent(sender=obj)
            obj.register_callback(self.Key, obj.Callbacks[self.Key])
        return obj.Callbacks[self.Key]

    def __set__(self, obj, value):
        if not isinstance(value, Event):
            raise ValueError('Callback properties must be instances of mGui.events.Event')
        obj.Callbacks[self.Key] = value
        obj.register_callback(self.Key, obj.Callbacks[self.Key])
        

class LateBoundProperty(object):
    '''
    This is a property descriptor that's useful for mixin classes that need to
    create instance properties but which won't get called in the __init__ of a
    class they are tacked onto.

    The property in the Mixin declares a name (which will be added to every
    instance as with a leading underscore, and optionally a string name allowing
    the mixin's target class to specify a default value at the class level. For example:

    class Mixin(object):
        example = LateBoundProperty('example', '_EX')

    class Target (Mixin):
        _EX = 99

    print Target().example
    # 99
    '''
    def __init__(self, name, class_default="IGNORE"):
        self._class_default_string = class_default
        self._name = "_" + name

    def __create_backstore(self, instance, owner=None):
        if not hasattr(instance, self._name):
            default = None
            if owner and hasattr(owner, self._class_default_string):
                default = getattr(owner, self._class_default_string)
            setattr(instance, self._name, default)

    def __get__(self, instance, owner):
        self.__create_backstore(instance, owner)
        return getattr(instance, self._name)

    def __set__(self, instance, val):
        self.__create_backstore(instance)
        setattr(instance, self._name, val)
