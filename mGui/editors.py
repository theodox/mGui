__author__ = 'Steve'
import maya.cmds as cmds

import mGui.core as core


class ModelEditor(core.Control):
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


class Panel(core.Control):
    CMD = cmds.panel
    PANEL_TYPE = None
    _ATTRIBS = ["copy", "defineTemplate", "docTag", "exists", "init", "label", "menuBarVisible",
                "needsInit", "parent", "replacePanel", "tearOff", "tearOffCopy", "unParent", "useTemplate"]
    _READONLY = ["control", "isUnique"]
    _CALLBACKS = ["popupMenuProcedure"]


class ModelPanel(Panel):
    CMD = cmds.modelPanel
    PANEL_TYPE = 'modelPanel'

    _ATTRIBS = ["barLayout", "camera", "copy", "defineTemplate", "docTag", "exists", "init", "label", "menuBarVisible",
                "modelEditor", "needsInit", "parent", "replacePanel", "tearOff", "tearOffCopy", "unParent",
                "useTemplate"]
    _READONLY = ["control", "isUnique"]
    _CALLBACKS = ["popupMenuProcedure"]



class PanelFactory(object):
    TYPES = {'modelPanel': ModelPanel}

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
        return pfclass.from_existing(panel_string, panel_string)

    @classmethod
    def register_type(cls, type_string, type_class):
        cls[type_string] = type_class
