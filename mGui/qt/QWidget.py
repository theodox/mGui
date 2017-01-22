
from ..core import BindingWindow

from maya import cmds
from maya.OpenMayaUI import MQtUtil

try:
    from shiboken import wrapInstance
    from PySide.QtGui import QWidget, QDialog
    from PySide import QtCore
except ImportError:
    from shiboken2 import wrapInstance
    from PySide2.QtWidgets import QWidget, QDialog
    from PySide2 import QtCore

class ModalWindow(BindingWindow):

    def __init__(self, *args, **kwargs):
        super(ModalWindow, self).__init__(*args, **kwargs)
        ptr = MQtUtil.findWindow(self.widget)
        self._qt_obj = wrapInstance(long(ptr), QWidget)
        self._qt_obj.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        

    def show(self):
        self._qt_obj.show()

    def forget(self, *args, **kwargs):
        super(ModalWindow, self).forget()
        self._qt_obj = None

    def hide(self):
        self._qt_obj.hide()

    def dismiss(self, *args, **kwargs):
        self.hide()
        cmds.deleteUI(self)

    def __exit__(self, typ, value, traceback):
        mGui_expand_stack = True
        super(ModalWindow, self).__exit__(typ, value, traceback)
