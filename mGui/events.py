'''
events.py

Defines a simple event handler system similar to that used in C#.  Events allow
multicast delegates and arbitrary message passing. They use weak references so
they don't keep their handlers alive if they are otherwise out of scope.

'''
import weakref
import maya.utils
from functools import  partial


class Event(object):
    '''
    Simple event handler, similar to the standard c# event pattern. The object
    raising an event calls this event object as a callable; the object will in
    turn fire any of the callables it stores in its Handlers list, passing the
    args and kwargs provided by the original caller.

    sample usage:
        test = Event()

        > def a ( *args, **kwargs ):
            print "A", args, kwargs
        > test += a;
        > test( 'arg1', 'arg2', e="fred" )
        A ('arg1', 'arg2') {'e': 'fred', 'event': <Event object at 0x00000000026892E8>}

    the handlers are stored as weakrefs, so they will not keep their referents alive if those referents exists
    in no other scope. For example:

        > x = Event()
        > def test(*args, **kwargs):
        >     print "hello world"
        > x += test
        > x()
        hello world
        > test = None
        > x()

    Handlers must exhibit the *args, **kwargs signature.  It's the handler's job
    to decide what to do with them but they will be passed.

    Events can be given 'metadata' - arguments that are passed in at creation time:

        x = Event(name = 'test_event')
        def test (*args, *kwargs):
            print args, kwargs

        x()
        {'name': 'test_event', 'event': <Event object at 0x00000000026892E8>}

    Metadata added when the Event is first created will be included in every
    firing of the event. Arguments and keywords can also be associated with a
    particular firing:

        x = Event(name = 'test_event')
        def test (*args, *kwargs):
            print "args:", args
            print "kwargs:", kwargs

        x('hello')
        args: hello
        kwargs: {'name': 'test_event', 'event': <Event object at 0x00000000026892E8>}

        x('world')
        args: world
        kwargs: {'name': 'test_event', 'event': <Event object at 0x00000000026892E8>}

    '''

    def __init__(self, **data):
        self._Handlers = set()
        '''Set list of handlers callables. Use a set to avoid multiple calls on one handler'''
        self.Data = data
        self.Data['event'] = self

    def _addHandler(self, handler):
        '''
        Add a handler callable. Raises a ValueError if the argument is not callable
        '''
        wr = WeakMethod(handler)

        self._Handlers.add(wr)
        return self

    def _removeHandler(self, handler):
        '''
        Remove a handler. Ignores handlers that are not present.
        '''
        wr = WeakMethod(handler)
        delenda = [h for h in self._Handlers if h == wr]
        self._Handlers = self._Handlers.difference(set(delenda))
        return self

    def metadata(self, kwargs):
        '''
        returns the me
        '''
        md = {}
        md.update(self.Data)
        md.update(kwargs)
        return md

    def _fire(self, *args, **kwargs):
        '''
        Call all handlers.  Any decayed references will be purged.
        '''

        delenda = []
        for handler in self._Handlers:
            try:
                handler(*args, **self.metadata(kwargs))
            except DeadReferenceError:
                delenda.append(handler)
        self._Handlers = self._Handlers.difference(set(delenda))

    def _handlerCount (self):
        '''
        Returns the count of the _Handlers field
        '''
        return len([i for i in self._Handlers])

    # hook up the instance methods to the base methods
    # doing it this way allows you to override more neatly
    # in derived classes
    __call__ = _fire
    __len__ = _handlerCount
    __iadd__ = _addHandler
    __isub__ = _removeHandler


class MayaEvent(Event):
    '''
    Subclass of event that uses Maya.utils.executeDeferred.
    '''
    def _fire(self, *args, **kwargs):
        '''
        Call all handlers.  Any decayed references will be purged.
        '''

        delenda = []
        for handler in self._Handlers:
            try:
                maya.utils.executeDeferred(partial(handler, *args, **self.metadata(kwargs)))
            except DeadReferenceError:
                delenda.append(handler)
        self._Handlers = self._Handlers.difference(set(delenda))

    __call__ = _fire


class DeadReferenceError(TypeError):
    '''
    Raised when a WeakMethodBound or WeakMethodFree tries to fire a method that
    has been garbage collected. Used by Events to know when to drop dead
    references
    '''
    pass

# # create weak references to both bound and unbound methods
# # hat tip to  Frederic Jolliton on ActiveState


class WeakMethodBound:
    '''
    Encapsulates a weak reference to a bound method on an object.  Has a
    hashable ID so that Events can identify multiple references to the same
    method and not duplicate them
    '''
    def __init__(self, f):

        self.f = f.im_func
        self.c = weakref.ref(f.im_self)
        self.ID = id(f.im_self) ^ id(f.im_func.__name__)

    def __call__(self, *arg, **kwarg):
        ref = self.c()
        if not ref is False and not ref is None:
            return apply(self.f, (self.c(),) + arg, kwarg)
        else:
            raise DeadReferenceError

    def __eq__(self, other):
        if not hasattr(other, 'ID'):
            return False
        return self.ID == other.ID

    def __hash__(self):
        return self.ID


class WeakMethodFree:
    '''
    Encapsulates a weak reference to an unbound method
    '''
    def __init__(self, f):
        self.f = weakref.ref(f)
        self.ID = id(f)

    def __call__(self, *arg, **kwarg) :
        if self.f():
            return apply(self.f(), arg, kwarg)
        else:
            raise DeadReferenceError

    def __eq__(self, other):
        if not hasattr(other, 'ID'): return False
        return self.ID == other.ID

    def __hash__(self):
        return self.ID


def WeakMethod(f) :
    '''
    Returns a WeakMethodFree or a WeakMethodBound for the supplied function, as
    appropriate
    '''
    try :
        f.im_func
    except AttributeError :
        return WeakMethodFree(f)
    return WeakMethodBound(f)
