__author__ = 'Steve'

import time

from mGui.core.controls import TextField
from mGui.events import Event
from mGui.scriptJobs import Idle
from mGui.qt._compat import as_qt_object, QtCore
from mGui.qt.properties import QtSignalPropety


class InputBuffer(object):

    '''
    accumulate inputs until a certain amount of time passes
    '''

    def __init__(self, parent, fn, interval=1):
        self.last = time.time()
        self.interval = interval
        self.fn = fn
        self.buffer = []
        self.idleEvent = Idle()
        self.idleEvent += self.update
        self.idleEvent.start(p=parent)
        self.previous_value = None

    def handle(self, *args, **_):
        self.buffer.append(args[0])

    def update(self, *_, **__):
        if time.time() - self.last < self.interval:
            return
        
        if self.buffer:
            previous = self.previous_value
            self.previous_value = self.buffer[-1]
            if self.previous_value != previous:
                self.fn(self.previous_value)
                self.buffer = []
        self.last = time.time()


class QTextField(TextField):

    """
    A wrapper around the QTextEdit in a Maya TextField.  The main difference is that it
    can emit events on every text change
    """

    textChanged = QtSignalPropety('textChanged')

    def __init__(self, key=None, **kwargs):
        interval = kwargs.pop('interval', .25)
        super(QTextField, self).__init__(key, **kwargs)

        self.textBufferChanged = None
        self._qt_wrapper = as_qt_object(self.widget)
        self.buffer = None
        self.keypress = Event()

        # this is unduly specific for a simple application
        # should be generalized
        fire_event = self.keypress
        special_keys = {
            16777235: 'up',
            16777237: 'down',
            16777220: 'enter',
            16777217: 'tab',
            16777216: 'esc'
        }
        # -------------------------

        class KeypressFilter(QtCore.QObject):

            def eventFilter(self, obj, event):
                if event.type() == QtCore.QEvent.KeyPress:
                    key_val = event.key()
                    if key_val in special_keys:
                        fire_event(special_keys[key_val])
                        return True
                return False

        self._qt_wrapper.installEventFilter(KeypressFilter(self._qt_wrapper))

        if interval:
            self.textBufferChanged = Event(**{'sender': self})
            self.buffer = InputBuffer(self, self.textBufferChanged)
            self.textChanged += self.buffer.handle

    
    