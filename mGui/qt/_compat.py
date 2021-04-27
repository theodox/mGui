"""
Internal module for providing a consistent interface for the various Qt Bindings.
The basic goal is allow mGui to just treat Qt elements as if we were writing against PySide2.
But we provide fallbacks to other bindings.

"""

from maya.OpenMayaUI import MQtUtil


def _find_widget_ptr(widget):
    ptr = MQtUtil.findControl(widget) or MQtUtil.findLayout(widget) or MQtUtil.findMenuItem(widget)
    return ptr


def _pyside2_as_qt_object(widget):
    from PySide2.QtCore import QObject
    from PySide2.QtWidgets import QWidget
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance

    if hasattr(widget, "__qt_object__"):
        return widget.__qt_object__
    ptr = _find_widget_ptr(widget)
    qobject = wrapInstance(int(ptr), QObject)
    meta = qobject.metaObject()
    _class = meta.className()
    _super = meta.superClass().className()
    qclass = getattr(QtWidgets, _class, getattr(QtWidgets, _super, QWidget))
    return wrapInstance(int(ptr), qclass)


def _pyside_as_qt_object(widget):
    from PySide.QtCore import QObject
    from PySide.QtGui import QWidget
    from PySide import QtGui
    from shiboken import wrapInstance

    if hasattr(widget, "__qt_object__"):
        return widget.__qt_object__
    ptr = _find_widget_ptr(widget)
    qobject = wrapInstance(int(ptr), QObject)
    meta = qobject.metaObject()
    _class = meta.className()
    _super = meta.superClass().className()
    qclass = getattr(QtGui, _class, getattr(QtGui, _super, QWidget))
    return wrapInstance(int(ptr), qclass)


def _pyqt4_as_qt_object(widget):
    from sip import wrapinstance

    # Seting to api level 2 to better align with PySide behavior.
    sip.setapi("QDate", 2)
    sip.setapi("QDateTime", 2)
    sip.setapi("QString", 2)
    sip.setapi("QtextStream", 2)
    sip.setapi("Qtime", 2)
    sip.setapi("QUrl", 2)
    sip.setapi("QVariant", 2)
    from PyQt4.QtGui import QWidget

    if hasattr(widget, "__qt_object__"):
        return widget.__qt_object__
    ptr = _find_widget_ptr(widget)
    return wrapinstance(int(ptr), QWidget)


def _pyqt5_as_qt_object(widget):
    from PyQt5.QtWidgets import QWidget
    from sip import wrapinstance

    if hasattr(widget, "__qt_object__"):
        return widget.__qt_object__
    ptr = _find_widget_ptr(widget)
    return wrapinstance(int(ptr), QWidget)


def _pyside2_load_ui(fyle, parent=None):
    from PySide2.QtUiTools import QUiLoader

    loader = QUiLoader()
    return loader.load(fyle, parent)


def _pyside_load_ui(fyle, parent=None):
    from PySide.QtUiTools import QUiLoader

    loader = QUiLoader()
    return loader.load(fyle, parent)


def _pyqt5_load_ui(fyle, parent=None):
    from PyQt5 import uic

    return uic.loadUi(fyle, parent)


def _pyqt4_load_ui(fyle, parent=None):
    from PyQt4 import uic

    return uic.loadUi(fyle, parent)


# Imports favor PySide over PyQt, and Qt5 over Qt4.
# as this is the most future forward set of options currently.
try:
    from PySide2 import QtCore, QtGui, QtWidgets
except ImportError:
    try:
        from PySide import QtCore, QtGui

        QtWidgets = QtGui
    except ImportError:
        try:
            from PyQt5 import QtCore, QtGui, QtWidgets
        except ImportError:
            try:
                from PyQt4 import QtCore, QtGui

                QtWidgets = QtGui
            except ImportError:
                pass
            else:
                as_qt_object = _pyqt4_as_qt_object
                load_ui = _pyqt4_load_ui
        else:
            as_qt_object = _pyqt5_as_qt_object
            load_ui = _pyqt5_as_qt_object
    else:
        as_qt_object = _pyside_as_qt_object
        load_ui = _pyside_load_ui
else:
    as_qt_object = _pyside2_as_qt_object
    load_ui = _pyside2_load_ui


def main_window():
    return as_qt_object("MayaWindow")


__all__ = ["QtCore", "QtGui", "QtWidgets", "main_window", "as_qt_object", "load_ui"]
