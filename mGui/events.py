'''
events.py

Defines a simple event handler system similar to that used in C#.
'''
import weakref
import inspect
import maya.utils
from functools import wraps, partial

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

    Handlers must exhibit the *args, **kwargs signature.  It's the handler's job to decide what to do with them but they will be passed.  Use the Trigger object to add a dummy args/kwargs wrapper to a callable which takes no arguments
    '''

    def __init__( self, **data):
        self._Handlers = set()
        '''Set list of handlers callables. Use a set to avoid multiple calls on one handler'''
        self.Data = data
        self.Data['event'] = self
        
    def _addHandler( self, handler ):
        '''
        Add a handler callable. Raises a ValueError if the argument is not callable
        '''
       
        self._Handlers.add( WeakMethod(handler) )
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
        d = {}
        d.update(self.Data)
        d.update(**kwargs)
        
        delenda = []
        for handler in self._Handlers:
            try:
                handler( *args, **d )
            except DeadReferenceError:
                delenda.append(handler)
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
            try:
                h = handler()
                maya.utils.executeDeferred( h,  *args, **kwargs )
            except DeadReferenceError:
                delenda.append(handler)
           
                
        self._Handlers = self._Handlers.difference(set(delenda))

    __call__ = _fire

class DeadReferenceError(TypeError):
    pass

## create weak references to both bound and unbound methods
## recipce c/o Frederic Jolliton 

class WeakMethodBound :
    def __init__( self , f ) :
        
        self.f = f.im_func
        self.c = weakref.ref( f.im_self )
        
    def __call__( self , *arg, **kwarg ) :
        if self.c():
            return apply( self.f , ( self.c() , ) + arg, kwarg )
        else:
            raise DeadReferenceError
        
class WeakMethodFree :
    def __init__( self , f ) :
        self.f = weakref.ref( f )
    def __call__( self , *arg , **kwarg) :
        if self.f():
            return apply( self.f() , arg , kwarg)
        else:
            raise DeadReferenceError

def WeakMethod( f ) :
    try :
        f.im_func
    except AttributeError :
        return WeakMethodFree( f )
    return WeakMethodBound( f )
