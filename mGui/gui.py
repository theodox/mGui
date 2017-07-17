"""
mGui.gui

forwards all of the widget definitions in the system for easy import.  This
module is probably safe to import * in a known context
"""

from mGui.core import Window, BindingWindow,  Control, REGISTRY, MAYA_VERSION
from mGui.core.menus import *
from mGui.core.controls import *
from mGui.core.layouts import *
from mGui.core.panels import  *
from mGui.core.editors import *
from mGui.core.treeView import MTreeView
from mGui.core.progress import ProgressBar

import warnings

# conditional imports for api additions
if MAYA_VERSION >= '2017':
    from mGui.core.controls_2017 import *



from mGui.events import event_handler

"""
create a lookup table indexing all UI commands to their corresponding mGui classes
"""


def _collect_mappings():
    """
    Iterate over the results of cmds.objectTypeUI(listAll=True) which lists the
    three names for every UI object type. Unfortunately they don't match exactly to the
    maya.cmds names, so this does its best to find the corresponding mGui wrapper based
    on the best fit of either the UI name or the mystery name returned by objectTypeUI.

    The goal is to create a mapping between objectTypeUI types and mGui types.  However this won't be
    100% accurate until ADSK unifies the cmds names and the results of objectTypeUI
    """
    accum = []
    for c, e in enumerate(cmds.objectTypeUI(listAll=True), 1):
        if c % 3 != 0:
            accum.append(e)
        else:
            key = accum[1]
            val = REGISTRY.get(accum[0], REGISTRY.get(accum[1]))
            yield (key, val)
            accum = []


_type_mappings = dict(_collect_mappings())
del _collect_mappings


def wrap(control, replace_events=False):
    """
    return an mGui proxy for <control>, using the string returned by  cmds.objectTypeUI() to figure out
    the correct wrapper class.  This should work for almost all common cases but there are some controls
    where Maya returns string types which can't be matched to the maya.cmds functions which mGui uses.

    If 'replace events' is true, the procedure will try to convert any existing callback handlers to mGui style
    event handlers.  This will only work properly for straightforward Python callbacks (mel is _not_ supported
    at this time).
    """
    target_class = _type_mappings.get(cmds.objectTypeUI(control))
    if not target_class:
        return Control.wrap(control, cmds.objectTypeUI(control))

    result = target_class.wrap(control)
    if replace_events:
        for cb in target_class._CALLBACKS or []:
            handler = target_class.CMD(control, **{'q': True, cb: True})
            if handler and callable(handler):
                setattr(result, cb, event_handler(handler))

    if hasattr(result, 'childArray'):
        for item in result.childArray:
            result.add(wrap(item))

    if hasattr(result, 'menuArray'):
        for item in result.menuArray:
            result.add(wrap(item))

    if hasattr(result, 'popupMenuArray'):
        for item in result.popupMenuArray:
            result.add(wrap(item))

    if target_class is Window or target_class is BindingWindow:
        window_children = [i for i in cmds.lsUI(controlLayouts=True, l=True) if str(i).startswith(control)]
        if window_children:
            window_children.sort()
            result.add(wrap(window_children[0]))

    return result


def derive(control):
    """
    gui.derive will be removed after mGui 2.2; for now it's going to issue a deprecation warning and call `wrap()`
    """
    warnings.warn("gui.derive() should be replaced by gui.wrap()", PendingDeprecationWarning)
    return wrap(control)