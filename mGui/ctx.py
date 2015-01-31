"""
This module is for scriptCtx based tools
"""
import maya.cmds as cmds

import mGui.runtimeCommands as rtc

# ----------------------------------------------
# helper classes for use in assembling contexts

class StructuredOptionProperty(object):
    """
    propety accessor
    """

    def __init__(self, key, flag, default):
        self.key = "_prop_" + key
        self.flag = flag
        self.default = default

    def __get__(self, instance, owner):
        if not hasattr(instance, self.key):
            self.__set__(instance, self.default)
        return getattr(instance, self.key)

    def __set__(self, instance, value):
        setattr(instance, self.key, value)


class StructuredOptionsMeta(type):
    """
    metaclass for cleaner creation of option flags
    """

    def __new__(cls, name, bases, kwargs):
        class_props = {'_PROPERTIES': []}

        for k, v in kwargs.items():
            print k, v
            if isinstance(v, tuple):
                new_prop = StructuredOptionProperty(k, v[0], v[1])
                class_props[k] = new_prop
                class_props['_PROPERTIES'].append(new_prop)
            else:
                class_props[k] = v
        return type.__new__(cls, name, bases, class_props)


class StructuredOptionSet(object):
    """
    base class for structured options
    """
    __metaclass__ = StructuredOptionsMeta

    def value(self):
        results = {}
        for v in self._PROPERTIES:
            results[v.flag] = v.__get__(self, None)
        return results


class Cursors(object):
    """
    The available cursors for scriptCtx commands
    """
    create = "create"
    dolly = "dolly"
    edit = "edit"
    pencil = "pencil"
    track = "track"
    trackHorizontal = "trackHorizontal"
    trackVertical = "trackVertical"
    transformation = "transformation"
    tumble = "tumble"
    zoom = "zoom"
    zoomIn = "zoomIn"
    zoomOut = "zoomOut"
    flyThrough = "flyThrough"
    dot = "dot"
    fleur = "fleur"
    leftArrow = "leftArrow"
    question = "question"
    doubleHorizArrow = "doubleHorizArrow"
    doubleVertArrow = "doubleVertArrow"
    sizing = "sizing"
    dollyIn = "dollyIn"
    dollyOut = "dollyOut"
    brush = "brush"
    camera = "camera"
    noAccess = "noAccess"
    input = "input"
    output = "output"
    leftCycle = "leftCycle"
    rightCycle = "rightCycle"
    rightExpand = "rightExpand"
    knife = "knife"


#------------------------------------------------
# build contexts out of these classes

class PromptOptions(StructuredOptionSet):
    prompt = 'ssp', ''
    unselected = 'snp', 'select something'
    completed = 'dsp', 'selection completed'
    hud_prompt = 'ssh', ''
    hud_unselected = 'snh', 'select something'


class SelectionSetOptions(StructuredOptionSet):
    autocomplete = 'sac', False
    toggle = 'sat', False
    allow_excess = 'sae', False
    count = 'ssc', 0

    def __init__(self, prompt):
        self.prompt = prompt

    def value(self):
        result = super(SelectionSetOptions, self).value()
        result.update(self.prompt.value())
        return result

class ScriptContextOptions(StructuredOptionSet):
    cursor = 'tct', Cursors.edit
    exit_on_completion = 'euc', False
    ignore_invalid = 'iii', True
    root_select = 'ers', False
    show_manips = 'sm', False
    cumulative = 'cls', True

    def __init__(self, *selectionSets):
        self.sets = selectionSets

    def value(self):
        result = super(ScriptContextOptions, self).value()
        result['tss'] = len(self.sets)
        opt_flags = ['snp', 'ssp', 'dsp', 'snh', 'ssh', 'ssc', 'sac', 'sat']
        for flag in opt_flags:
            result[flag] = []
        for each_set in self.sets:
            tmp = each_set.value()
            for opt in opt_flags:
                result[opt].append(tmp[opt])

        result['ts'] = rtc.create_runtime_command(self.__class__.__name__ + "_tool_start", self.__class__.start)
        result['tf'] = rtc.create_runtime_command(self.__class__.__name__ + "_tool_finish", self.__class__.finish)
        result['fcs'] = rtc.create_runtime_command(self.__class__.__name__ + "_tool_exit", self.__class__.exit)

        return result

    def create(self, title):
        opts = self.value()
        opts['title'] = title
        return cmds.scriptCtx(**opts)

    @classmethod
    def start(cls):
        raise NotImplementedError

    @classmethod
    def finish(cls):
        raise NotImplementedError

    @classmethod
    def exit(cls):
        raise NotImplementedError

