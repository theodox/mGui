"""
Created on May 2, 2014

@author: Steve
"""

import maya.cmds as cmds
import mGui.events as events
import mGui.properties as properties
from mGui.debugging import Logger
import weakref


class ScriptJobEvent(events.Event):
    """
    A derivative of the Event class that is attached to a Maya scriptJob

    Typical usage:

        def handle_new_object(*args, **kwargs):
            # do something for new object
            print "new object!"
            print args, kwargs

       sj = ScriptJobEvent("e", "DagObjectCreated")
       sj += handle_new_object
       sj.start(protected = True)

    to find out if the scriptJob is still running:

        if sj.running:
            print 'scriptjob is still running'

    to stop a scriptJob:

        sj.kill()

    Run conditions (such as -runOnce, -parent,  or -protected) should be specified when the scriptJob is started.
    """

    def __init__(self, scriptJobFlag, eventType, **kwargs):
        self.script_flag = scriptJobFlag
        self.event_type = eventType
        super(ScriptJobEvent, self).__init__(**kwargs)
        self.data["scriptJob"] = -1

    def start(self, **sjFlags):
        kwargs = {self.script_flag: (self.event_type, self)}
        kwargs.update(sjFlags)
        self.data["scriptJob"] = cmds.scriptJob(**kwargs)
        Logger.info("start scriptJob %s" % self.__class__)

    def kill(self):
        if self.data.get("scriptJob") > 0:
            cmds.scriptJob(k=self.data["scriptJob"])
            self.data["scriptJob"] = -1
            Logger.info("kill scriptJob %s" % self.__class__)

    @property
    def running(self):
        sid = self.data["scriptJob"]
        return sid != -1 and cmds.scriptJob(exists=sid)


# ======================================================================================================================
# Attribute  based script jobs
#
# See maya docs for more on the distinction between scriptJob -e, scriptJob -ct , etc
# ======================================================================================================================


class AttributeChange(ScriptJobEvent):
    def __init__(self, attrib, **kwargs):
        super(AttributeChange, self).__init__("attributeChange", attrib, **kwargs)
        self.attribute = attrib


class AttributeAdded(ScriptJobEvent):
    def __init__(self, attrib, **kwargs):
        super(AttributeAdded, self).__init__("attributeAdded", attrib, **kwargs)
        self.attribute = attrib


class AttributeDeleted(ScriptJobEvent):
    def __init__(self, attrib, **kwargs):
        super(AttributeDeleted, self).__init__("attributeDeleted", attrib, **kwargs)
        self.attribute = attrib


# ======================================================================================================================
# Event based script jobs
#
# See maya docs for more on the distinction between scriptJob -e, scriptJob -ct , etc
# ======================================================================================================================


class ScriptJobE(ScriptJobEvent):
    EVENT = ""

    def __init__(self, **kwargs):
        super(ScriptJobE, self).__init__("e", self.EVENT, **kwargs)


class LinearUnitChanged(ScriptJobE):
    EVENT = "linearUnitChanged"


class TimeUnitChanged(ScriptJobE):
    EVENT = "timeUnitChanged"


class AngularUnitChanged(ScriptJobE):
    EVENT = "angularUnitChanged"


class Undo(ScriptJobE):
    EVENT = "Undo"


class Redo(ScriptJobE):
    EVENT = "Redo"


class TimeChanged(ScriptJobE):
    EVENT = "timeChanged"


class CurrentContainerChange(ScriptJobE):
    EVENT = "currentContainerChange"


class QuitApplication(ScriptJobE):
    EVENT = "quitApplication"


class IdleHigh(ScriptJobE):
    EVENT = "idleHigh"


class Idle(ScriptJobE):
    EVENT = "idle"


class RecentCommandChanged(ScriptJobE):
    EVENT = "RecentCommandChanged"


class ToolChanged(ScriptJobE):
    EVENT = "ToolChanged"


class PostToolChanged(ScriptJobE):
    EVENT = "PostToolChanged"


class ToolDirtyChanged(ScriptJobE):
    EVENT = "ToolDirtyChanged"


class DisplayRGBColorChanged(ScriptJobE):
    EVENT = "DisplayRGBColorChanged"


class AnimLayerRebuild(ScriptJobE):
    EVENT = "animLayerRebuild"


class AnimLayerRefresh(ScriptJobE):
    EVENT = "animLayerRefresh"


class AnimLayerAnimationChanged(ScriptJobE):
    EVENT = "animLayerAnimationChanged"


class AnimLayerLockChanged(ScriptJobE):
    EVENT = "animLayerLockChanged"


class AnimLayerBaseLockChanged(ScriptJobE):
    EVENT = "animLayerBaseLockChanged"


