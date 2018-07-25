import mock
import sys
from types import ModuleType

# this creates and 'imports' a maya and a maya.cmds module
# as mocks

_maya = ModuleType('maya')
_cmds = ModuleType('cmds')
_maya.cmds = mock.MagicMock()
sys.modules['maya'] = _maya
sys.modules['maya.cmds'] = _cmds