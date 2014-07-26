'''
mGui wrapper classes

Auto-generated wrapper classes for use with mGui
'''

import maya.cmds as cmds

from .core import Control


class ComponentEditor(Control):
    '''Wrapper class for cmds.componentEditor'''
    CMD = cmds.componentEditor
    _ATTRIBS = ['newTab', 'hidePathName', 'query', 'lockMainConnection', 'setOperationLabel', 'lockInput', 'filter',
                'stateString', 'selected', 'hideZeroColumns', 'operationType', 'highlightConnection',
                'forceMainConnection', 'removeTab', 'floatSlider', 'updateMainConnection', 'precision',
                'unlockMainConnection', 'showSelected', 'operationCount', 'panel', 'edit', 'showObjects',
                'selectionConnection', 'floatField', 'mainListConnection', 'sortAlpha', 'operationLabels']
    _CALLBACKS = []


class HardwareRenderPanel(Control):
    '''Wrapper class for cmds.hardwareRenderPanel'''
    CMD = cmds.hardwareRenderPanel
    _ATTRIBS = ["camera", "copy", "defineTemplate", "docTag", "exists", "glRenderEditor", "init", "isUnique", "label",
                "menuBarVisible", "needsInit", "parent", "replacePanel", "tearOff", "tearOffCopy", "unParent",
                "useTemplate"]
    _CALLBACKS = ["popupMenuProcedure"]
    _READ_ONLY = ['control']


class HyperGraph(Control):
    '''Wrapper class for cmds.hyperGraph'''
    CMD = cmds.hyperGraph
    _ATTRIBS = ["addBookmark", "addDependGraph", "addDependNode", "animateTransition", "attributeEditor",
                "bookmarkName", "clear", "collapseContainer", "connectionDrawStyle", "control", "defineTemplate",
                "deleteBookmark", "dependGraph", "dependNode", "docTag", "down", "downstream", "dropNode",
                "dropTargetNode", "enableAutomaticLayout", "exists", "expandContainer", "feedbackGadget",
                "feedbackNode", "filter", "filterDetail", "fitImageToHeight", "fitImageToWidth", "fold",
                "forceMainConnection", "forceRefresh", "frame", "frameBranch", "frameGraph", "frameHierarchy",
                "freeform", "fromAttr", "getNodeList", "getNodePosition", "graphLayoutStyle", "graphType",
                "highlightConnection", "iconSize", "image", "imageEnabled", "imageForContainer", "imagePosition",
                "imageScale", "isHotkeyTarget", "layout", "layoutSelected", "lockMainConnection", "look",
                "mainListConnection", "mergeConnections", "navigateHome", "nextView", "opaqueContainers", "orientation",
                "panel", "parent", "popupMenuScript", "previousView", "range", "rebuild", "removeNode", "rename",
                "resetFreeform", "restoreBookmark", "scrollUpDownNoZoom", "selectionConnection", "setNodePosition",
                "showConstraints", "showDeformers", "showExpressions", "showInvisible", "showRelationships",
                "showShapes", "showUnderworld", "stateString", "transitionFrames", "unParent", "unfold", "unfoldAll",
                "unlockMainConnection", "updateMainConnection", "updateNodeAdded", "updateSelection", "upstream",
                "useFeedbackList", "useTemplate", "viewOption", "visibility", "zoom"]
    _CALLBACKS = ["dragAndDropBehaviorCommand", "edgeDimmedDblClickCommand", "edgeDblClickCommand", "focusCommand",
                  "nodeDropCommand", "nodePressCommand", "nodeReleaseCommand", ]


class HyperPanel(Control):
    '''Wrapper class for cmds.hyperPanel'''
    CMD = cmds.hyperPanel
    _ATTRIBS = ["control", "copy", "defineTemplate", "docTag", "exists", "hyperEditor", "init", "isUnique", "label",
                "menuBarVisible", "needsInit", "parent", "replacePanel", "tearOff", "tearOffCopy", "unParent",
                "useTemplate"]
    _CALLBACKS = ["popupMenuProcedure"]


