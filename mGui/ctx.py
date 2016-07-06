"""
This module is for scriptCtx based tools
"""
import maya.cmds as cmds
import maya.mel
import maya.utils as utils
from mGui.scriptJobs import SelectionChanged
from mGui.events import Event
from mGui.bindings import BindingContext
from mGui.debugging import Logger

ALL_SELECT_MODES = """
component
hierarchical
leaf
object
preset
root
template
""".split()

ALL_SELECT_TYPES = """animBreakdown
animCurve
animInTangent
animKeyframe
allComponents
allObjects
animOutTangent
curve
camera
curveKnot
cluster
collisionModel
curveOnSurface
curveParameterPoint
controlVertex
dynamicConstraint
dimension
edge
emitter
editPoint
facet
field
fluid
follicle
handle
hull
hairSystem
ikEndEffector
implicitGeometry
ikHandle
imagePlane
isoparm
joint
jointPivot
lattice
locator
latticePoint
light
locatorUV
meshComponents
meshUVShell
motionTrailPoint
motionTrailTangent
nurbsCurve
nCloth
nonlinear
nParticle
nParticleShape
nRigid
nurbsSurface
orientationLocator
polymesh
polymeshEdge
polymeshFace
polymeshFreeEdge
plane
particle
particleShape
polymeshUV
polymeshVertex
polymeshVtxFace
localRotationAxis
rigidBody
rigidConstraint
rotatePivot
sculpt
subdiv
surfaceEdge
surfaceFace
selectHandle
surfaceKnot
scalePivot
springComponent
surfaceParameterPoint
spring
surfaceRange
stroke
surfaceUV
texture
vertex
locatorXYZ""".split()


class ToolEvent(Event):
    REGISTRY = {}

    @classmethod
    def create(cls, name, *args, **kwargs):
        cls.REGISTRY[name] = cls(*args, **kwargs)
        return cls.REGISTRY[name]

    @classmethod
    def fire(cls, name):
        target_event = cls.REGISTRY.get(name)
        if target_event:
            target_event()
        else:
            cmds.warning("no event for %s" % name)

    @classmethod
    def delete_tool(cls, tool):
        for v in cls.REGISTRY.values():
            v -= tool.start
            v -= tool.finish
            v -= tool.exit
            if hasattr(tool, 'values'):
                v -= tool.values
            if hasattr(tool, 'create_property_ui'):
                v -= tool.create_property_ui


class ComponentSelectionTracker(object):
    """
    A variant of ScriptContextOptions which tracks component selections in user selected order -- the stupid mel
    callback system makes this extremely awkward to do in the tool scripts themselves, so it's easier to just use this.
    """

    def __init__(self):
        self.selected = []
        self.watcher = None

    def track_selection(self, *_, **__):
        new_sel = cmds.ls(sl=True, fl=True, l=True) or []
        results = []
        for item in self.selected:
            if item in new_sel:
                results.append(item)
        for item in new_sel:
            if not item in results:
                results.append(item)
        self.selected = results
        Logger.debug("selection %s" % self.selected)

    def start(self, *args, **kwargs):
        Logger.debug("starting selection watcher")
        self.watcher = SelectionChanged()
        self.watcher += self.track_selection
        self.selected = cmds.ls(sl=True, fl=True, l=True) or []
        self.watcher.start()

    def finish(self):
        # reserved for future needs
        self.track_selection()
        if self.watcher and self.watcher.running:
            self.watcher.kill()

    def exit(self, *args, **kwargs):
        self.track_selection()
        if self.watcher and self.watcher.running:
            self.watcher.kill()

    def component_selection(self):
        return [i for i in self.selected]


