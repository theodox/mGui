import mGui.gui as gui
import maya.cmds as cmds
"""
This example shows a cleaned up version of traditional Maya GUI using context managers and addressing but no other new features

Note: buttons are non-functional; this just shows layout style
"""

def main():
    with gui.Window(title="Ugly version") as main_window:
        with gui.ColumnLayout(width=256) as main:
            with gui.FrameLayout(label="buttons column") as t_buttons:
                with gui.ColumnLayout() as col:
                    mk_sphere = gui.Button(label="Make Sphere")
                    mk_cone = gui.Button(label="Make Cone")
                    mk_cube = gui.Button(label="Make Cube")

            with gui.FrameLayout(label="buttons row") as r_buttons:
                with gui.RowLayout(numberOfColumns=3) as row:
                    mk_sphere = gui.Button(label="Make Sphere")
                    mk_cone = gui.Button(label="Make Cone")
                    mk_cube = gui.Button(label="Make Cube")

            with gui.FrameLayout(label="buttons grid") as g_buttons:
                with gui.GridLayout(numberOfColumns=2) as grid:
                    mk_sphere = gui.Button(label="Make Sphere")
                    mk_cone = gui.Button(label="Make Cone")
                    mk_cube = gui.Button(label="Make Cube")
                    mk_circle = gui.Button(label="Make Circle")

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
    return main_window

if __name__ == '__main__':
    main_window = main()
    main_window.show()
