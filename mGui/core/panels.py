"""
mGui wrapper classes

Auto-generated wrapper classes for use with mGui
"""

import maya.cmds as cmds

from mGui.core import Control, Nested
from mGui.core.editors import EditorFactory
from mGui.properties import WrappedCtlProperty


def make_editor_command(cmd, editorString):
    return WrappedCtlProperty(editorString, cmd, True, EditorFactory.get)


class Panel(Nested):
    CMD = cmds.panel
    PANEL_TYPE = None
    _ATTRIBS = [
        "copy",
        "defineTemplate",
        "docTag",
        "exists",
        "init",
        "label",
        "menuBarVisible",
        "needsInit",
        "parent",
        "replacePanel",
        "tearOff",
        "tearOffCopy",
        "unParent",
        "useTemplate",
        "createString",
        "editString",
    ]
    _READONLY = ["control", "isUnique"]
    _CALLBACKS = ["popupMenuProcedure"]


class ModelPanel(Panel):
    CMD = cmds.modelPanel
    PANEL_TYPE = "modelPanel"

    _ATTRIBS = [
        "barLayout",
        "camera",
        "copy",
        "defineTemplate",
        "docTag",
        "exists",
        "init",
        "label",
        "menuBarVisible",
        "needsInit",
        "parent",
        "replacePanel",
        "tearOff",
        "tearOffCopy",
        "unParent",
        "useTemplate",
    ]
    _READONLY = ["control", "isUnique"]
    _CALLBACKS = ["popupMenuProcedure"]

    modelEditor = make_editor_command(cmds.modelPanel, "modelEditor")


class HardwareRenderPanel(Panel):
    """Wrapper class for cmds.hardwareRenderPanel"""

    CMD = cmds.hardwareRenderPanel
    _ATTRIBS = [
        "camera",
        "copy",
        "defineTemplate",
        "docTag",
        "exists",
        "init",
        "isUnique",
        "label",
        "menuBarVisible",
        "needsInit",
        "parent",
        "replacePanel",
        "tearOff",
        "tearOffCopy",
        "unParent",
        "useTemplate",
    ]
    _CALLBACKS = ["popupMenuProcedure"]
    _READ_ONLY = ["control"]

    glRenderEditor = make_editor_command(cmds.glRenderEditor, "glRenderEditor")


class HyperGraph(Panel):
    """Wrapper class for cmds.hyperGraph"""

    CMD = cmds.hyperGraph
    _ATTRIBS = [
        "addBookmark",
        "addDependGraph",
        "addDependNode",
        "animateTransition",
        "attributeEditor",
        "bookmarkName",
        "clear",
        "collapseContainer",
        "connectionDrawStyle",
        "control",
        "defineTemplate",
        "deleteBookmark",
        "dependGraph",
        "dependNode",
        "docTag",
        "down",
        "downstream",
        "dropNode",
        "dropTargetNode",
        "enableAutomaticLayout",
        "exists",
        "expandContainer",
        "feedbackGadget",
        "feedbackNode",
        "filter",
        "filterDetail",
        "fitImageToHeight",
        "fitImageToWidth",
        "fold",
        "forceMainConnection",
        "forceRefresh",
        "frame",
        "frameBranch",
        "frameGraph",
        "frameHierarchy",
        "freeform",
        "fromAttr",
        "getNodeList",
        "getNodePosition",
        "graphLayoutStyle",
        "graphType",
        "highlightConnection",
        "iconSize",
        "image",
        "imageEnabled",
        "imageForContainer",
        "imagePosition",
        "imageScale",
        "isHotkeyTarget",
        "layout",
        "layoutSelected",
        "lockMainConnection",
        "look",
        "mainListConnection",
        "mergeConnections",
        "navigateHome",
        "nextView",
        "opaqueContainers",
        "orientation",
        "panel",
        "parent",
        "popupMenuScript",
        "previousView",
        "range",
        "rebuild",
        "removeNode",
        "rename",
        "resetFreeform",
        "restoreBookmark",
        "scrollUpDownNoZoom",
        "selectionConnection",
        "setNodePosition",
        "showConstraints",
        "showDeformers",
        "showExpressions",
        "showInvisible",
        "showRelationships",
        "showShapes",
        "showUnderworld",
        "stateString",
        "transitionFrames",
        "unParent",
        "unfold",
        "unfoldAll",
        "unlockMainConnection",
        "updateMainConnection",
        "updateNodeAdded",
        "updateSelection",
        "upstream",
        "useFeedbackList",
        "useTemplate",
        "viewOption",
        "visibility",
        "zoom",
    ]
    _CALLBACKS = [
        "dragAndDropBehaviorCommand",
        "edgeDimmedDblClickCommand",
        "edgeDblClickCommand",
        "focusCommand",
        "nodeDropCommand",
        "nodePressCommand",
        "nodeReleaseCommand",
    ]


