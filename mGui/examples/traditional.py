import mGui.gui as gui
import maya.cmds as cmds
"""
This example shows a cleaned up version of traditional Maya GUI using context managers and addressing but no other new features

Note: buttons are non-functional; this just shows layout style
"""


window = gui.Window('main window', title="Ugly version")
with gui.ColumnLayout('gui', width=256) as main:
    with gui.FrameLayout("t_buttons", label="buttons column"):
        with gui.ColumnLayout("col"):
            gui.Button('mkSphere', label="Make Sphere")
            gui.Button('mkCone', label="Make Cone")
            gui.Button('mkCube', label="Make Cube")

    with gui.FrameLayout("r_buttons", label="buttons row"):
        with gui.RowLayout ("row", numberOfColumns=3):
            gui.Button('mkSphere', label="Make Sphere")
            gui.Button('mkCone', label="Make Cone")
            gui.Button('mkCube', label="Make Cube")

    with gui.FrameLayout("g_buttons", label="buttons grid"):
        with gui.GridLayout("grid", numberOfColumns=2):
            gui.Button('mkSphere', label="Make Sphere")
            gui.Button('mkCone', label="Make Cone")
            gui.Button('mkCube', label="Make Cube")
            gui.Button('mkCircle', label="Make Circle")

# using the iterability of the layout to set widths

for item in main.t_buttons:
    item.width = 256

for item in main.r_buttons.row:
    item.width = 85

# last 'item' is the row itself...
item.width = 256
item.columnWidth3 = (85, 85, 85)

for item in main.g_buttons.grid:
    item.width = 128

# last item is the grid...
item.width = 256
item.cellWidth = 128

cmds.showWindow(window)
