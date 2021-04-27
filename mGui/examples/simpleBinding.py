"""
Warning: If you give this layout less than one child there will be an error.
Example:
import mGui.examples.simpleBinding as simpleBinding
reload(simpleBinding)
example = simpleBinding.ExampleWindow()
example.settings
"""

import maya.cmds as cmds
from mGui import gui, forms
from mGui.bindings import bind


class ExampleWindow(object):
    settings = {"namespace": "Starting example, type here"}

    def __init__(self):
        with gui.Window(title="Example") as self.window:
            with forms.VerticalForm() as vf:
                self.thing = ExampleItem(self.settings)
                self.thing.field.update_bindings()
                poopy = gui.Button(label="print settings")
                poopy.command += self.query_settings

        self.window.show()

    def query_settings(self, *args, **kwargs):
        self.thing.field.update_bindings()
        print("self.settings ={!s}".format(self.settings))


class ExampleItem(object):
    def __init__(self, settings):
        self.settings = settings
        self.field = gui.TextField("namespace")
        self.field.bind.text | bind(lambda p: p or self.settings["namespace"]) | (
            self.settings,
            "namespace",
        )


if __name__ == "__main__":
    win = ExampleWindow()
