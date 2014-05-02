'''
Created on May 2, 2014

@author: Steve
'''

import maya.cmds as cmds
import mGui.events as events
import mGui.properties as properties


class ScriptJobEvent(events.Event):

    '''
    A derivative of the Event class that is attached to a Maya scriptJob
    '''
    def __init__(self, scriptJobFlag, parent, **kwargs):
        self.ScriptFlag = scriptJobFlag
        self.Parent = parent
        super(ScriptJobEvent, self).__init__(**kwargs)
        self.Data['scriptJob'] = -1

    def start(self, **sjFlags):
        kwargs = {self.ScriptFlag: (self.Parent, self)}
        kwargs.update(sjFlags)
        self.Data['scriptJob'] = cmds.scriptJob(**kwargs)

    def kill(self):
        if self.Data.get('scriptJob') > 0:
            cmds.scriptJob(k=self.Data['scriptJob'])
            self.Data['scriptJob'] = -1

    @property
    def running(self):
        sid = self.Data['scriptJob']
        return sid != -1 and cmds.scriptJob(exists=sid)


class ScriptJobCallbackProperty(properties.CallbackProperty):
    '''
    A property descriptor that creates a scriptJob and a corresponding ScriptJobEvent

    The scriptJob must be take an object as it's second argument
    '''
    def __init__(self, key, scriptFlag):
        self.ScriptFlag = scriptFlag
        super(ScriptJobCallbackProperty, self).__init__(key)

    def __get__(self, obj, objtype):
        cb = obj.Callbacks.get(self.Key, None)

        if cb is None:
            new_cb = ScriptJobEvent(self.ScriptFlag, str(obj), sender=obj)
            obj.Callbacks[self.Key] = new_cb
            new_cb.start()

        return obj.Callbacks[self.Key]

    def __set__(self, obj, sjEvent):
        if not isinstance(sjEvent, ScriptJobEvent):
            raise ValueError('Callback properties must be instances of mGui.scriptJobs.ScriptJobEvent')
        obj.Callbacks[self.Key] = sjEvent
        if not sjEvent.running:
            sjEvent.start()