class AnimLayerGhostChanged(ScriptJobE):
    EVENT = "animLayerGhostChanged"


class CameraChange(ScriptJobE):
    EVENT = "cameraChange"


class CameraDisplayAttributesChange(ScriptJobE):
    EVENT = "cameraDisplayAttributesChange"


class SelectionChanged(ScriptJobE):
    EVENT = "SelectionChanged"


class ActiveViewChanged(ScriptJobE):
    EVENT = "ActiveViewChanged"


class SelectModeChanged(ScriptJobE):
    EVENT = "SelectModeChanged"


class SelectTypeChanged(ScriptJobE):
    EVENT = "SelectTypeChanged"


class SelectPreferenceChanged(ScriptJobE):
    EVENT = "SelectPreferenceChanged"


class DisplayPreferenceChanged(ScriptJobE):
    EVENT = "DisplayPreferenceChanged"


class DagObjectCreated(ScriptJobE):
    EVENT = "DagObjectCreated"


class RenderLayerManagerChange(ScriptJobE):
    EVENT = "renderLayerManagerChange"


class RenderLayerChange(ScriptJobE):
    EVENT = "renderLayerChange"


class DisplayLayerManagerChange(ScriptJobE):
    EVENT = "displayLayerManagerChange"


class DisplayLayerAdded(ScriptJobE):
    EVENT = "displayLayerAdded"


class DisplayLayerDeleted(ScriptJobE):
    EVENT = "displayLayerDeleted"


class DisplayLayerVisibilityChanged(ScriptJobE):
    EVENT = "displayLayerVisibilityChanged"


class DisplayLayerChange(ScriptJobE):
    EVENT = "displayLayerChange"


class RenderPassChange(ScriptJobE):
    EVENT = "renderPassChange"


class RenderPassSetChange(ScriptJobE):
    EVENT = "renderPassSetChange"


class RenderPassSetMembershipChange(ScriptJobE):
    EVENT = "renderPassSetMembershipChange"


class PassContributionMapChange(ScriptJobE):
    EVENT = "passContributionMapChange"


class DisplayColorChanged(ScriptJobE):
    EVENT = "DisplayColorChanged"


class LightLinkingChanged(ScriptJobE):
    EVENT = "lightLinkingChanged"


class LightLinkingChangedNonSG(ScriptJobE):
    EVENT = "lightLinkingChangedNonSG"


class SceneSegmentChanged(ScriptJobE):
    EVENT = "SceneSegmentChanged"


class PostSceneSegmentChanged(ScriptJobE):
    EVENT = "PostSceneSegmentChanged"


class SequencerActiveShotChanged(ScriptJobE):
    EVENT = "SequencerActiveShotChanged"


class ColorIndexChanged(ScriptJobE):
    EVENT = "ColorIndexChanged"


class DeleteAll(ScriptJobE):
    EVENT = "deleteAll"


class NameChanged(ScriptJobE):
    EVENT = "NameChanged"


class SymmetricModellingOptionsChanged(ScriptJobE):
    EVENT = "symmetricModellingOptionsChanged"


class SoftSelectOptionsChanged(ScriptJobE):
    EVENT = "softSelectOptionsChanged"


class SetModified(ScriptJobE):
    EVENT = "SetModified"


class LinearToleranceChanged(ScriptJobE):
    EVENT = "linearToleranceChanged"


class AngularToleranceChanged(ScriptJobE):
    EVENT = "angularToleranceChanged"


class NurbsToPolygonsPrefsChanged(ScriptJobE):
    EVENT = "nurbsToPolygonsPrefsChanged"


class NurbsCurveRebuildPrefsChanged(ScriptJobE):
    EVENT = "nurbsCurveRebuildPrefsChanged"


class ConstructionHistoryChanged(ScriptJobE):
    EVENT = "constructionHistoryChanged"


class ThreadCountChanged(ScriptJobE):
    EVENT = "threadCountChanged"


class SceneSaved(ScriptJobE):
    EVENT = "SceneSaved"


class NewSceneOpened(ScriptJobE):
    EVENT = "NewSceneOpened"


class SceneOpened(ScriptJobE):
    EVENT = "SceneOpened"


class SceneImported(ScriptJobE):
    EVENT = "SceneImported"


class PreFileNewOrOpened(ScriptJobE):
    EVENT = "PreFileNewOrOpened"


class PostSceneRead(ScriptJobE):
    EVENT = "PostSceneRead"


class WorkspaceChanged(ScriptJobE):
    EVENT = "workspaceChanged"


class StartColorPerVertexTool(ScriptJobE):
    EVENT = "startColorPerVertexTool"


class StopColorPerVertexTool(ScriptJobE):
    EVENT = "stopColorPerVertexTool"