class HyperShade(Control):
    '''Wrapper class for cmds.hyperShade'''

    CMD = cmds.hyperShade
    _ATTRIBS = ["assign", "clearWorkArea", "collapse", "createNode", "dependGraphArea", "downStream", "duplicate",
                "fixRenderSize", "incremental", "listDownstreamNodes", "listDownstreamShaderNodes", "listUpstreamNodes",
                "name", "networks", "noSGShapes", "noShapes", "noTransforms", "objects", "renderCreateAndDrop", "reset",
                "resetGraph", "resetSwatch", "setAllowsRegraphing", "setWorkArea", "shaderNetwork", "shaderNetworks",
                "shaderNetworksSelectMaterialNodes", "snapShot", "uncollapse", "upStream", "userDefinedLayout",
                "workAreaAddCmd", "workAreaDeleteCmd", "workAreaSelectCmd"]
    _CALLBACKS = []


class ModelEditor(Control):
    '''Wrapper class for cmds.modelEditor'''
    CMD = cmds.modelEditor
    _ATTRIBS = ['rendererOverrideListUI', 'filteredObjectList', 'objectFilterUI', 'cameraSetup', 'query',
                'textureEnvironmentMap', 'addObjects', 'rendererListUI', 'displayTextures', 'colorResolution',
                'lowQualityLighting', 'displayLights', 'smoothWireframe', 'forceMainConnection', 'sortTransparent',
                'grid', 'fogColor', 'nurbsSurfaces', 'shadows', 'clipGhosts', 'userNode', 'edit',
                'smallObjectThreshold', 'textureAnisotropic', 'bufferMode', 'nCloths', 'useDefaultMaterial', 'fogging',
                'nParticles', 'rendererName', 'textureHilight', 'dynamics', 'addSelected', 'subdivSurfaces',
                'unlockMainConnection', 'bumpResolution', 'backfaceCulling', 'rendererDeviceName', 'textureSampling',
                'cameras', 'viewSelected', 'fluids', 'fogSource', 'xray', 'lights', 'nurbsCurves', 'locators',
                'maximumNumHardwareLights', 'cameraName', 'modelPanel', 'textures', 'lockMainConnection',
                'pluginObjects', 'pivots', 'selectionHiliteDisplay', 'follicles', 'stereoDrawMode', 'panel',
                'editorChanged', 'hulls', 'wireframeBackingStore', 'filter', 'twoSidedLighting', 'rendererList',
                'textureMemoryUsed', 'lineWidth', 'cameraSet', 'nRigids', 'jointXray', 'useInteractiveMode', 'fogMode',
                'setSelected', 'activeComponentsXray', 'pluginShapes', 'useBaseRenderer', 'shadingModel',
                'textureMaxSize', 'manipulators', 'ikHandles', 'handles', 'cullingOverride', 'controlVertices',
                'fogDensity', 'updateMainConnection', 'polymeshes', 'greasePencils', 'isFiltered', 'imagePlane',
                'objectFilterShowInHUD', 'objectFilterList', 'headsUpDisplay', 'default', 'hairSystems',
                'queryPluginObjects', 'planes', 'activeView', 'selectionConnection', 'ignorePanZoom',
                'smallObjectCulling', 'interactive', 'textureDisplay', 'joints', 'transparencyAlgorithm',
                'dynamicConstraints', 'occlusionCulling', 'deformers', 'motionTrails', 'stateString',
                'useReducedRenderer', 'textureCompression', 'fogStart', 'activeOnly', 'useColorIndex',
                'objectFilterListUI', 'interactiveBackFaceCull', 'objectFilter', 'highlightConnection',
                'updateColorMode', 'noUndo', 'strokes', 'camera', 'useRGBImagePlane', 'allObjects', 'removeSelected',
                'interactiveDisableShadows', 'displayAppearance', 'rendererOverrideList', 'colorMap', 'viewObjects',
                'fogEnd', 'dimensions', 'maxConstantTransparency', 'mainListConnection', 'transpInShadows',
                'rendererOverrideName', 'wireframeOnShaded', 'viewType']
    _CALLBACKS = []