class HyperPanel(Panel):
    """Wrapper class for cmds.hyperPanel"""

    CMD = cmds.hyperPanel
    _ATTRIBS = [
        "control",
        "copy",
        "defineTemplate",
        "docTag",
        "exists",
        "init",
        "isUnique",
        "label",
        "menuBarVisible",
        "needsInit",
        "parent",
        "replacePanel",
        "tearOff",
        "tearOffCopy",
        "unParent",
        "useTemplate",
    ]
    _CALLBACKS = ["popupMenuProcedure"]

    hyperEditor = make_editor_command(cmds.hyperGraph, "hyperEditor")


class HyperShade(Panel):
    """Wrapper class for cmds.hyperShade"""

    CMD = cmds.hyperShade
    _ATTRIBS = [
        "assign",
        "clearWorkArea",
        "collapse",
        "createNode",
        "dependGraphArea",
        "downStream",
        "duplicate",
        "fixRenderSize",
        "incremental",
        "listDownstreamNodes",
        "listDownstreamShaderNodes",
        "listUpstreamNodes",
        "name",
        "networks",
        "noSGShapes",
        "noShapes",
        "noTransforms",
        "objects",
        "renderCreateAndDrop",
        "reset",
        "resetGraph",
        "resetSwatch",
        "setAllowsRegraphing",
        "setWorkArea",
        "shaderNetwork",
        "shaderNetworks",
        "shaderNetworksSelectMaterialNodes",
        "snapShot",
        "uncollapse",
        "upStream",
        "userDefinedLayout",
        "workAreaAddCmd",
        "workAreaDeleteCmd",
        "workAreaSelectCmd",
    ]
    _CALLBACKS = []


class NodeOutliner(Panel):
    """Wrapper class for cmds.nodeOutliner"""

    CMD = cmds.nodeOutliner
    _ATTRIBS = [
        "isObscured",
        "attrAlphaOrder",
        "showNonKeyable",
        "fullPathName",
        "preventOverride",
        "height",
        "visible",
        "enable",
        "lastClickedNode",
        "query",
        "menuMultiOption",
        "numberOfPopupMenus",
        "enableBackground",
        "noConnectivity",
        "showOutputs",
        "pressHighlightsUnconnected",
        "annotation",
        "width",
        "backgroundColor",
        "currentSelection",
        "addObject",
        "manage",
        "lastMenuChoice",
        "niceNames",
        "connectivity",
        "showInputs",
        "replace",
        "showNonConnectable",
        "noBackground",
        "nodesDisplayed",
        "redraw",
        "longNames",
        "edit",
        "popupMenuArray",
        "showReadOnly",
        "remove",
        "removeAll",
        "showHidden",
        "multiSelect",
        "showPublished",
        "showConnectedOnly",
        "redrawRow",
    ]
    _CALLBACKS = [
        "addCommand",
        "dragCallback",
        "dropCallback",
        "menuCommand",
        "selectCommand",
        "visibleChangeCommand",
    ]


class OutlinerPanel(Panel):
    """Wrapper class for cmds.outlinerPanel"""

    CMD = cmds.outlinerPanel
    _ATTRIBS = ["edit", "createString", "editString", "query"]
    _CALLBACKS = ["popupMenuProcedure"]

    outlinerEditor = make_editor_command(cmds.outlinerEditor, "outlinerEditor")


