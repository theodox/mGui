
import sys
import pymel.core as pm
import maya.cmds as cmds
sys.path.append(r"C:\Users\Stephen Theodore\Documents\GitHub\mGui")
###
import mGui.core as core
import mGui.controls as ctrl
import mGui.layouts as lyt
import mGui.styles as styles
import mGui.bindings as bindings
import mGui.events as events
import mGui.forms as forms
import mGui.styles as style
import mGui.observable as obs
import mGui.lists as lists


class exx(object):
    def __init__(self, name):
        self.Name = name
        self.Value = 5
    
    def __str__(self):
       return str(self.Name)

test = obs.ViewCollection(exx("hello"), exx("world"))
def flt (*args, **kwargs):
    lm = eval("lambda x: " + args[0])
    test.update_filter(lm)
     
w = core.Window('window', title = 'fred')
with bindings.BindingContext() as bc:
    with forms.VerticalForm('main') as main:
        with lyt.TabLayout('sub', height = 240):
            test >> lists.VerticalListForm('lister' ).Collection
        with forms.HorizontalStretchForm('buttons', height = 32):
            ctrl.TextField('filterbox', width = 300)
            bb = ctrl.Text(0, width = 60) 
            test + "ViewCount" >> bb + 'label'
            
cmds.showWindow(w)                
