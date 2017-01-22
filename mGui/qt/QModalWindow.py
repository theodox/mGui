"""
Modal Window is a version of the Window class that blocks all input to other windows.
However it does not block code execution, so it does not behave like a standard dialog.


"""
from maya import cmds
from mGui.core import BindingWindow
from mGui.qt._compat import as_qt_object, QtCore


class QModalWindow(BindingWindow):

    def __init__(self, *args, **kwargs):
        super(QModalWindow, self).__init__(*args, **kwargs)
        self._qt_obj = as_qt_object(self)
        self._qt_obj.setWindowModality(
            QtCore.Qt.WindowModality.ApplicationModal)

    def show(self):
        self._qt_obj.show()

    def forget(self, *args, **kwargs):
        super(QModalWindow, self).forget()
        self._qt_obj = None

    def hide(self):
        self._qt_obj.hide()

    def dismiss(self, *args, **kwargs):
        self.hide()
        cmds.deleteUI(self)

    def __exit__(self, typ, value, traceback):
        mGui_expand_stack = True
        super(QModalWindow, self).__exit__(typ, value, traceback)
