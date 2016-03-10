__author__ = 'Steve'
from maya.OpenMayaUI import MQtUtil
from shiboken import wrapInstance
from PySide.QtGui import QTextEdit
from PySide import QtCore

from mGui.core.controls import TextField
from mGui.properties import CallbackProperty
from mGui.events import Event


def hook_text_changed_event(maya_text_field, event):
    ptr = MQtUtil.findControl(maya_text_field)
    qt_wrapper = wrapInstance(long(ptr), QTextEdit)
    signal = QtCore.SIGNAL("textChanged(const QString&)")
    qt_wrapper.connect(signal, event)
    return qt_wrapper


class QTextField(TextField):
    def __init__(self, key=None, **kwargs):
        super(QTextField, self).__init__(key, **kwargs)
        self.textChanged = Event()
        self._qt_wrapper = hook_text_changed_event(self.widget, self.textChanged)
        self.textChanged.data['qWidget'] = self._qt_wrapper

'''
    @property
    def html(self):
        return self._qt_wrapper.toHtml()

    @html.setter
    def set_html(self, val):
        self._qt_wrapper.setHtml(val)
'''