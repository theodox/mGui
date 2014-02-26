'''
events.py

Defines a simple event handler system similar to that used in C#.
'''
import weakref
import inspect
import maya.utils

class Event( object ):
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

    Handlers must exhibit the *args, **kwargs signature.  It's the handler's job to decide what to do with them but they will be passed.  Use the Notification object to add a dummy args/kwargs wrapper to a callable which takes no arguments
    '''

    def __init__( self ):
        self._Handlers = set()
        '''Set list of handlers callables. Use a set to avoid multiple calls on one handler'''

    def _addHandler( self, handler ):
        '''
        Add a handler callable. Raises a ValueError if the argument is not callable
        '''
        if not callable( handler ): raise ValueError( "Handler argument must be callable" )

        code = handler
        if hasattr(code, '__call__') and not inspect.isfunction(code):
            code = handler.__call__

        argspec = inspect.getargspec(code)
        if (not argspec.varargs or not argspec.keywords):
                raise ValueError( "Handler argument must accept *args and **keywordArgs" )
        self._Handlers.add( weakref.ref(handler) )
        return self

    def _removeHandler( self, handler ):
        '''
        Remove a handler. Ignores handlers that are not present.
        '''
        delenda = []
        for h in self._list_handlers():
            if h() == handler:
                delenda.append(h)
        self._Handlers = self._Handlers.difference(set(delenda))
        return self

    def _fire( self, *args, **kwargs ):
        '''
        Call all handlers.  Any decayed references will be purged.
        '''
        kwargs['event'] = self
        delenda = []
        for handler in self._Handlers:
            h = handler()
            if h:
                h( *args, **kwargs )
            else:
                delenda.append(h)
        self._Handlers = self._Handlers.difference(set(delenda))

    def _handlerCount ( self ):
        '''
        Returns the count of the _Handlers field
        '''
        return len( [i for i in self._list_handlers()] )

    def _list_handlers( self ):
        for item in self._Handlers: 
            if item(): yield item()
                

    # hook up the instance methods to the base methods
    # doing it this way allows you to override more neatly
    # in derived classes
    __call__ = _fire
    __len__ = _handlerCount
    __iadd__ = _addHandler
    __isub__ = _removeHandler
    __iter__ = _list_handlers


class MayaEvent(Event):
    '''
    Subclass of event that uses Maya.utils.executeDeferred
    '''
    def _fire( self, *args, **kwargs ):
        '''
        Call all handlers.  Any decayed references will be purged.
        '''
        kwargs['event'] = self
        delenda = []
        for handler in self._Handlers:
            h = handler()
            if h:
                maya.utils.executeDeferred( h,  *args, **kwargs )
            else:
                delenda.append(h)
        self._Handlers = self._Handlers.difference(set(delenda))

    __call__ = _fire




class Notification(object):
    '''
    wrapper for callables that don't present the *args, **kwargs signature

    Calls the function when the event fires, but swallows any args or kwargs
    '''
    def __init__(self, callable):
        self.callable = callable

    def __call__(self, *args, **kwargs):
        self.callable()
            