class Start3dPaintTool(ScriptJobE):
    EVENT = "start3dPaintTool"


class Stop3dPaintTool(ScriptJobE):
    EVENT = "stop3dPaintTool"


class DragRelease(ScriptJobE):
    EVENT = "DragRelease"


class ModelPanelSetFocus(ScriptJobE):
    EVENT = "ModelPanelSetFocus"


class ModelEditorChanged(ScriptJobE):
    EVENT = "modelEditorChanged"


class MenuModeChanged(ScriptJobE):
    EVENT = "MenuModeChanged"


class GridDisplayChanged(ScriptJobE):
    EVENT = "gridDisplayChanged"


class InteractionStyleChanged(ScriptJobE):
    EVENT = "interactionStyleChanged"


class AxisAtOriginChanged(ScriptJobE):
    EVENT = "axisAtOriginChanged"


class CurveRGBColorChanged(ScriptJobE):
    EVENT = "CurveRGBColorChanged"


class SelectPriorityChanged(ScriptJobE):
    EVENT = "SelectPriorityChanged"


class SnapModeChanged(ScriptJobE):
    EVENT = "snapModeChanged"


class NurbsToSubdivPrefsChanged(ScriptJobE):
    EVENT = "nurbsToSubdivPrefsChanged"


class SelectionPipelineChanged(ScriptJobE):
    EVENT = "selectionPipelineChanged"


class PlaybackRangeChanged(ScriptJobE):
    EVENT = "playbackRangeChanged"


class PlaybackRangeSliderChanged(ScriptJobE):
    EVENT = "playbackRangeSliderChanged"


class CurrentSoundNodeChanged(ScriptJobE):
    EVENT = "currentSoundNodeChanged"


class GlFrameTrigger(ScriptJobE):
    EVENT = "glFrameTrigger"


class RebuildUIValues(ScriptJobE):
    EVENT = "RebuildUIValues"


# ======================================================================================================================
# Condition based script jobs
#
# See maya docs for more on the distinction between scriptJob -e, scriptJob -ct , etc
# ======================================================================================================================


class ScriptJobC(ScriptJobEvent):
    CONDITION = ""

    def __init__(self, type, **kwargs):
        """
        initialize with True for -ct, False for -cf, any other value for -cc
        """
        changetype = "cc"
        if type is True:
            changetype = "ct"
        if type is False:
            changetype = "cf"

        super(ScriptJobC, self).__init__(changetype, self.CONDITION, **kwargs)

    def get_state(self):
        return cmds.condition(self.event_type, q=True, st=True)


class PlayingBack(ScriptJobC):
    CONDITION = "playingBack"


class Recording(ScriptJobC):
    CONDITION = "recording"


class DeleteAllCondition(ScriptJobC):
    CONDITION = "deleteAllCondition"


class TimeChangeTemp(ScriptJobC):
    CONDITION = "timeChangeTemp"


class SomethingSelected(ScriptJobC):
    CONDITION = "SomethingSelected"


class AutoKeyframeState(ScriptJobC):
    CONDITION = "autoKeyframeState"


class Delete(ScriptJobC):
    CONDITION = "delete"


class DeleteUndo(ScriptJobC):
    CONDITION = "deleteUndo"


class DeleteRedo(ScriptJobC):
    CONDITION = "deleteRedo"


class IsCurrentRenderLayerChanging(ScriptJobC):
    CONDITION = "isCurrentRenderLayerChanging"


class IsApplyingMemberOverride(ScriptJobC):
    CONDITION = "isApplyingMemberOverride"


class BatchMode(ScriptJobC):
    CONDITION = "BatchMode"


class ReadingFile(ScriptJobC):
    CONDITION = "readingFile"


class RenderingExists(ScriptJobC):
    CONDITION = "RenderingExists"


class PolyCoreExists(ScriptJobC):
    CONDITION = "PolyCoreExists"


class BaseMayaExists(ScriptJobC):
    CONDITION = "BaseMayaExists"


class AnimationExists(ScriptJobC):
    CONDITION = "AnimationExists"


class ImageUIExists(ScriptJobC):
    CONDITION = "ImageUIExists"


class ManipsExists(ScriptJobC):
    CONDITION = "ManipsExists"


class BaseUIExists(ScriptJobC):
    CONDITION = "BaseUIExists"


class FlushingScene(ScriptJobC):
    CONDITION = "flushingScene"


class GoButtonEnabled(ScriptJobC):
    CONDITION = "GoButtonEnabled"


class ModelExists(ScriptJobC):
    CONDITION = "ModelExists"


class DatabaseUIExists(ScriptJobC):
    CONDITION = "DatabaseUIExists"


