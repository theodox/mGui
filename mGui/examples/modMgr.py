
"""
ModuleManager.py

An example showing data bound collection UI.  The module files on disk are
collected and managed by the ModuleManager class, which is purely functional and
has no UI.  

The UI contains a list which is bound to the ModuleManager's collection of
mofTuple objects; the list displays the available modules as widgets (created
using the the ModuleTemplate clas).  

The widgets are directly bound to the modTuple variables; this means that
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
import mGui.gui as gui
import mGui.lists as lists
import mGui.observable as observable
import mGui.forms as forms
import mGui.styles 
from mGui.bindings import bind, BindingContext
import itertools
import maya.cmds as cmds
import os
import maya.mel
import webbrowser as wb

# Mod manager classes
#==============================================================================================

class modTuple(object):
    """
    Represents a module file on disk
    """
    def __init__(self, enabled, name, version, path, filename):
        self.enabled = enabled
        self.name = name
        self.version = version
        self.path = path
        self.file = filename


class ModuleManager (object):
    """
    Manages the list of .mod files on the local maya's MAYA_MODULE_PATH.
    
    Note this class is purely functional - UI is handled in the ModuleManagerDialog via binding.
    """
    def __init__(self):
        self.Modules = {}
        self.Module_Files = []
        self.refresh()
    
    def refresh(self):
        """
        Update the internal module list to reflect the state of files on disk
        """
        self.Module_Files = []
        self.Modules = {}
        module_paths = maya.mel.eval('getenv MAYA_MODULE_PATH').split(";")
        for p in module_paths:
            try:
                self.Module_Files += [os.path.join(p, x).replace('\\', '/') for x in os.listdir(p) if x.lower()[-3:] == "mod"]
            except OSError: 
                pass # ignore bad paths
        for eachfile in self.Module_Files:
            for eachmod in self.parse_mod(eachfile):
                self.Modules["%s (%s)" % (eachmod.name, eachmod.version)] = eachmod 
                
    def parse_mod(self, modfile):
        """
        Yields a modtuple describing the supplied .mod file
        """
        with open (modfile, 'rt') as filehandle:
            for line in filehandle:
                if line.startswith("+") or line.startswith("-"):
                    enable, name, version, path = self.parse_mod_entry(line)
                    yield modTuple(enable == "+", name, version, path, modfile)
                    
    def parse_mod_entry(self, line):
        """
        parses a line from a mod file describing a given mod
        """
        
        enable, _, line = line.partition(" ")
        name, _, line = line.partition(" ")
        if 'PLATFORM:' in name.upper():
            name, _, line = line.partition(" ")
        version, _, path = line.strip().partition(" ")
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
            

#GUI classes
#======================================
class ModuleTemplate(lists.ItemTemplate):
    """
    Create a complex display widger for each modTuple
    """
    def widget(self, item):
        with BindingContext() as bc:
            with forms.HorizontalExpandForm('root', parent=self.Parent, height=60) as root:
                with forms.VerticalExpandForm('cb', width=60) as cbf:
                    gui.CheckBox('enabled', label='', tag=item, value=item.enabled).bind.value > bind() > (item, 'enabled')
                    cbf.dock(cbf.enabled, left=20, top=10, bottom=40, right=5)
                with forms.FillForm('path', width=300):
                    with gui.ColumnLayout('x'):
                        gui.Text('displayName', font='boldLabelFont').bind.label < bind() < (item, 'name')
                        gui.Text('path', font='smallObliqueLabelFont').bind.label < bind() < (item, 'path')
                with gui.GridLayout('btns', width=140, numberOfColumns=2):
                    edit = gui.Button('edit', label='Edit', tag=item)
                    show = gui.Button('show', label='Show', tag=item)
                    
        root.cb.enabled.changeCommand += self.update_status
        root.btns.show.command += self.show_item
        root.btns.edit.command += self.edit
        
        return lists.Templated(item, root, edit=edit.command, show=show.command)
    
    @classmethod
    def update_status(cls, *args, **kwargs):
        kwargs['sender'].update_bindings()
        
    @classmethod
    def show_item(cls, *args, **kwargs):
        wb.open('"%s"' % os.path.dirname(kwargs['sender'].Tag.file))

    @classmethod
    def edit(cls, *args, **kwargs):
        os.startfile('"%s"' % kwargs['sender'].Tag.file)    


class ModuleManagerDialog(object):
    """
    Module manager dialog, implemented via LayoutDialog
    """
    def __init__(self):
        self.ModMgr = ModuleManager()
        self.ModMgr.refresh()
        self.Widgets = {}
        
    def _layout(self):
        with forms.LayoutDialogForm('base') as base:
            with BindingContext() as bc:
                with forms.VerticalThreePane('root', width=512) as main:
                    with forms.VerticalForm('header'):
                        gui.Text('x', 'Installed modules')
                     
                    with forms.FillForm('middle'):
                        mod_list = lists.VerticalList('xxx', itemTemplate=ModuleTemplate)
                        mod_list.Collection < bind() < (self.ModMgr.Modules, 'values')
                        # binds the 'values' method of the ModuleManager's Modules{} dictionary
                                                
                    with forms.HorizontalStretchForm('footer'):
                        gui.Button('Cancel', label='cancel').command += self._cancel
                        gui.Separator(None, style='none')
                        gui.Button('Save', label='save').command += self._save
        base.fill(main, 5)   
        mod_list.update_bindings()     
        
    def _cancel(self, *args, **kwargs):
        cmds.layoutDialog(dismiss="dismiss")
 
    def _save(self, *arg, **kwargs):
        for v in self.ModMgr.Modules.values():
            if v.enabled: self.ModMgr.enable(v)
            if not v.enabled: self.ModMgr.disable(v)            
        cmds.layoutDialog(dismiss="OK")
 
    def show(self):
        self.ModMgr.refresh()
        cmds.layoutDialog(ui=self._layout, t='Module editor')

#example:
#   m = ModuleManagerDialog()        
#   m.show()
