"""
mGui wrapper classes

Auto-generated wrapper classes for use with mGui
"""

import maya.cmds as cmds

from mGui.core import Layout


class ColumnLayout(Layout):
    """Wrapper class for cmds.columnLayout"""
    CMD = getattr(cmds, 'columnLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'columnAlign', 'columnOffset', 'rowSpacing', 'columnWidth', 'columnAttach', 'adjustableColumn']
    _CALLBACKS = []


class DockControl(Layout):
    """Wrapper class for cmds.dockControl"""
    CMD = getattr(cmds, 'dockControl', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'raise', 'area', 'label', 'content', 'allowedArea', 'floating', 'enablePopupOption']
    _CALLBACKS = ['floatChangeCommand']


class FlowLayout(Layout):
    """Wrapper class for cmds.flowLayout"""
    CMD = getattr(cmds, 'flowLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'columnSpacing', 'wrap', 'vertical']
    _CALLBACKS = []


class FormLayout(Layout):
    """Wrapper class for cmds.formLayout"""
    CMD = getattr(cmds, 'formLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'attachNone', 'attachControl', 'attachOppositeForm', 'attachForm', 'attachPosition',
                'attachOppositeControl', 'numberOfDivisions']
    _CALLBACKS = []


class FrameLayout(Layout):
    """Wrapper class for cmds.frameLayout"""
    CMD = getattr(cmds, 'frameLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'marginHeight', 'labelWidth', 'collapse', 'labelIndent', 'collapsable', 'borderVisible', 'label',
                'marginWidth', 'borderStyle', 'font', 'labelVisible', 'labelAlign']
    _CALLBACKS = ['collapseCommand', 'expandCommand', 'preCollapseCommand', 'preExpandCommand']


class GridLayout(Layout):
    """Wrapper class for cmds.gridLayout"""
    CMD = getattr(cmds, 'gridLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'cellWidth', 'columnsResizable', 'gridOrder', 'numberOfColumns', 'cellWidthHeight', 'numberOfRows',
                'numberOfRowsColumns', 'autoGrow', 'position', 'allowEmptyCells', 'cellHeight']
    _CALLBACKS = []


class MenuBarLayout(Layout):
    """Wrapper class for cmds.menuBarLayout"""
    CMD = getattr(cmds, 'menuBarLayout', NotImplemented)
    _ATTRIBS = ['menuBarVisible', 'menuArray', 'menuIndex', 'numberOfMenus']
    _CALLBACKS = []


class PaneLayout(Layout):
    """Wrapper class for cmds.paneLayout"""
    CMD = getattr(cmds, 'paneLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'pane3', 'pane2', 'pane1', 'activeFrameThickness', 'pane4', 'numberOfVisiblePanes', 'configuration',
                'activePaneIndex', 'paneSize', 'setPane', 'activePane', 'separatorThickness', 'staticWidthPane',
                'paneUnderPointer', 'staticHeightPane']
    _CALLBACKS = ['separatorMovedCommand']


class RowColumnLayout(Layout):
    """Wrapper class for cmds.rowColumnLayout"""
    CMD = getattr(cmds, 'rowColumnLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'columnAlign', 'columnOffset', 'rowHeight', 'rowSpacing', 'columnWidth', 'numberOfColumns',
                'columnAttach', 'numberOfRows', 'columnSpacing', 'rowAlign', 'rowOffset', 'rowAttach']
    _CALLBACKS = []


class RowLayout(Layout):
    """Wrapper class for cmds.rowLayout"""
    CMD = getattr(cmds, 'rowLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'rowAttach', 'columnAttach', 'columnWidth2', 'columnWidth3', 'columnWidth1', 'columnWidth6',
                'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4', 'columnAlign3',
                'columnAlign2', 'columnAlign1', 'numberOfColumns', 'adjustableColumn', 'columnAlign',
                'adjustableColumn1', 'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4', 'adjustableColumn5',
                'adjustableColumn6', 'columnWidth', 'columnOffset1', 'columnOffset2', 'columnOffset3', 'columnOffset4',
                'columnOffset5', 'columnOffset6', 'columnAttach6', 'columnAttach4', 'columnAttach5', 'columnAttach2',
                'columnAttach3', 'columnAttach1']
    _CALLBACKS = []


class ScrollLayout(Layout):
    """Wrapper class for cmds.scrollLayout"""
    CMD = getattr(cmds, 'scrollLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'verticalScrollBarThickness', 'scrollAreaWidth', 'scrollPage', 'scrollAreaHeight', 'childResizable',
                'horizontalScrollBarThickness', 'scrollByPixel', 'scrollAreaValue', 'minChildWidth']
    _CALLBACKS = ['resizeCommand']


class ShelfLayout(Layout):
    """Wrapper class for cmds.shelfLayout"""
    CMD = getattr(cmds, 'shelfLayout', NotImplemented)
    _ATTRIBS = ['cellWidth', 'style', 'cellHeight', 'cellWidthHeight', 'position']
    _CALLBACKS = []


class ShelfTabLayout(Layout):
    """Wrapper class for cmds.shelfTabLayout"""
    CMD = getattr(cmds, 'shelfTabLayout', NotImplemented)
    _ATTRIBS = ['verticalScrollBarThickness', 'scrollable', 'tabsVisible', 'image', 'imageVisible', 'selectTabIndex',
                'tabLabelIndex', 'childResizable', 'horizontalScrollBarThickness', 'tabLabel', 'innerMarginHeight',
                'selectTab', 'moveTab', 'innerMarginWidth', 'minChildWidth']
    _CALLBACKS = ['changeCommand', 'doubleClickCommand', 'preSelectCommand', 'selectCommand']


class TabLayout(Layout):
    """Wrapper class for cmds.tabLayout"""
    CMD = getattr(cmds, 'tabLayout', NotImplemented)
    _ATTRIBS = ['backgroundColor', 'verticalScrollBarThickness', 'scrollable', 'tabsVisible', 'image', 'imageVisible', 'selectTabIndex',
                'tabLabelIndex', 'childResizable', 'horizontalScrollBarThickness', 'tabLabel', 'innerMarginHeight',
                'selectTab', 'moveTab', 'innerMarginWidth', 'minChildWidth']
    _CALLBACKS = ['changeCommand', 'doubleClickCommand', 'preSelectCommand', 'selectCommand']


    def layout(self):
        kids = [(i.widget, i.key) for i in self.controls]
        self.tabLabel = kids
        return super(TabLayout, self).layout()

class ToolBar(Layout):
    """Wrapper class for cmds.toolBar"""
    CMD = getattr(cmds, 'toolBar', NotImplemented)
    _ATTRIBS = ['allowedArea', 'content', 'area', 'label']
    _CALLBACKS = []


