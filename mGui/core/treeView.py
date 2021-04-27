from mGui.core.controls import TreeView
from mGui.events import Event
import maya.cmds as cmds


class TreeViewButtonProxy(object):
    """
    Enables MTreeView access to button callbacks
    """

    def __init__(self, parent, index):
        self.parent = parent
        self.index = index
        self.pressed = Event(button_index=index, tree_view=parent)
        self.rightPressed = Event(button_index=index, tree_view=parent)


class MTreeView(TreeView):
    """
    A wrapper for TreeViews which gets around some of the strange way Maya ties
    button commands to buttons in that control.  This version shares the same commands
    except that it an indirection for buttons so they can be accessed like this:

        treeview1.buttons[0].pressed += handler
    or
        treeview2.buttons[2].rightPressed -= handler
    """

    def __init__(self, key=None, **kw):
        super(TreeView, self).__init__(key=key, **kw)
        buttonCount = kw.get("numberOfButtons", 0)
        self.buttons = [TreeViewButtonProxy(self, n) for n in range(buttonCount)]
        for idx, btn in enumerate(self.buttons):
            cmds.treeView(self, e=True, pressCommand=(idx + 1, btn.pressed))
            cmds.treeView(self, e=True, rightPressCommand=(idx + 1, btn.rightPressed))

    def set_items(self, **tree):
        self.removeAll = True
        for kv in tree.items():
            self.addItem = kv
