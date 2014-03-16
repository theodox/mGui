'''
Created on Mar 15, 2014

@author: Stephen Theodore
'''
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
#reload(core)
reload(obs)
reload(lists)

class exx(object):
    def __init__(self, name):
        self.Name = name
        self.Value = 5
    
    def __str__(self):
       return str(self.Name)

test = obs.ViewCollection(exx("hello"), exx("world"))
def flt (*args, **kwargs):
    print args, kwargs['event'].Data

w = core.Window('window', title = 'fred')
with bindings.BindingContext() as bc:
    with forms.VerticalStretchForm('main') as main:
        with forms.VerticalForm('sub'):
            ctrl.Button('dummy')

            bedtime = lists.ListForm('lister')
            bedtime.Collection << test
            
cmds.showWindow(w)                
test.sort()
bc.update()
for item in bc.Bindings: print item
bedtime.layout()
test.add(exx("blah"))
test.Contents[0].name = 'Fred'
test.Contents[0]
test.clear()


for item in bedtime.Collection:
    print item, type(item), dir(item)
    
    item.update_bindings()