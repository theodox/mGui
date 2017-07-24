__author__ = 'Steve'
import maya.cmds as cmds

from mGui.core import Control


class ModelEditor(Control):
    CMD = cmds.modelEditor

    _ATTRIBS = ["activeComponentsXray", "activeOnly", "activeView", "addObjects", "addSelected", "allObjects",
                "backfaceCulling", "bufferMode", "bumpResolution", "camera", "cameraName", "cameraSetup", "cameras",
                "colorMap", "colorResolution", "control", "controlVertices", "cullingOverride", "default",
                "defineTemplate", "deformers", "dimensions", "displayAppearance", "displayLights", "displayTextures",
                "docTag", "dynamicConstraints", "dynamics", "exists", "filter", "fluids", "fogColor", "fogDensity",
                "fogEnd", "fogMode", "fogSource", "fogStart", "fogging", "follicles", "forceMainConnection", "grid",
                "hairSystems", "handles", "headsUpDisplay", "highlightConnection", "hulls", "ignorePanZoom",
                "ikHandles", "interactive", "jointXray", "joints", "lights", "lineWidth", "locators",
                "lockMainConnection", "lowQualityLighting", "mainListConnection", "manipulators",
                "maxConstantTransparency", "modelPanel", "nCloths", "nParticles", "nRigids", "noUndo", "nurbsCurves",
                "nurbsSurfaces", "occlusionCulling", "panel", "parent", "pivots", "planes", "polymeshes",
                "removeSelected", "rendererList", "rendererListUI", "rendererName", "selectionConnection",
                "selectionHiliteDisplay", "setSelected", "shadows", "smoothWireframe", "sortTransparent", "stateString",
                "strokes", "subdivSurfaces", "textureAnisotropic", "textureDisplay", "textureHilight", "textureMaxSize",
                "textureMemoryUsed", "textureSampling", "textures", "transpInShadows", "transparencyAlgorithm",
                "twoSidedLighting", "unParent", "unlockMainConnection", "updateColorMode", "updateMainConnection",
                "useBaseRenderer", "useColorIndex", "useDefaultMaterial", "useInteractiveMode", "useRGBImagePlane",
                "useTemplate", "userNode", "viewObjects", "viewSelected", "viewType", "wireframeBackingStore",
                "wireframeOnShaded", "xray"]

    _CALLBACKS = ["editorChanged"]


class ComponentEditor(Control):
    """Wrapper class for cmds.componentEditor"""
    CMD = cmds.componentEditor
    _ATTRIBS = ['newTab', 'hidePathName', 'query', 'lockMainConnection', 'setOperationLabel', 'lockInput', 'filter',
                'stateString', 'selected', 'hideZeroColumns', 'operationType', 'highlightConnection',
                'forceMainConnection', 'removeTab', 'floatSlider', 'updateMainConnection', 'precision',
                'unlockMainConnection', 'showSelected', 'operationCount', 'panel', 'edit', 'showObjects',
                'selectionConnection', 'floatField', 'mainListConnection', 'sortAlpha', 'operationLabels']
    _CALLBACKS = []


class OutlinerEditor(Control):
    """Wrapper class for cmds.outlinerEditor"""
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


class EditorFactory(object):
    TYPES = {
        'modelEditor': ModelEditor,
        'componentEditor': ComponentEditor,
        'outlinerEditor': OutlinerEditor,
    }

    @classmethod
    def get(cls, editor_string):
        ptype = cmds.objectTypeUI(str(editor_string))
        pfclass = cls.TYPES.get(ptype, None)
        if not pfclass:
            raise RuntimeError("Unknown editor type: {}".format(ptype))
        return pfclass.wrap(editor_string)

__all__ = ['ModelEditor', 'ComponentEditor', 'OutlinerEditor', ]

