"""
Defines a descriptor object for binding Qt Signals to mGui objects.

"""

from mGui.events import Event, MayaEvent
from mGui.qt._compat import as_qt_object
import weakref


class QtSignalProperty(object):
    """
    Property descriptor for Qt Signals.  When accessed, returns the appropriate
    Event object from a Control-derived class's Callback dictionary.

    By default, this will create a new MayaEvent (so evalDeferred safe) if
    you have not created an event manually, so:

    button.command += doSomething
    button.command -= doSomething

    However you can also create events manually and parameterize them

    button.command = events.MayaEvent(target = 'pCube1', distance = 2.0)

    """

    def __init__(self, key):
        self._key = key

    def __get__(self, obj, obj_type):
        if obj is None:
            return self
        qt_object = as_qt_object(obj)

        cb = obj.callbacks.get(self._key, None)
        if cb is None:
            if obj.modal or obj.parent and obj.parent.modal:
                cb = obj.callbacks[self._key] = Event(sender=weakref.proxy(obj), qWidget=qt_object)
            else:
                cb = obj.callbacks[self._key] = MayaEvent(sender=weakref.proxy(obj), qWidget=qt_object)
            getattr(qt_object, self._key).connect(cb)
        return cb

    def __set__(self, obj, value):
        if obj.callbacks[self._key] != value:
            qt_object = as_qt_object(obj)
            getattr(qt_object, self._key).disconnect(obj.callbacks[self._key])
            obj.callbacks[self._key] = value
            getattr(qt_object, self._key).connect(value)
