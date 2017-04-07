import weakref
from itertools import count

from maya import cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQDockWidget

from mGui.core import BindingWindow
from mGui.events import MayaEvent, Event
from mGui.qt._compat import QtWidgets, QtCore, as_qt_object
from mGui.qt._properties import QtSignalProperty


# class QtSignalProperty(object):
#     """
#     Similar to the compat libraries signal handling property.
#     Except rather tightly coupled to the the _Dialog class.

#     """

#     def __init__(self, key, event_class):
#         self._key = key
#         self._event_class = event_class

#     def __get__(self, obj, obj_type):
#         if obj is None:
#             return self
#         qt_object = obj._qt_object

#         cb = obj.callbacks.get(self._key, None)
#         if cb is None:
#             cb = obj.callbacks[self._key] = self._event_class(sender=weakref.proxy(obj), qWidget=qt_object)
#             getattr(qt_object, self._key).connect(cb)
#         return cb

#     def __set__(self, obj, value):
#         if obj.callbacks[self._key] != value:
#             qt_object = obj._qt_object
#             getattr(qt_object, self._key).disconnect(obj.callbacks[self._key])
#             obj.callbacks[self._key] = value
#             getattr(qt_object, self._key).connect(value)



class _Dialog(MayaQWidgetBaseMixin, QtWidgets.QDialog):

    """
    Simple wrapper around QtWidgets.QDialog.

    """
    closeEventTriggered = QtCore.Signal()
    windowStateChanged = QtCore.Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super(_Dialog, self).__init__(parent, *args, **kwargs)
        # I get the feeling I'll be using this pattern a lot.
        # Might want to make a helper method out of it.
        template = 'dialogWindow{}'
        for i in count(1):
            name = template.format(i)
            if not cmds.window(name, exists=True):
                self.setObjectName(name)
                break
        cmds.setParent(self)

    def __str__(self):
        return self.objectName().encode('utf-8')

    def __unicode__(self):
        return self.objectName()

    def resizeEvent(self, event):
        super(_Dialog, self).resizeEvent(event)
        if event.isAccepted():
            self.windowStateChanged.emit()

    def moveEvent(self, event):
        super(_Dialog, self).moveEvent(event)
        if event.isAccepted():
            self.windowStateChanged.emit()

    def closeEvent(self, evt):
        '''Hide the QDockWidget and trigger the closeEventTriggered signal
        '''
        # Handle the standard closeEvent()
        super(_Dialog, self).closeEvent(evt)
        if evt.isAccepted():
            # Force visibility to False
            self.setVisible(False)  # since this does not seem to have happened already

            # Emit that a close event is occurring
            self.closeEventTriggered.emit()

class DialogWindow(BindingWindow):

    """
    Integrates the QtWidgets.QDialog class with mGui.
    Should behave exactly like a BindingWindow with a few extra features.

    """
    
    # _Dialog
    closeEventTriggered = QtSignalProperty('closeEventTriggered')
    windowStateChanged = QtSignalProperty('windowStateChanged')

    # QDialog
    accepted = QtSignalProperty('accepted')
    finished = QtSignalProperty('finished')
    rejected = QtSignalProperty('rejected')

    # QObject
    customContextMenuRequested = QtSignalProperty('customContextMenuRequested')
    windowIconChanged = QtSignalProperty('windowIconChanged')
    windowIconTextChanged = QtSignalProperty('windowIconTextChanged')
    windowTitleChanged = QtSignalProperty('windowTitleChanged')

    # QObject
    destroyed = QtSignalProperty('destroyed')
    objectNameChanged = QtSignalProperty('objectNameChanged')

    def __init__(self, key=None, **kwargs):
        self._qt_object = _Dialog()
        if key is not None:
            self._qt_object.setObjectName(key)

        kwargs['title'] = kwargs.pop('title', kwargs.pop('t', self._qt_object.objectName()))
        kwargs['e'] = kwargs['edit'] = True
        super(DialogWindow, self).__init__(self._qt_object.objectName(), **kwargs)

    def show(self):
        self._qt_object.show()

    def forget(self, *args, **kwargs):
        super(DialogWindow, self).forget()
        self.bindingContext = None
        try:
            self._qt_object.deleteLater()
        except RuntimeError as e:
            pass

    def hide(self):
        self._qt_object.hide()


class ModalDialogWindow(DialogWindow):
    # _Dialog
    closeEventTriggered = QtSignalProperty('closeEventTriggered')
    windowStateChanged = QtSignalProperty('windowStateChanged')
    
    # QDialog
    accepted = QtSignalProperty('accepted')
    finished = QtSignalProperty('finished')
    rejected = QtSignalProperty('rejected')
    
    # QWidget
    customContextMenuRequested = QtSignalProperty('customContextMenuRequested')
    windowIconChanged = QtSignalProperty('windowIconChanged')
    windowIconTextChanged = QtSignalProperty('windowIconTextChanged')
    windowTitleChanged = QtSignalProperty('windowTitleChanged')

    # QObject
    destroyed = QtSignalProperty('destroyed')
    objectNameChanged = QtSignalProperty('objectNameChanged')
    
    def show(self):
        return self._qt_object.exec_()

    def __init__(self, key=None, **kwargs):
        self.modal = True
        super(ModalDialogWindow, self).__init__(key, **kwargs)