class ModelPanel(Control):
    '''Wrapper class for cmds.modelPanel'''
    CMD = cmds.modelPanel
    _ATTRIBS = ["barLayout", "camera", "control", "copy", "defineTemplate", "docTag", "exists", "init", "isUnique",
                "label", "menuBarVisible", "modelEditor", "needsInit", "parent", "replacePanel", "tearOff",
                "tearOffCopy", "unParent", "useTemplate"]
    _CALLBACKS = ['popupMenuProcedure']


class NodeOutliner(Control):
    '''Wrapper class for cmds.nodeOutliner'''
    CMD = cmds.nodeOutliner
    _ATTRIBS = ['isObscured', 'attrAlphaOrder', 'showNonKeyable', 'fullPathName', 'preventOverride', 'height',
                'visible', 'enable', 'lastClickedNode', 'query', 'menuMultiOption', 'numberOfPopupMenus',
                'enableBackground', 'noConnectivity', 'showOutputs', 'pressHighlightsUnconnected', 'annotation',
                'width', 'backgroundColor', 'currentSelection', 'addObject', 'manage', 'lastMenuChoice', 'niceNames',
                'connectivity', 'showInputs', 'replace', 'showNonConnectable', 'noBackground', 'nodesDisplayed',
                'redraw', 'longNames', 'edit', 'popupMenuArray', 'showReadOnly', 'remove', 'removeAll', 'showHidden',
                'multiSelect', 'showPublished', 'showConnectedOnly', 'redrawRow']
    _CALLBACKS = ['addCommand', 'dragCallback', 'dropCallback', 'menuCommand', 'selectCommand', 'visibleChangeCommand']


class OutlinerEditor(Control):
    '''Wrapper class for cmds.outlinerEditor'''
    CMD = cmds.outlinerEditor
    _ATTRIBS = ['attrAlphaOrder', 'allowMultiSelection', 'containersIgnoreFilters', 'showAttributes', 'showSetMembers',
                'doNotSelectNewObjects', 'setsIgnoreFilters', 'highlightSecondary', 'alwaysToggleSelect',
                'showNumericAttrsOnly', 'unpinPlug', 'organizeByLayer', 'query', 'animLayerFilterOptions', 'attrFilter',
                'panel', 'directSelect', 'showMuteInfo', 'highlightActive', 'unlockMainConnection', 'showPinIcons',
                'showReferenceMembers', 'expandConnections', 'showCompounds', 'parentObject',
                'showPublishedAsConnected', 'expandObjects', 'isChildSelected', 'autoSelectNewObjects',
                'showAnimLayerWeight', 'sortOrder', 'autoExpand', 'showAnimCurvesOnly', 'transmitFilters',
                'dropIsParent', 'showContainerContents', 'ignoreDagHierarchy', 'showAssets', 'mainListConnection',
                'forceMainConnection', 'showShapes', 'lockMainConnection', 'showContainedOnly', 'updateMainConnection',
                'showTextureNodesOnly', 'showAttrValues', 'showLeafs', 'displayMode', 'showDagOnly', 'pinPlug',
                'stateString', 'showSelected', 'showNamespace', 'setFilter', 'niceNames', 'highlightConnection',
                'longNames', 'edit', 'object', 'filter', 'editAttrName', 'showConnected', 'showUVAttrsOnly',
                'mapMotionTrails', 'showUpstreamCurves', 'showUnitlessCurves', 'masterOutliner', 'autoExpandLayers',
                'selectionConnection', 'showReferenceNodes']
    _CALLBACKS = ['selectCommand']


