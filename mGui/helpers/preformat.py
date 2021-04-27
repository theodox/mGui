"""
mGui.helpers.tools

This module provides services that can be useful of r
"""

import maya.mel as mel

from . import constants
import mGui.core as core
from io import StringIO

_is_widget = lambda helptext: "dragCallback" in helptext
_is_layout = lambda helptext: "childArray" in helptext
__layout_cmds = []  # filled out on module initialize
__control_cmds = []  # filled out on module initialize
for item in mel.eval('help -list "*"'):
    help = mel.eval("help %s" % item)
    if _is_widget(help):
        if _is_layout(help):
            __layout_cmds.append(item)
        else:
            __control_cmds.append(item)


class CommandInfo(object):
    """
    This class uses the mel help strings for commands to generate class wrapper classes
    """

    DEFAULTS = core.Control._ATTRIBS + core.Control._READ_ONLY
    INHERITS = "Control"

    def __init__(self, name, **flags):
        self.Name = name
        self.Flags = flags

    def collect_callbacks(self, attribs):
        callbacks = [c for c in attribs if "ommand" in c or "allback" in c]
        return callbacks

    def template(self):
        code = StringIO()
        code.write("class %s(%s):\n" % (self.Name[0].upper() + self.Name[1:], self.INHERITS))
        code.write("    '''Wrapper class for cmds.%s'''\n" % self.Name)
        code.write("    CMD = cmds.%s\n" % self.Name)
        attribs = [k for k in self.Flags.values() if not k in self.DEFAULTS]
        attribs.sort()
        callbacks = self.collect_callbacks(attribs)
        attribs = list(set(attribs) - set(callbacks))
        quoted = lambda p: "'%s'" % p
        attrib_names = list(map(quoted, attribs))
        code.write("    _ATTRIBS = [%s]\n" % ",".join(attrib_names))
        callback_names = list(map(quoted, callbacks))
        code.write("    _CALLBACKS = [%s]\n" % ",".join(callback_names))
        return code.getvalue()

    @classmethod
    def from_command(cls, commandname):
        if hasattr(commandname, "__name__"):
            commandname = commandname.__name__
        helptext = mel.eval("help %s;" % commandname)
        if not helptext:
            raise RuntimeError('no command "%s" found' % commandname)
        results = {}
        for line in helptext.split("\n")[4:-2]:
            tokens = line.split()
            if len(tokens) > 1:
                results[str(tokens[0][1:])] = str(tokens[1][1:])
        return cls(commandname, **results)


class LayoutInfo(CommandInfo):
    DEFAULTS = core.Layout._ATTRIBS + core.Layout._READ_ONLY
    INHERITS = "Layout"


class PanelInfo(CommandInfo):
    DEFAULTS = [
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
    INHERITS = "Control"

    def collect_callbacks(self, attribs):
        callbacks = [c for c in attribs if "rocedure" in c or "allback" in c or "ommand" in c]
        return callbacks

    def get_editor(seelf, attriblist):
        editors = [e for e in attriblist if e.endswith("Editor")]
        for e in editors:
            attriblist.remove(e)
        return editors

    def template(self):
        base = CommandInfo().template()
        editor_cmd = """'    make_editor_command(cmds.%s, '%s')\n/"""
        return base + editor_cmd


def generate_controls(filename):
    with open(filename, "wt") as filehandle:
        filehandle.write("'''\nmGui wrapper classes\n\nAuto-generated wrapper classes for use with mGui\n'''\n\n")
        filehandle.write("import maya.cmds as cmds\n")
        filehandle.write("from .core import Control\n")

        for each_class in constants.CONTROL_COMMANDS:
            try:
                filehandle.write(CommandInfo.from_command(each_class).template())
                filehandle.write("\n\n")
            except RuntimeError:
                filehandle.write("# command '%s' not present in this maya" % each_class)


def generate_layouts(filename):
    with open(filename, "wt") as filehandle:
        filehandle.write("'''\nmGui wrapper classes\n\nAuto-generated wrapper classes for use with mGui\n'''\n\n")
        filehandle.write("import maya.cmds as cmds\n")
        filehandle.write("from .core import Layout\n\n")
        for each_class in constants.LAYOUT_COMMANDS:
            try:
                filehandle.write(LayoutInfo.from_command(each_class).template())
                filehandle.write("\n\n")
            except RuntimeError:
                filehandle.write("# command '%s' not present in this maya" % each_class)


def generate_panels(filename):
    with open(filename, "wt") as filehandle:
        filehandle.write("'''\nmGui wrapper classes\n\nAuto-generated wrapper classes for use with mGui\n'''\n\n")
        filehandle.write(
            """
        import maya.cmds as cmds
        from mGui.core import Control
        from mGui.core.editors import EditorFactory
        from mGui.properties import WrappedCtlProperty
        def make_editor_command(cmd, editorString):
            return WrappedCtlProperty(editorString, cmd, True, EditorFactory.get)
        """
        )

        for each_class in constants.PANEL_COMMANDS:
            try:
                filehandle.write(PanelInfo.from_command(each_class).template())
                filehandle.write("\n\n")

            except RuntimeError:
                filehandle.write("# command '%s' not present in this maya" % each_class)

        filehandle.write(
            """
        class PanelFactory(object):
            TYPES = {
                'modelPanel': ModelPanel,
                'hardwareRenderPanel': HardwareRenderPanel,
                'hyperGraph': HyperGraph,
                'hyperPanel': HyperPanel,
                'hyperShade': HyperShade,
                'nodeOutliner': NodeOutliner,
                'outlinerPanel': OutlinerPanel,
                'panelConfiguration': PanelConfiguration,
                'panelHistory': PanelHistory,
                'scriptedPanel': ScriptedPanel,
                'spreadSheetEditor': SpreadSheetEditor,
                'visor': Visor
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
                return pfclass.wrap(panel_string, panel_string)\n"""
        )
