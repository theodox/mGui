'''
Warning: If you give this layout less than one child there will be an error.
Example:
import mGui.examples.simpleBinding as simpleBinding
reload(simpleBinding)
example = simpleBinding.window_object()
example.settings
'''

import maya.cmds as cmds
import mGui.gui as gui
import mGui.forms as forms
from mGui.bindings import bind


class window_object(object):
    settings = {'namespace': 'Starting example, type here'}

    def __init__(self):
        with gui.Window(None, title="Example") as window:
            with forms.VerticalForm(None):
                self.thing1 = testItem(self.settings)
                self.thing1.field.proxy_update()
                gui.Button('poopy', label='print settings').command += self.query_settings

        cmds.showWindow(window)

    def query_settings(self, *args, **kwargs):
        self.thing1.field.proxy_update()
        print 'self.settings =', self.settings


class testItem(object):

    def __init__(self, settings):
        self.settings = settings
        self.field = gui.TextField('namespace').bind.text | bind(lambda p: p or self.settings['namespace']) | (self.settings, 'namespace')
