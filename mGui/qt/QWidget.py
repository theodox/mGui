
from ..core import BindingWindow

from maya.OpenMayaUI import MQtUtil

try:
    from shiboken import wrapInstance
    from PySide.QtGui import QWidget
    from PySide import QtCore
except ImportError:
    from shiboken2 import wrapInstance
    from PySide2.QtWidgets import QWidget
    from PySide2 import QtCore

class ModalWindow(BindingWindow):

    def __init__(self, *args, **kwargs):
        super(ModalWindow, self).__init__(*args, **kwargs)
        ptr = MQtUtil.findWindow(self.widget)
        self._qt_obj = wrapInstance(long(ptr), QWidget)
        self._qt_obj.setWindowModality(QtCore.Qt.WindowModality.WindowModal)

    def show(self):
        self._qt_obj.show()

    def forget(self):
        super(ModalWindow, self).forget()
        self._qt_obj = None

    def hide(self, *args, **kwargs):
        self._qt_obj.hide()
