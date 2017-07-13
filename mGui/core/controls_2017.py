from itertools import count

import maya.cmds as cmds

from mGui.core import Nested
from mGui.bindings import BindingContext


__all__ = ['WorkspaceControl']


class WorkspaceControl(Nested):
    '''Wrapper class for cmds.workspaceControl'''
    CMD = cmds.workspaceControl
    _ATTRIBS = ['restore', 'dockToPanel', 'tabPosition', 'initialHeight', 'widthProperty', 'requiredControl',
                'close', 'tabToControl', 'floating', 'stateString', 'r', 'dockToMainWindow',
                'uiScript', 'label', 'checksPlugins', 'initialWidth', 'minimumWidth', 'collapse',
                'requiredPlugin', 'dockToControl', 'horizontal', 'heightProperty', 'loadImmediately', 'duplicatable']
    _CALLBACKS = ['initCallback']

    def __init__(self, key=None, **kwargs):
        if key is None:
            for i in count(1):
                key = 'WorkspaceControl{!s}'.format(i)
                if not self.CMD(key, exists=True):
                    break
        super(WorkspaceControl, self).__init__(key, **kwargs)
        self.bindingContext = BindingContext()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def __enter__(self):
        self.bindingContext.__enter__()
        return super(WorkspaceControl, self).__enter__()

    def __exit__(self, typ, value, traceback):
        self.bindingContext.__exit__(None, None, None)
        mGui_expand_stack = True
        super(WorkspaceControl, self).__exit__(typ, value, traceback)

    def update_bindings(self):
        self.bindingContext.update(True)

    def forget(self, *args, **kwargs):
        super(WorkspaceControl, self).forget()
        self.bindingContext = None
