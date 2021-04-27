from itertools import count

from maya import cmds

from mGui.core import BindingWindow
from mGui.qt._compat import QtWidgets, QtCore, as_qt_object
from mGui.qt._properties import QtSignalProperty
from mGui.qt._mixins import QWidgetBaseMixin


class BaseDialog(QWidgetBaseMixin, QtWidgets.QDialog):
    """
    Simple wrapper around QtWidgets.QDialog.

    """

    closeEventTriggered = QtCore.Signal()
    windowStateChanged = QtCore.Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super(BaseDialog, self).__init__(parent, *args, **kwargs)
        template = "dialogWindow{}"
        for i in count(1):
            name = template.format(i)
            if not cmds.window(name, exists=True):
                self.setObjectName(name)
                break
        cmds.setParent(self)

    def resizeEvent(self, event):
        super(BaseDialog, self).resizeEvent(event)
        if event.isAccepted():
            self.windowStateChanged.emit()

    def moveEvent(self, event):
        super(BaseDialog, self).moveEvent(event)
        if event.isAccepted():
            self.windowStateChanged.emit()

    def closeEvent(self, event):
        super(BaseDialog, self).closeEvent(event)
        if event.isAccepted():
            self.closeEventTriggered.emit()


class DialogWindow(BindingWindow):
    """
    Integrates the QtWidgets.QDialog class with mGui.
    Should behave exactly like a BindingWindow with a few extra features.

    >>> from mGui import gui, forms
    >>> from mGui.qt.QDialog import DialogWindow
    >>>
    >>> with DialogWindow() as win:
    >>>     with forms.FooterForm() as base:
    >>>         with forms.FillForm() as main:
    >>>             text = gui.TextField()
    >>>
    >>>         with forms.HorizontalStretchForm() as footer:
    >>>             okay = gui.Button(label='Okay')
    >>>             cancel = gui.Button(label='Cancel')
    >>>
    >>>             okay.command += win.accept
    >>>             cancel.command += win.reject
    >>>
    >>>
    >>> def _accepted(*args, **kwargs):
    >>>     sender = kwargs['sender']
    >>>     print(sender.base.main.text.text)
    >>>
    >>> def _rejected(*args, **kwargs):
    >>>     print('Rejected!')
    >>>
    >>> win.accepted += _accepted
    >>> win.rejected += _rejected
    >>>
    >>> win.show()
    """

    closeEventTriggered = QtSignalProperty("closeEventTriggered")
    windowStateChanged = QtSignalProperty("windowStateChanged")

    accepted = QtSignalProperty("accepted")
    finished = QtSignalProperty("finished")
    rejected = QtSignalProperty("rejected")

    customContextMenuRequested = QtSignalProperty("customContextMenuRequested")
    windowIconChanged = QtSignalProperty("windowIconChanged")
    windowIconTextChanged = QtSignalProperty("windowIconTextChanged")
    windowTitleChanged = QtSignalProperty("windowTitleChanged")

    destroyed = QtSignalProperty("destroyed")
    objectNameChanged = QtSignalProperty("objectNameChanged")

    def __init__(self, key=None, **kwargs):
        self.__qt_object__ = BaseDialog()

        if key is not None:
            self.__qt_object__.setObjectName(key)

        retain = kwargs.pop("retain", kwargs.pop("ret", False))
        if not retain:
            self.__qt_object__.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        kwargs["title"] = kwargs.pop("title", kwargs.pop("t", self.__qt_object__.objectName()))
        kwargs["e"] = kwargs["edit"] = True
        super(DialogWindow, self).__init__(self.__qt_object__.objectName(), **kwargs)

    def show(self):
        self.__qt_object__.show()

    def hide(self):
        self.__qt_object__.hide()

    def accept(self, *args, **kwargs):
        return self.__qt_object__.accept()

    def reject(self, *args, **kwargs):
        return self.__qt_object__.reject()


class ModalDialogWindow(DialogWindow):
    """
    Dialog that blocks user input to the rest of system.

    >>> from mGui import gui, forms
    >>> from mGui.qt.QDialog import ModalDialogWindow
    >>>
    >>> with ModalDialogWindow() as win:
    >>>     with forms.FooterForm() as base:
    >>>         with forms.FillForm() as main:
    >>>             text = gui.TextField()
    >>>
    >>>         with forms.HorizontalStretchForm() as footer:
    >>>             okay = gui.Button(label='Okay')
    >>>             cancel = gui.Button(label='Cancel')
    >>>
    >>>             okay.command += win.accept
    >>>             cancel.command += win.reject
    >>>
    >>>
    >>> def _accepted(*args, **kwargs):
    >>>     sender = kwargs['sender']
    >>>     print(sender.base.main.text.text)
    >>>
    >>> def _rejected(*args, **kwargs):
    >>>     print('Rejected!')
    >>>
    >>> win.accepted += _accepted
    >>> win.rejected += _rejected
    >>>
    >>> win.show()
    """

    def __init__(self, key=None, **kwargs):
        super(ModalDialogWindow, self).__init__(key, **kwargs)
        self.modal = True

    def show(self, *args, **kwargs):
        return self.__qt_object__.exec_()
