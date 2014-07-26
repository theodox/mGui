'''
mGui.gui

forwards all of the widget definitions in the system for easy import.  This
module is probably safe to import * in a known context
'''

import copy

from mGui.core import Window, BindingWindow, ControlMeta
from mGui.core.layouts import *
from mGui.core.menus import *
from mGui.core.controls import *


"""
create a lookup table indexing all UI commands to their corresponding mGui classes
"""
__defined = locals()
__defined = copy.copy(__defined)
__lookup = {}

for k, v in __defined.items():
    if isinstance(v, ControlMeta):
        __lookup[v.CMD.__name__] = v

__lookup['floatingWindow'] = Window
__lookup['commandMenuItem'] = MenuItem


def _objectTypeUI(widget):
    '''
    objectTypeUI in maya 2011 does not reconize menuItems. This is a fix to that issue.
    '''
    if cmds.menuItem(widget, q=True, ex=True):
        widget_type = 'menuItem'
    else:
        widget_type = cmds.objectTypeUI(widget)

    return widget_type


def derive(widget):
    widget_type = _objectTypeUI(widget)

    result = __lookup[widget_type].wrap(widget)
    kids = []
    if isinstance(result, Window):
        all_layouts = cmds.lsUI(type='layout', l=True) or []
        kids = [ly for ly in all_layouts if ly.startswith(widget) and ly.count("|") == 1]
    if isinstance(result, Layout):
        kids = result.childArray or []
    if isinstance(result, Menu) or isinstance(result, PopupMenu):
        kids = result.itemArray or []
    if isinstance(result, OptionMenu):
        kids = result.itemListLong or []

    for k in kids:
        result.Controls.append(derive(k))

    return result
