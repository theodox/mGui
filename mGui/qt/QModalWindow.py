"""
Modal Window is a version of the Window class that blocks all input to other windows.
However it does not block code execution, so it does not behave like a standard dialog.

"""
from maya import cmds
from mGui.core import BindingWindow
from mGui.qt._compat import as_qt_object, QtCore

APPLICATION_MODAL = QtCore.Qt.WindowModality.ApplicationModal

class QModalWindow(BindingWindow):

    def __init__(self, *args, **kwargs):
        super(QModalWindow, self).__init__(*args, **kwargs)
        self.__qt_object__ = as_qt_object(self)
        self.__qt_object__.setWindowModality(APPLICATION_MODAL)

    def show(self):
        self.__qt_object__.show()

    def forget(self, *args, **kwargs):
        super(QModalWindow, self).forget()
        self.__qt_object__ = None

    def hide(self):
        self.__qt_object__.hide()

    def dismiss(self, *args, **kwargs):
        self.hide()
        cmds.deleteUI(self)

    def __exit__(self, typ, value, traceback):
        mGui_expand_stack = True
        super(QModalWindow, self).__exit__(typ, value, traceback)
