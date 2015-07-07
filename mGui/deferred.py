"""
This module exposes a single event callback, which fires on a maya idle event.  It's intended to be used as a way to
trigger things like menu or ui loads once the main Maya UI is initialized.
"""
from mGui.events import MayaEvent
import maya.cmds as cmds

Maya_is_ready = MayaEvent()

class MayaUIStatus(object):
    """
    This object can be used to check to see if the maya UI has finished booting. When the UI has loaded,
    MayaUIStatus.ready will be True; until them it will be false
    """
    ready = False

    @classmethod
    def maya_is_ready(cls, *args, **kwargss):
        cls.ready = True


cmds.scriptJob(e=('idle', Maya_is_ready), runOnce=True)
Maya_is_ready += MayaUIStatus.maya_is_ready
