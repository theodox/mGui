"""
mGui.helpers.tools

Utility code for generating a complete copy of all the commands and layouts in the maya gui toolkit.

In ordinary circumstance you won't need to run this if you're using
mGui.controls and mGui.layouts, which were generated using the tools here.
However it may be useful to be able to rebuild those modules from scratch if
you're trying to make significant changes to the library.


(c) 2014 Steve Theodore - see mGui/__init__.py for MIT license details
"""


import maya.mel as mel
from StringIO import StringIO
import constants
        

_is_widget  = lambda helptext: 'dragCallback' in helptext
_is_layout = lambda helptext: 'childArray' in helptext
__layout_cmds = []  # filled out on module initialize
__control_cmds = [] # filled out on module initialize
for item in mel.eval('help -list "*"'):
    help = mel.eval('help %s' % item)
    if _is_widget(help):
        if _is_layout(help):
            __layout_cmds.append(item)
        else:
            __control_cmds.append(item)



                      

class CommandInfo(object):
    """
    This class uses the mel help strings for commands to generate class wrapper classes
    """
    DEFAULTS = constants.CONTROL_ATTRIBS
    INHERITS = 'Control'
    
    
    def __init__(self, name, **flags ):
        self.Name = name
        self.Flags = flags
    
    def template(self, includeShortNames = False):
        """
        produces a string containing a complete class definition for a class derived from mGui.core.Control, such as:
        
            class AttrColorSliderGrp(Control):
                ''Wrapper class for cmds.attrColorSliderGrp''
                 CMD = cmds.attrColorSliderGrp
                 _ATTRIBS = ['attribute','rowAttach','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','adjustableColumn','columnAlign','columnAttach6','adjustableColumn5','adjustableColumn2','adjustableColumn3','adjustableColumn4','showButton','hsvValue','columnWidth','adjustableColumn6','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','rgbValue','attrNavDecision','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
                 _CALLBACKS = []

        @note the _ATTRIBS class field is usually over the pep-8 width limit. Sorry.
        """
        
        code = StringIO()
        code.write('class %s(%s):\n' % (self.Name[0].upper() + self.Name[1:], self.INHERITS))
        code.write("    '''Wrapper class for cmds.%s'''\n"  % self.Name)
        code.write('    CMD = cmds.%s\n' % self.Name)
        attribs = [k for k in self.Flags.values() if not k in self.DEFAULTS]
        if includeShortNames:
            attribs += [k for k in self.Flags.keys() if not k in self.DEFAULTS]
            
        attribs.sort()
        # note this deliberately excludes short names of callbacks!
        callback_exceptions = { 'alwaysInvokeEnterCommandOnReturn' }
        callbacks = { c for c in attribs if 'Command' in c or 'Callback' in c }  - callback_exceptions
        attribs = list(set(attribs) - callbacks)
        quoted = lambda p : "'%s'" % p
        attrib_names = map (quoted, attribs)
        code.write('    _ATTRIBS = [%s]\n' %','.join(attrib_names))
        callback_names = map (quoted, callbacks)
        code.write('    _CALLBACKS = [%s]\n' %','.join(callback_names))
        return code.getvalue()
        
    @classmethod    
    def from_command(cls, commandname):
        """
        generate a CommandInfo object from a maya command name string OR a maya cmd from the cmds module
        """
        if hasattr(commandname, "__name__"): commandname = commandname.__name__
        helptext  = mel.eval("help %s;" % commandname)
        if not helptext: raise RuntimeError, 'no command "%s" found' % commandname
        results = {}
        for line in helptext.split("\n")[4:-2]:
            tokens = line.split()
            if len(tokens) > 1:
                results[str(tokens[0][1:])] = str(tokens[1][1:])
        return cls(commandname, **results)


class LayoutInfo(CommandInfo):
    """
    Produces classes for layouts, including all the Layout specific attributes
    """
    DEFAULTS = constants.CONTROL_ATTRIBS + constants.LAYOUT_ATTRIBS
    INHERITS = 'Layout'
    

def generate_controls(filename, includeShortNames=False):
    """
    Write a text file with class definitions for all of the control classes in Maya.
    """
    with open (filename, 'wt') as filehandle:
        filehandle.write("'''\nmGui wrapper classes\n\nAuto-generated wrapper classes for use with mGui\n'''\n\n")
        filehandle.write('import maya.cmds as cmds\n')
        filehandle.write('from .core import Control\n')
        
        
        
        for each_class in constants.CONTROL_COMMANDS:
            try:
                filehandle.write(CommandInfo.from_command(each_class).template(includeShortNames))
                filehandle.write('\n\n')
            except RuntimeError:
                filehandle.write("# command '%s' not present in this version of maya" % each_class)

def generate_layouts(filename, includeShortNames=False):
    """
    Write a text file with class definitions for all of the layout classes in Maya.
    """
    with open (filename, 'wt') as filehandle:
        filehandle.write("'''\nmGui wrapper classes\n\nAuto-generated wrapper classes for use with mGui\n'''\n\n")
        filehandle.write('import maya.cmds as cmds\n')
        filehandle.write('from .core import Layout\n\n')
        for each_class in constants.LAYOUT_COMMANDS:
            try:
                filehandle.write(LayoutInfo.from_command(each_class).template(includeShortNames))
                filehandle.write('\n\n')
            except RuntimeError:
                filehandle.write("# command '%s' not present in this maya" % each_class)


                           
            