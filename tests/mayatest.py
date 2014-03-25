import mGui
from mGui.controls import *
from mGui.layouts import *
from mGui.core import Window


window = Window('main window', title="Ugly version")
with ColumnLayout('gui', width = 256) as gui:
    with FrameLayout("t_buttons", label = "buttons column"):
        with ColumnLayout("col"):
            Button('mkSphere', label = "Make Sphere")
            Button('mkCone', label ="Make Cone")
            Button('mkCube', label ="Make Cube")
       
    with FrameLayout("r_buttons", label = "buttons row"):
        with RowLayout ("row", numberOfColumns=3):
            Button('mkSphere', label = "Make Sphere")
            Button('mkCone', label ="Make Cone")
            Button('mkCube', label ="Make Cube")

    with FrameLayout("g_buttons", label = "buttons grid"):
        with GridLayout("grid", numberOfColumns = 2):
            Button('mkSphere', label = "Make Sphere")
            Button('mkCone', label ="Make Cone")
            Button('mkCube', label ="Make Cube")
            Button('mkCircle', label = "Make Circle")


# using the iterability of the layout to set widths 

for item in gui.t_buttons:
    item.width = 256
    
for item in gui.r_buttons.row:
    item.width = 85
item.width = 256
item.columnWidth3 = (85,85,85)    
    
for item in gui.g_buttons.grid:
    item.width = 128
item.width = 256
item.cellWidth = 128

cmds.showWindow(window)