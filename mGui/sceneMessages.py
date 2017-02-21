"""
Wraps the various Scene Messages from maya.api.OpenMaya.MSceneMessage
with an mGui.events.Event class.

These are a bit more fine-grained than the higher level events available
through scriptJobs.

Scene message events will also work properly in standalone.

"""
import weakref

from maya.api import OpenMaya as om

from mGui import events
from mGui import properties


## SceneMessageEvent ##
class SceneMessageEvent(events.Event):

    """
    A derivative of the Event class that is attached to a SceneMessage

    Typical usage:

        def handle_before_new_scene(*args, **kwargs):
            # Prep for a new scene
            print("Starting a new scene!")

       sm = SceneMessageEvent(maya.api.OpenMaya.MSceneMessage.kBeforeNew)
       sm += handle_before_new_scene
       sm.start(protected = True)

    to find out if the scene message is still running:

        if sm.running:
            print('Scene Message is still running')

    to stop a scene message:

        sm.kill()

    Added a runOnce flag to the start method, this mimics the scriptJob 
    behavior of only firing the event once.

    """

    add_callback = om.MSceneMessage.addCallback
    message_type = None

    def __init__(self, **data):
        self._run_once = False
        super(SceneMessageEvent, self).__init__(**data)
        self._callback_id = None
        self.data['event'] = weakref.proxy(self)

    def _fire(self, *args, **kwargs):
        super(SceneMessageEvent, self)._fire(*args, **kwargs)
        if self._run_once and self.running():
            self.kill()

    __call__ = _fire

    def start(self, runOnce=False):
        self._run_once = runOnce
        if self._callback_id is None and self.message_type is not None:
            self._callback_id = self.add_callback(self.message_type, weakref.proxy(self))

    def kill(self):
        if self._callback_id is not None:
            self._callback_id = om.MMessage.removeCallback(self._callback_id)

    def running(self):
        return self._callback_id is not None

    def __del__(self):
        self.kill()


class AfterCreateReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterCreateReference


class AfterCreateReferenceAndRecordEdits(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterCreateReferenceAndRecordEdits


class AfterExport(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterExport


class AfterExportReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterExportReference


class AfterFileRead(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterFileRead


class AfterImport(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterImport


class AfterImportReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterImportReference


class AfterLoadReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterLoadReference


class AfterLoadReferenceAndRecordEdits(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterLoadReferenceAndRecordEdits


class AfterNew(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterNew


class AfterOpen(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterOpen


class AfterRemoveReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterRemoveReference


class AfterSave(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterSave


class AfterSceneReadAndRecordEdits(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterSceneReadAndRecordEdits


class AfterSoftwareFrameRender(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterSoftwareFrameRender


class AfterSoftwareRender(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterSoftwareRender


class AfterUnloadReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kAfterUnloadReference


class BeforeCreateReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeCreateReference


class BeforeCreateReferenceAndRecordEdits(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeCreateReferenceAndRecordEdits


class BeforeExport(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeExport


class BeforeExportReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeExportReference


class BeforeFileRead(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeFileRead


class BeforeImport(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeImport


class BeforeImportReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeImportReference


class BeforeLoadReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeLoadReference


class BeforeLoadReferenceAndRecordEdits(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeLoadReferenceAndRecordEdits


class BeforeNew(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeNew


class BeforeOpen(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeOpen


class BeforeRemoveReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeRemoveReference


class BeforeSave(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeSave


class BeforeSoftwareFrameRender(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeSoftwareFrameRender


class BeforeSoftwareRender(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeSoftwareRender


class BeforeUnloadReference(SceneMessageEvent):
    message_type = om.MSceneMessage.kBeforeUnloadReference


class ExportStarted(SceneMessageEvent):
    message_type = om.MSceneMessage.kExportStarted


class MayaExiting(SceneMessageEvent):
    message_type = om.MSceneMessage.kMayaExiting


class MayaInitialized(SceneMessageEvent):
    message_type = om.MSceneMessage.kMayaInitialized


class SoftwareRenderInterrupted(SceneMessageEvent):
    message_type = om.MSceneMessage.kSoftwareRenderInterrupted


## SceneMessageReferenceEvent ##
class SceneMessageReferenceEvent(SceneMessageEvent):
    add_callback = om.MSceneMessage.addReferenceCallback


class AfterCreateReferenceAndRecordEdits(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kAfterCreateReferenceAndRecordEdits


class AfterLoadReference(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kAfterLoadReference


class AfterLoadReferenceAndRecordEdits(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kAfterLoadReferenceAndRecordEdits


class AfterUnloadReference(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kAfterUnloadReference


class BeforeImportReference(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kBeforeImportReference


class BeforeLoadReference(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kBeforeLoadReference


class BeforeLoadReferenceAndRecordEdits(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kBeforeLoadReferenceAndRecordEdits


class BeforeRemoveReference(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kBeforeRemoveReference


class BeforeUnloadReference(SceneMessageReferenceEvent):
    message_type = om.MSceneMessage.kBeforeUnloadReference


## SceneMessageCheckEvent ##
class SceneMessageCheckEvent(SceneMessageEvent):

    """
    This Event wraps the Check Scene Messages.

    These allow for the event to be aborted if any handlers return False.

    """

    add_callback = om.MSceneMessage.addCheckCallback

    def _fire(self, *args, **kwargs):
        """
        Call all handlers.  Any decayed references will be purged.
        """
        results = []
        delenda = []
        for handler in self._handlers:
            try:
                results.append(handler(*args, **self.metadata(kwargs)))
            except events.DeadReferenceError:
                delenda.append(handler)
        self._handlers = self._handlers.difference(set(delenda))

        if self._run_once and self.running():
            self.kill()

        return all(results)

    __call__ = _fire


class BeforeNewCheck(SceneMessageCheckEvent):
    message_type = om.MSceneMessage.kBeforeNewCheck


class BeforeReferenceCheck(SceneMessageCheckEvent):
    message_type = om.MSceneMessage.kBeforeReferenceCheck


class BeforeSaveCheck(SceneMessageCheckEvent):
    message_type = om.MSceneMessage.kBeforeSaveCheck


## SceneMessageCheckFileEvent ##
class SceneMessageCheckFileEvent(SceneMessageCheckEvent):

    add_callback = om.MSceneMessage.addCheckFileCallback


class BeforeCreateReferenceCheck(SceneMessageCheckFileEvent):
    message_type = om.MSceneMessage.kBeforeCreateReferenceCheck


class BeforeExportCheck(SceneMessageCheckFileEvent):
    message_type = om.MSceneMessage.kBeforeExportCheck


class BeforeImportCheck(SceneMessageCheckFileEvent):
    message_type = om.MSceneMessage.kBeforeImportCheck


class BeforeLoadReferenceCheck(SceneMessageCheckFileEvent):
    message_type = om.MSceneMessage.kBeforeLoadReferenceCheck


class BeforeOpenCheck(SceneMessageCheckFileEvent):
    message_type = om.MSceneMessage.kBeforeOpenCheck


## SceneMessageCheckReferenceEvent ##
class SceneMessageCheckReferenceEvent(SceneMessageCheckEvent):
    add_callback = om.MSceneMessage.addCheckReferenceCallback


class BeforeLoadReferenceCheck(SceneMessageCheckReferenceEvent):
    message_type = om.MSceneMessage.kBeforeLoadReferenceCheck