class PanelConfiguration(Panel):
    """Wrapper class for cmds.panelConfiguration"""

    CMD = cmds.panelConfiguration
    _ATTRIBS = [
        "replaceTypeString",
        "createStrings",
        "addPanel",
        "edit",
        "replaceCreateString",
        "defaultImage",
        "replaceFixedState",
        "removeLastPanel",
        "replaceLabel",
        "removeAllPanels",
        "labelStrings",
        "isFixedState",
        "editStrings",
        "replaceEditString",
        "query",
        "typeStrings",
        "sceneConfig",
        "numberOfPanels",
        "image",
        "configString",
    ]
    _CALLBACKS = []


class PanelHistory(Panel):
    """Wrapper class for cmds.panelHistory"""

    CMD = cmds.panelHistory
    _ATTRIBS = [
        "historyDepth",
        "edit",
        "clear",
        "back",
        "forward",
        "suspend",
        "isEmpty",
        "wrap",
        "query",
        "targetPane",
    ]
    _CALLBACKS = []


class ScriptedPanel(Panel):
    """Wrapper class for cmds.scriptedPanel"""

    CMD = cmds.scriptedPanel
    _ATTRIBS = ["edit", "query", "createString", "type", "editString"]
    _CALLBACKS = ["popupMenuProcedure"]


class SpreadSheetEditor(Panel):
    """Wrapper class for cmds.spreadSheetEditor"""

    CMD = cmds.spreadSheetEditor
    _ATTRIBS = [
        "attrRegExp",
        "allAttr",
        "query",
        "unlockMainConnection",
        "fixedAttrList",
        "highlightConnection",
        "forceMainConnection",
        "showShapes",
        "lockMainConnection",
        "updateMainConnection",
        "precision",
        "selectedAttr",
        "niceNames",
        "stateString",
        "keyableOnly",
        "panel",
        "execute",
        "longNames",
        "edit",
        "filter",
        "mainListConnection",
        "selectionConnection",
    ]
    _CALLBACKS = []


class Visor(Panel):
    """Wrapper class for cmds.visor"""

    CMD = cmds.visor
    _ATTRIBS = [
        "addFolder",
        "addNodes",
        "allowPanningInX",
        "allowPanningInY",
        "allowZooming",
        "command",
        "deleteFolder",
        "editFolder",
        "folderList",
        "menu",
        "name",
        "nodeType",
        "openDirectories",
        "openFolder",
        "parent",
        "path",
        "popupMenuScript",
        "rebuild",
        "refreshAllSwatches",
        "refreshSelectedSwatches",
        "refreshSwatch",
        "reset",
        "restrictPanAndZoom",
        "saveSwatches",
        "scrollBar",
        "scrollPercent",
        "selectedGadgets",
        "showDividers",
        "showFiles",
        "showFolders",
        "showNodes",
        "stateString",
        "style",
        "transform",
        "type",
    ]
    _CALLBACKS = []


class PanelFactory(object):
    TYPES = {
        "modelPanel": ModelPanel,
        "hardwareRenderPanel": HardwareRenderPanel,
        "hyperGraph": HyperGraph,
        "hyperPanel": HyperPanel,
        "hyperShade": HyperShade,
        "nodeOutliner": NodeOutliner,
        "outlinerPanel": OutlinerPanel,
        "panelConfiguration": PanelConfiguration,
        "panelHistory": PanelHistory,
        "scriptedPanel": ScriptedPanel,
        "spreadSheetEditor": SpreadSheetEditor,
        "visor": Visor,
    }

    @classmethod
    def get_current_panel(cls):
        current = cmds.getPanel(wf=True)
        try:
            return cls.get(current)
        except RuntimeError:
            return None

    @classmethod
    def get(cls, panel_string):
        ptype = cmds.getPanel(typeOf=panel_string)
        pfclass = cls.TYPES.get(ptype, None)
        if not pfclass:
            raise RuntimeError("Unknown panel type: {}".format(ptype))
        return pfclass.wrap(panel_string, panel_string)


__all__ = [
    "Panel",
    "ModelPanel",
    "HardwareRenderPanel",
    "HyperGraph",
    "HyperPanel",
    "HyperShade",
    "NodeOutliner",
    "OutlinerPanel",
    "PanelConfiguration",
    "PanelHistory",
    "ScriptedPanel",
    "SpreadSheetEditor",
    "Visor",
    "PanelFactory",
]
