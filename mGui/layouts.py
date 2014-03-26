'''
mGui wrapper classes

Auto-generated wrapper classes for use with mGui
'''

import maya.cmds as cmds
from mGui.core import Layout

class ColumnLayout(Layout):
    '''Wrapper class for cmds.columnLayout'''
    CMD = cmds.columnLayout
    _ATTRIBS = ['columnAlign','columnOffset','rowSpacing','columnWidth','columnAttach','adjustableColumn']
    _CALLBACKS = []


class DockControl(Layout):
    '''Wrapper class for cmds.dockControl'''
    CMD = cmds.dockControl
    _ATTRIBS = ['raise','area','label','content','allowedArea','floating','enablePopupOption']
    _CALLBACKS = ['floatChangeCommand']


class FlowLayout(Layout):
    '''Wrapper class for cmds.flowLayout'''
    CMD = cmds.flowLayout
    _ATTRIBS = ['columnSpacing','wrap','vertical']
    _CALLBACKS = []


class FormLayout(Layout):
    '''Wrapper class for cmds.formLayout'''
    CMD = cmds.formLayout
    _ATTRIBS = ['attachNone','attachControl','attachOppositeForm','attachForm','attachPosition','attachOppositeControl','numberOfDivisions']
    _CALLBACKS = []


class FrameLayout(Layout):
    '''Wrapper class for cmds.frameLayout'''
    CMD = cmds.frameLayout
    _ATTRIBS = ['marginHeight','labelWidth','collapse','labelIndent','collapsable','borderVisible','label','marginWidth','borderStyle','font','labelVisible','labelAlign']
    _CALLBACKS = ['collapseCommand','expandCommand','preCollapseCommand','preExpandCommand']


class GridLayout(Layout):
    '''Wrapper class for cmds.gridLayout'''
    CMD = cmds.gridLayout
    _ATTRIBS = ['cellWidth','columnsResizable','gridOrder','numberOfColumns','cellWidthHeight','numberOfRows','numberOfRowsColumns','autoGrow','position','allowEmptyCells','cellHeight']
    _CALLBACKS = []


class MenuBarLayout(Layout):
    '''Wrapper class for cmds.menuBarLayout'''
    CMD = cmds.menuBarLayout
    _ATTRIBS = ['menuBarVisible','menuArray','menuIndex','numberOfMenus']
    _CALLBACKS = []


class PaneLayout(Layout):
    '''Wrapper class for cmds.paneLayout'''
    CMD = cmds.paneLayout
    _ATTRIBS = ['pane3','pane2','pane1','activeFrameThickness','pane4','numberOfVisiblePanes','configuration','activePaneIndex','paneSize','setPane','activePane','separatorThickness','staticWidthPane','paneUnderPointer','staticHeightPane']
    _CALLBACKS = ['separatorMovedCommand']


class RowColumnLayout(Layout):
    '''Wrapper class for cmds.rowColumnLayout'''
    CMD = cmds.rowColumnLayout
    _ATTRIBS = ['columnAlign','columnOffset','rowHeight','rowSpacing','columnWidth','numberOfColumns','columnAttach','numberOfRows','columnSpacing','rowAlign','rowOffset','rowAttach']
    _CALLBACKS = []


class RowLayout(Layout):
    '''Wrapper class for cmds.rowLayout'''
    CMD = cmds.rowLayout
    _ATTRIBS = ['rowAttach','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','columnAlign1','numberOfColumns','adjustableColumn','columnAlign','adjustableColumn1','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','columnOffset1','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3','columnAttach1']
    _CALLBACKS = []


class ScrollLayout(Layout):
    '''Wrapper class for cmds.scrollLayout'''
    CMD = cmds.scrollLayout
    _ATTRIBS = ['verticalScrollBarThickness','scrollAreaWidth','scrollPage','scrollAreaHeight','childResizable','horizontalScrollBarThickness','scrollByPixel','scrollAreaValue','minChildWidth']
    _CALLBACKS = ['resizeCommand']


class ShelfLayout(Layout):
    '''Wrapper class for cmds.shelfLayout'''
    CMD = cmds.shelfLayout
    _ATTRIBS = ['cellWidth','style','cellHeight','cellWidthHeight','position']
    _CALLBACKS = []


class ShelfTabLayout(Layout):
    '''Wrapper class for cmds.shelfTabLayout'''
    CMD = cmds.shelfTabLayout
    _ATTRIBS = ['verticalScrollBarThickness','scrollable','tabsVisible','image','imageVisible','selectTabIndex','tabLabelIndex','childResizable','horizontalScrollBarThickness','tabLabel','innerMarginHeight','selectTab','moveTab','innerMarginWidth','minChildWidth']
    _CALLBACKS = ['changeCommand','doubleClickCommand','preSelectCommand','selectCommand']


class TabLayout(Layout):
    '''Wrapper class for cmds.tabLayout'''
    CMD = cmds.tabLayout
    _ATTRIBS = ['verticalScrollBarThickness','scrollable','tabsVisible','image','imageVisible','selectTabIndex','tabLabelIndex','childResizable','horizontalScrollBarThickness','tabLabel','innerMarginHeight','selectTab','moveTab','innerMarginWidth','minChildWidth']
    _CALLBACKS = ['changeCommand','doubleClickCommand','preSelectCommand','selectCommand']


class ToolBar(Layout):
    '''Wrapper class for cmds.toolBar'''
    CMD = cmds.toolBar
    _ATTRIBS = ['allowedArea','content','area','label']
    _CALLBACKS = []