class Tool(object):
    """
    Represents a scriptContext tool
    """
    REGISTRY = {}  # don't override this in derived -- always use the Tool version
    ICON = ''
    START = 'start'
    FINISH = 'finish'
    EXIT = 'exit'
    PROPERTIES = 'properties'
    VALUES = 'values'

    EVENT_PREFIX = 'tool'  # give each derived tool a unique name

    def __init__(self, name):
        self.name = name
        self.context_name = None
        self.repeat = False
        self.select_mode = None
        self.select_type = None

        def hook_event(name, function):
            event_name = lambda name: self.EVENT_PREFIX + "_" + name
            ev = ToolEvent.create(event_name(name))
            ev += function

        hook_event(self.START, self.start)
        hook_event(self.FINISH, self.finish)
        hook_event(self.EXIT, self.exit)

        # if the derived class implements 'properties' and 'values' methods
        if hasattr(self, 'create_property_ui'):
            hook_event(self.PROPERTIES, self.create_property_ui)
            hook_event(self.VALUES, self.values)

        Tool.REGISTRY[self.name] = self

    def create_context(self, contextOptions, repeat=False):
        """
        Create a context hooked to the events for this instance
        """
        props = hasattr(self, 'create_property_ui') or None
        vals = hasattr(self, 'values') or None
        if not props == vals:
            raise RuntimeError('Tool classes with custom properties must implement both properties() and values()')

        if props and vals:
            props = self.PROPERTIES
            vals = self.VALUES

        opts = contextOptions.options(self.EVENT_PREFIX, self.START, self.FINISH, self.EXIT, props, vals)
        opts['title'] = self.name
        context_name = cmds.scriptCtx(**opts)
        Tool.REGISTRY[context_name] = self
        self.context_name = context_name
        self.repeat = repeat
        return context_name

    def start(self, *args, **kwargs):
        pass

    def exit(self, *args, **kwargs):
        utils.executeDeferred(self.reset_select_mask)
        if self.repeat:
            lazy_reset = lambda: cmds.setToolTo(self.context_name)
            utils.executeDeferred(lazy_reset)


    def finish(self, *args, **kwargs):
        pass

    @classmethod
    def retrieve(cls, name_or_context):
        return Tool.REGISTRY.get(name_or_context, None)

    @classmethod
    def delete(cls, name_or_context):
        target = cls.retrieve(name_or_context)
        if target is not None:
            ToolEvent.delete_tool(target)
            for k, v in Tool.REGISTRY.items():
                if v == target:
                    del (Tool.REGISTRY[k])

    def set_select_mode(self, *types):
        """
        replace the existing selection mode (object, component etc) with the types supplied.  Cache the existing mode
        for later restore
        """
        self.select_mode = {k: cmds.selectMode(**{'q': 1, k: 1}) for k in ALL_SELECT_MODES}
        options = {k: k in types for k in ALL_SELECT_MODES}
        cmds.selectMode(**options)

    def set_select_types(self, *types):
        """
        replace the existing selection type (face, vertex, etc) with the types supplied.  Cache the existing types for
        later restore
        """
        self.select_type = {k: cmds.selectType(**{'q': 1, k: 1}) for k in ALL_SELECT_TYPES}
        options = {k: k in types for k in ALL_SELECT_TYPES}
        cmds.selectType(**options)

    def reset_select_mask(self):
        """
        resets any selection modes set by this tool
        """
        if self.select_mode:
            cmds.selectMode(**self.select_mode)
            self.select_mode = None
        if self.select_type:
            cmds.selectType(**self.select_type)
            self.select_type = None


class SelectionTrackingTool(Tool):
    """
    This is a variant of the base tool which includes a ComponentSelectionTracker so that
     it can track serial selections. It preserves selection order to support component selection tools
     (it's hard to do this in Python otherwise)

     You need to remember to call these via super() when implementing start(), finish() and exit() in
     derived classes to make sure that the selection is properly tracked
    """

    def __init__(self, name):
        super(SelectionTrackingTool, self).__init__(name)
        self.tracker = ComponentSelectionTracker()
        self._inner_selection = []

    def start(self, *args, **kwargs):
        super(SelectionTrackingTool, self).start(*args, **kwargs)
        self.tracker.start()

    def finish(self, *args, **kwargs):
        # currently a nullop
        # reserve for future needs
        self._inner_selection = self.tracker.component_selection()
        self.tracker.finish()
        super(SelectionTrackingTool, self).finish(*args, **kwargs)

    def exit(self, *args, **kwargs):
        # have to grab these before the tracker shuts down...
        self._inner_selection = self.tracker.component_selection()
        self.tracker.exit()
        super(SelectionTrackingTool, self).exit(*args, **kwargs)

    def component_selection(self):
        return self._inner_selection


