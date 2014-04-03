

import mGui.gui as gui
import mGui.lists as lists
import mGui.observable as observable
import mGui.forms as forms
import mGui.styles 
from mGui.bindings import bind, BindingContext
import traceback

'''
ModuleManager.py

Defines ModuleManager class for enabling/disable Maya modules, and ModuleManagerDialog - a GUI for same.

Copyright  (c) 2014 Steve Theodore. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import itertools
import maya.cmds as cmds
import os
import maya.mel
from collections import namedtuple

# Mod manager classes
#==============================================================================================

class modTuple(object):
    def __init__(self, enabled, name, version, path, file):
        self.enabled = enabled
        self.name = name
        self.version = version
        self.path = path
        self.file = file

class ModuleManager (object):
    '''
    Manages the list of .mod files on the local maya's MAYA_MODULE_PATH.
    
    Note this class is purely functional - UI is handled in the ModuleManagerDialog via binding
    '''
    def __init__(self):
        self.Modules = {}
        self.Module_Files = []
        self.refresh()
    
    def refresh(self):
        '''
        Update the internal module list to reflect the state of files on disk
        '''
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
        '''
        Yields a modtuple describing the supplied .mod file
        '''
        with open (modfile, 'rt') as filehandle:
            for line in filehandle:
                if line.startswith("+") or line.startswith("-"):
                    enable, name, version, path = self.parse_mod_entry(line)
                    yield modTuple(enable == "+", name, version, path, modfile)
                    
    def parse_mod_entry(self, line):
        '''
        parses a line from a mod file describing a given mod
        '''
        
        enable, ignore, line = line.partition(" ")
        name, ignore, line = line.partition(" ")
        if 'PLATFORM:' in name.upper():
            name, ignore, line  = line.partition(" ")
        version, ignore, path = line.strip().partition(" ")
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
            


#======================================



        
class ModuleTemplate(lists.ItemTemplate):
    def widget(self, item):
        with BindingContext() as bc:
            with forms.HorizontalExpandForm('root', parent = self.Parent, height = 60) as root:
                with forms.Form('cb', width = 60):
                     gui.CheckBox('enabled', label = '', tag = item, value = item.enabled).bind.value > bind() > (item, 'enabled')
                with forms.FillForm('path', width = 300):
                    with gui.ColumnLayout('x'):
                        gui.Text('displayName', font='boldLabelFont').bind.label < bind() < (item, 'name')
                        gui.Text('path', font = 'smallObliqueLabelFont').bind.label < bind() < (item, 'path')
                with gui.GridLayout('btns', width = 140, numberOfColumns = 2):
                    edit =  gui.Button('edit', label = 'Edit', tag = item)
                    show = gui.Button('show',  label = 'Show', tag = item)
                    
        root.cb.enabled.changeCommand += self.update_status
        root.btns.show.command += self.show_item
        return lists.Templated(item, root, edit = edit.command, show = show.command)
    
    @classmethod
    def update_status(cls, *args, **kwargs):
        kwargs['sender'].update_bindings()
        
    @classmethod
    def show_item(cls, *args, **kwargs):
        os.system('start "%s"' % os.path.dirname( kwargs['sender'].Tag.file) )
    
    
class ModuleManagerDialog(object):
    '''
    Module manager dialog, implemented via LayoutDialog
    '''
    def __init__(self):
        self.ModMgr = ModuleManager()
        self.ModMgr.refresh()
        self.Widgets = {}
        
    def _layout(self):
        with forms.LayoutDialogForm('base') as base:
            with BindingContext() as bc:
                with forms.VerticalThreePane('root', width = 512) as main:
                    with forms.VerticalForm('header' ):
                        gui.Text('x', 'Installed modules')
                     
                    with forms.FillForm('middle'):
                        mod_list = lists.VerticalList('xxx', itemTemplate = ModuleTemplate)
                        mod_list.Collection < bind() < (self.ModMgr.Modules, 'values')
                        
                        
                    with forms.HorizontalStretchForm('footer'):
                        gui.Button('Cancel', label='cancel').command += self._cancel
                        gui.Separator(None, style = 'none')
                        gui.Button('Save', label='save').command += self._save
        base.fill(main, 5)   
        mod_list.update_bindings()     
        
    def _cancel(self, *args, **kwargs):
        cmds.layoutDialog(dismiss = "dismiss")
 
    def _save(self, *arg, **kwargs):
        for info, v in self.ModMgr.Modules.items():
            if v.enabled: self.ModMgr.enable(v)
            if not v.enabled: self.ModMgr.disable(v)            
        cmds.layoutDialog(dismiss = "OK")
 
    def show(self):
        self.ModMgr.refresh()
        cmds.layoutDialog(ui = self._layout, t='Module editor')


m = ModuleManagerDialog()        
m.show()