class OutlinerPanel(Control):
    '''Wrapper class for cmds.outlinerPanel'''
    CMD = cmds.outlinerPanel
    _ATTRIBS = ['edit', 'outlinerEditor', 'createString', 'editString', 'query']
    _CALLBACKS = ['popupMenuProcedure']


class Panel(Control):
    '''Wrapper class for cmds.panel'''
    CMD = cmds.panel
    _ATTRIBS = ['edit', 'query', 'createString', 'editString']
    _CALLBACKS = ['popupMenuProcedure']


class PanelConfiguration(Control):
    '''Wrapper class for cmds.panelConfiguration'''
    CMD = cmds.panelConfiguration
    _ATTRIBS = ['replaceTypeString', 'createStrings', 'addPanel', 'edit', 'replaceCreateString', 'defaultImage',
                'replaceFixedState', 'removeLastPanel', 'replaceLabel', 'removeAllPanels', 'labelStrings',
                'isFixedState', 'editStrings', 'replaceEditString', 'query', 'typeStrings', 'sceneConfig',
                'numberOfPanels', 'image', 'configString']
    _CALLBACKS = []


class PanelHistory(Control):
    '''Wrapper class for cmds.panelHistory'''
    CMD = cmds.panelHistory
    _ATTRIBS = ['historyDepth', 'edit', 'clear', 'back', 'forward', 'suspend', 'isEmpty', 'wrap', 'query', 'targetPane']
    _CALLBACKS = []


class ScriptedPanel(Control):
    '''Wrapper class for cmds.scriptedPanel'''
    CMD = cmds.scriptedPanel
    _ATTRIBS = ['edit', 'query', 'createString', 'type', 'editString']
    _CALLBACKS = ['popupMenuProcedure']


class SpreadSheetEditor(Control):
    '''Wrapper class for cmds.spreadSheetEditor'''
    CMD = cmds.spreadSheetEditor
    _ATTRIBS = ['attrRegExp', 'allAttr', 'query', 'unlockMainConnection', 'fixedAttrList', 'highlightConnection',
                'forceMainConnection', 'showShapes', 'lockMainConnection', 'updateMainConnection', 'precision',
                'selectedAttr', 'niceNames', 'stateString', 'keyableOnly', 'panel', 'execute', 'longNames', 'edit',
                'filter', 'mainListConnection', 'selectionConnection']
    _CALLBACKS = []


class Visor(Control):
    '''Wrapper class for cmds.visor'''
    CMD = cmds.visor
    _ATTRIBS = ["addFolder", "addNodes", "allowPanningInX", "allowPanningInY", "allowZooming", "command",
                "deleteFolder", "editFolder", "folderList", "menu", "name", "nodeType", "openDirectories", "openFolder",
                "parent", "path", "popupMenuScript", "rebuild", "refreshAllSwatches", "refreshSelectedSwatches",
                "refreshSwatch", "reset", "restrictPanAndZoom", "saveSwatches", "scrollBar", "scrollPercent",
                "selectedGadgets", "showDividers", "showFiles", "showFolders", "showNodes", "stateString", "style",
                "transform", "type"]
    _CALLBACKS = []


class WebBrowser(Control):
    '''Wrapper class for cmds.webBrowser'''
    CMD = cmds.webBrowser
    _ATTRIBS = ['isObscured', 'preventOverride', 'manage', 'back', 'height', 'visible', 'query', 'wrap', 'home', 'find',
                'numberOfPopupMenus', 'enableBackground', 'searchForward', 'noBackground', 'width', 'backgroundColor',
                'forward', 'urlChangedCb', 'enable', 'openURL', 'matchWholeWord', 'stop', 'fullPathName', 'annotation',
                'edit', 'popupMenuArray', 'matchCase', 'reload']
    _CALLBACKS = ['command', 'dragCallback', 'dropCallback', 'visibleChangeCommand']