class UITool(object):
    @property
    def binding_context(self):
        """
        createa BindingContext if needed
        """
        if not hasattr(self, '_bind_ctx'):
            self._bind_ctx = BindingContext()
        return self._bind_ctx

    def create_property_ui(self, *_, **__):
        """
        override this in derived classes to create gui.

        You'll need to attach your gui to the results of set_ui_parent() and then
        close by activating the tab using set_active() as shown below
        """
        prop_sheet = self.set_ui_parent()
        cmds.columnLayout(self.name)
        cmds.text("no properties")
        cmds.setParent("..")
        self.set_active()

    def values(self, *_, **__):
        # this will probably never be needed,
        # but if it is, override this
        pass

    def set_ui_parent(self):
        prop = cmds.toolPropertyWindow(q=True, loc=True)
        cmds.setParent(prop)
        return prop

    def set_active(self):
        prop = cmds.toolPropertyWindow(q=True, loc=True)
        cmds.tabLayout(prop, e=True, selectTab=self.name)


# ---------------------------------------------
# convenience constants

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


# ----------------------------------------------
# helper classes for use in assembling contexts

class StructuredOptionProperty(object):
    """
    propety accessor for StructuredOptions.  This is used
    to keep all the boilerplated for defaults, etc in one place
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
    Make all StructuredOptions use StructuredOptionsProperties
    """

    def __new__(cls, name, bases, kwargs):
        class_props = {'_PROPERTIES': []}
        for k, v in kwargs.items():
            if isinstance(v, tuple):
                new_prop = StructuredOptionProperty(k, v[0], v[1])
                class_props[k] = new_prop
                class_props['_PROPERTIES'].append(new_prop)
            else:
                class_props[k] = v
        return type.__new__(cls, name, bases, class_props)


class StructuredOptionSet(object):
    """
    Base class for structured options. They are just a clean way
    to assemble the dictionary of options needed by the scriptCtx
    command
    """
    __metaclass__ = StructuredOptionsMeta

    def value(self):
        results = {}
        for v in self._PROPERTIES:
            results[v.flag] = v.__get__(self, None)
        return results


class PromptOptions(StructuredOptionSet):
    """
    The prompts for a selection set
    """
    prompt = 'ssp', ''
    unselected = 'snp', 'select something'
    completed = 'dsp', 'selection completed'
    hud_prompt = 'ssh', ''
    hud_unselected = 'snh', ''


class SelectionSetOptions(StructuredOptionSet):
    """
    A selection set. A finished context includes at least one
    and possibly more of these
    """
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


class ScriptContextFactory(StructuredOptionSet):
    """
    Collect selection sets into a single dictionary to be fed to the ScriptCtx command.
    """
    cursor = 'tct', Cursors.track
    exit_on_completion = 'euc', True
    ignore_invalid = 'iii', True
    root_select = 'ers', False
    show_manips = 'sm', False
    cumulative = 'cls', True
    image1 = 'image1', 'pythonFamily.png'
    image2 = 'image2', ''
    image3 = 'image3', ''

    def __init__(self, *selectionSets):
        self.sets = selectionSets

    def options(self, tool_class, start_name, finish_name, exit_name, props_name, vals_name):
        result = self.value()

        result['tss'] = len(self.sets)
        opt_flags = ['snp', 'ssp', 'dsp', 'snh', 'ssh', 'ssc', 'sac', 'sat']
        for flag in opt_flags:
            result[flag] = []
        for each_set in self.sets:
            tmp = each_set.value()
            for opt in opt_flags:
                result[opt].append(tmp[opt])

        def generate_event_callback(classname, tool_name):
            long_name = classname + "_" + tool_name
            return '''python("from mGui.ctx import ToolEvent; ToolEvent.fire('%s')")''' % long_name

        result['ts'] = generate_event_callback(tool_class, start_name)
        result['tf'] = generate_event_callback(tool_class, finish_name)
        result['fcs'] = generate_event_callback(tool_class, exit_name)

        if props_name:
            # if custom properties are provided, define mel proxies
            result['bcn'] = tool_class
            prop_event = generate_event_callback(tool_class, props_name)
            val_event = generate_event_callback(tool_class, vals_name)
            maya.mel.eval("""global proc %sProperties(){%s;}""" % (tool_class, prop_event))
            maya.mel.eval("""global proc %sValues(string $toolName){%s;}""" % (tool_class, val_event))

        return result