class DynamicsExists(ScriptJobC):
    CONDITION = "DynamicsExists"


class KinematicsExists(ScriptJobC):
    CONDITION = "KinematicsExists"


class PolygonsExists(ScriptJobC):
    CONDITION = "PolygonsExists"


class PolyTextureExists(ScriptJobC):
    CONDITION = "PolyTextureExists"


class SubdivExists(ScriptJobC):
    CONDITION = "SubdivExists"


class NurbsExists(ScriptJobC):
    CONDITION = "NurbsExists"


class DeformersExists(ScriptJobC):
    CONDITION = "DeformersExists"


class Busy(ScriptJobC):
    CONDITION = "busy"


class UndoAvailable(ScriptJobC):
    CONDITION = "UndoAvailable"


class RedoAvailable(ScriptJobC):
    CONDITION = "RedoAvailable"


class Opening(ScriptJobC):
    CONDITION = "opening"


class WritingFile(ScriptJobC):
    CONDITION = "writingFile"


class Newing(ScriptJobC):
    CONDITION = "newing"


class PostSceneCallbacks(ScriptJobC):
    CONDITION = "postSceneCallbacks"


class OpenMayaExists(ScriptJobC):
    CONDITION = "OpenMayaExists"


class ReadingReferenceFile(ScriptJobC):
    CONDITION = "readingReferenceFile"


class AlwaysWriteReferenced(ScriptJobC):
    CONDITION = "alwaysWriteReferenced"


class RenderingUIExists(ScriptJobC):
    CONDITION = "RenderingUIExists"


class ExplorerExists(ScriptJobC):
    CONDITION = "ExplorerExists"


class Playblasting(ScriptJobC):
    CONDITION = "playblasting"


class DimensionsExists(ScriptJobC):
    CONDITION = "DimensionsExists"


class ClipEditorExists(ScriptJobC):
    CONDITION = "ClipEditorExists"


class AnimationUIExists(ScriptJobC):
    CONDITION = "AnimationUIExists"


class MayaCreatorExists(ScriptJobC):
    CONDITION = "MayaCreatorExists"


class ModelUIExists(ScriptJobC):
    CONDITION = "ModelUIExists"


class KinematicsUIExists(ScriptJobC):
    CONDITION = "KinematicsUIExists"


class SubdivUIExists(ScriptJobC):
    CONDITION = "SubdivUIExists"


class DynamicsUIExists(ScriptJobC):
    CONDITION = "DynamicsUIExists"


class NurbsUIExists(ScriptJobC):
    CONDITION = "NurbsUIExists"


class SurfaceUIExists(ScriptJobC):
    CONDITION = "SurfaceUIExists"


class DeformersUIExists(ScriptJobC):
    CONDITION = "DeformersUIExists"


class PolygonsUIExists(ScriptJobC):
    CONDITION = "PolygonsUIExists"


class SoftSelectOptions(ScriptJobC):
    CONDITION = "softSelectOptions"


class PanZoomEnabled(ScriptJobC):
    CONDITION = "panZoomEnabled"


class PlaybackIconsCondition(ScriptJobC):
    CONDITION = "playbackIconsCondition"


class HotkeyListChange(ScriptJobC):
    CONDITION = "hotkeyListChange"


class CustomCondition(ScriptJobC):
    """
    Create a ScriptJobC for a named condition other than the predefined ones in Maya.  See the documentation
    for cmds.condition for how to create a named condition.
    """

    def __init__(self, conditionName, type):
        super(CustomCondition, self).__init__(conditionName, type)


# ======================================================================================================================
# Property Descriptor
# used by all ScriptJobEvent classes


class ScriptJobCallbackProperty(properties.CallbackProperty):
    """
    A property descriptor that creates a scriptJob and a corresponding ScriptJobEvent

    The scriptJob must be able to take an object as it's second argument
    """

    def __init__(self, key, scriptFlag, **run_flags):
        self.script_flag = scriptFlag
        self.run_flags = run_flags
        super(ScriptJobCallbackProperty, self).__init__(key)

    def __get__(self, obj, objtype):
        cb = obj.callbacks.get(self.key, None)

        if cb is None:
            new_cb = ScriptJobEvent(self.script_flag, str(obj), sender=weakref.proxy(obj))
            obj.callbacks[self.key] = new_cb
            new_cb.start(**self.run_flags)

        return obj.callbacks[self.key]

    def __set__(self, obj, sjEvent):
        if not isinstance(sjEvent, ScriptJobEvent):
            raise ValueError("Callback properties must be instances of mGui.scriptJobs.ScriptJobEvent")
        obj.callbacks[self.key] = sjEvent
        if not sjEvent.running:
            sjEvent.start(**self.run_flags)
