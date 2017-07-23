"""
ModuleManager.py

An example showing data bound collection UI.  The module files on disk are
collected and managed by the ModuleManager class, which is purely functional and
has no UI.  

The UI contains a list which is bound to the ModuleManager's collection of
mofTuple objects; the list displays the available modules as widgets (created
using the the ModuleTemplate clas).  

The widgets are directly bound to the ModTuple variables; this means that
closing the dialog checks the state of the list and updates the files on disk as
needed. You'll notice there is no checking the state of the UI widgets: the
values inside the ModuleManager are updated by the bindings using the update_status method.

Some other points of note:

Tags
----
The widgets use the Tag property to make sure that each widget knows what
object to work on without extra lambdas or partials 

LayoutDialogForm
---------------
The root of the UI is a LayoutDialogForm;  a convenience class which takes the existing
formLayout created by Maya's layoutDialog command and wraps it with an mGui Layout so that
it can be edited like other mGui widgets.

BindingContext
--------------
The BindingContext in the UI catches all of the bindings created while it's active and updates
them automatically when it closes; this makes sure that all the UI elements get set properly
at creation time.

"""
import sys

import maya.cmds as cmds

import os
import subprocess
import webbrowser as wb
from mGui import gui, lists, forms
from mGui.bindings import bind, BindingContext


# Mod manager classes
# ==============================================================================================

class ModTuple(object):
    """
    Represents a module file on disk
    """

    def __init__(self, enabled, name, version, path, filename):
        self.enabled = enabled
        self.name = name
        self.version = version
        self.path = path
        self.file = filename


class ModuleManager(object):
    """
    Manages the list of .mod files on the local maya's MAYA_MODULE_PATH.

    Note this class is purely functional - UI is handled in the ModuleManagerDialog via binding.
    """

    def __init__(self):
        self.modules = {}
        self.refresh()

    def refresh(self):
        """
        Update the internal module list to reflect the state of files on disk
        """
        self.modules.clear()
        module_files = []
        module_paths = os.environ['MAYA_MODULE_PATH'].split(os.pathsep)
        for p in module_paths:
            try:
                module_files += [os.path.join(p, x).replace(os.sep, os.altsep or os.sep) for x in os.listdir(p) if
                                 x.lower()[-3:] == "mod"]
            except OSError:
                pass  # ignore bad paths
        for eachfile in module_files:
            for eachmod in self.parse_mod(eachfile):
                self.modules["{0.name} ({0.version})".format(eachmod)] = eachmod

    def parse_mod(self, modfile):
        """
        Yields a modtuple describing the supplied .mod file
        """
        with open(modfile, 'rt') as filehandle:
            for line in filehandle:
                if line.startswith(("+", "-")):
                    enable, name, version, path = self.parse_mod_entry(line)
                    yield ModTuple(enable == "+", name, version, path, modfile)

    def parse_mod_entry(self, line):
        """
        parses a line from a mod file describing a given mod
        module description format:
            enabled [LOCALE:val] [PLATFORM:plat] [MAYAVERSION:version] name version path

        Flags within [] are optional, and can be in any order.
        Currently all optional flags are ignored.
        """
        split_line = line.split(' ')
        enable = split_line.pop(0)
        path = split_line.pop()
        version = split_line.pop()
        name = split_line.pop()
        return enable, name, version, path

    def enable(self, modtuple):
        self._rewrite_mod(modtuple, '+')

    def disable(self, modtuple):
        self._rewrite_mod(modtuple, '-')

    def _rewrite_mod(self, modtuple, character):
        all_lines = []
        with open(modtuple.file, 'rt') as filehandle:
            for line in filehandle:
                enable, name, version, path = self.parse_mod_entry(line)
                if name == modtuple.name and version == modtuple.version:
                    line = character + line[1:]
                all_lines.append(line)
        with open(modtuple.file, 'wt') as filehandle:
            filehandle.write('\n'.join(all_lines))


# GUI classes
# ======================================
class ModuleTemplate(lists.ItemTemplate):
    """
    Create a complex display widget for each ModTuple
    """

    def widget(self, item):
        with BindingContext() as bc:
            with forms.HorizontalExpandForm(height=60, margin=(12, 0), backgroundColor=(.2, .2, .2)) as root:
                with forms.VerticalExpandForm(width=60) as cbf:
                    enabled = gui.CheckBox(label='', tag=item, value=item.enabled)
                    enabled.bind.value > bind() > (item, 'enabled')
                    cbf.dock(enabled, left=20, top=10, bottom=40, right=5)
                with forms.FillForm(width=300) as path:
                    with gui.ColumnLayout() as cl:
                        display_name = gui.Text(font='boldLabelFont')
                        display_name.bind.label < bind() < (item, 'name')
                        path = gui.Text(font='smallObliqueLabelFont')
                        path.bind.label < bind() < (item, 'path')
                with gui.GridLayout(width=200, numberOfColumns=2) as btns:
                    edit = gui.Button(label='Edit', tag=item)
                    show = gui.Button(label='Show', tag=item)
        enabled.changeCommand += self.update_status
        show.command += self.show_item
        edit.command += self.edit

        return lists.Templated(item, root, edit=edit.command, show=show.command)

    @classmethod
    def update_status(cls, *args, **kwargs):
        kwargs['sender'].update_bindings()

    @classmethod
    def show_item(cls, *args, **kwargs):
        wb.open(os.path.dirname(kwargs['sender'].tag.file))

    @classmethod
    def edit(cls, *args, **kwargs):
        try:
            os.startfile(kwargs['sender'].tag.file)
        except OSError:
            if sys.platform.startswith('win'):
                subprocess.call(['notepad', kwargs['sender'].tag.file])
            else:
                subprocess.call(['vi', kwargs['sender'].tag.file])


class ModuleManagerDialog(object):
    """
    Module manager dialog, implemented via LayoutDialog
    """

    def __init__(self):
        self._manager = ModuleManager()
        self._manager.refresh()

    def _layout(self):
        with forms.LayoutDialogForm() as base:
            with BindingContext() as bc:
                with forms.VerticalThreePane(width=512, margin=(4, 4), spacing=(0, 8)) as main:
                    with forms.VerticalForm() as header:
                        gui.Text(label='Installed Modules')

                    with forms.FillForm() as body:
                        mod_list = lists.VerticalList(itemTemplate=ModuleTemplate)
                        mod_list.collection < bind() < (self._manager.modules, 'values')
                        # binds the 'values' method of the ModuleManager's modules{} dictionary

                    with forms.HorizontalStretchForm() as footer:
                        cancel = gui.Button(label='Cancel')
                        cancel.command += self._cancel
                        gui.Separator(style=None)
                        save = gui.Button(label='Save')
                        save.command += self._save

        base.fill(main, 5)
        mod_list.update_bindings()

    def _cancel(self, *args, **kwargs):
        cmds.layoutDialog(dismiss="dismiss")

    def _save(self, *args, **kwargs):
        for v in self._manager.modules.values():
            if v.enabled:
                self._manager.enable(v)
            else:
                self._manager.disable(v)
        cmds.layoutDialog(dismiss="OK")

    def show(self):
        self._manager.refresh()
        cmds.layoutDialog(ui=self._layout, title='Module editor')


if __name__ == '__main__':
    m = ModuleManagerDialog()
    m.show()
