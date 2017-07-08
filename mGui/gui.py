"""
mGui.gui

forwards all of the widget definitions in the system for easy import.  This
module is probably safe to import * in a known context
"""

from mGui.core.controls import *
from mGui.core.layouts import *
from mGui.core.menus import *
from mGui.core.progress import ProgressBar, MainProgressBar
from mGui.core.treeView import MTreeView
from mGui.core import Window, Control, Layout, REGISTRY


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
    for c, e in enumerate(cmds.objectTypeUI(listAll=True)):
        c += 1
        if c % 3 != 0:
            accum.append(e)
        else:
            key = accum[1]
            val = REGISTRY.get(accum[0], REGISTRY.get(accum[1]))
            yield (key, val)
            accum = []


_type_mappings = dict(_collect_mappings())
del _collect_mappings

def wrap(control):
    target_class = _type_mappings .get(cmds.objectTypeUI(control))
    result = None
    if not target_class:
        result = Control.wrap(control)

    result = target_class.wrap(control)
    if hasattr(result, 'childArray'):
        for item in result.childArray:
            result.add(wrap(item))
    return result
