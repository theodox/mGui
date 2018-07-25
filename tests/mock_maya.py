import mock
import sys
from types import ModuleType

# this creates and 'imports' a maya and a maya.cmds module
# as mocks

_maya = ModuleType('maya')
_cmds = ModuleType('cmds')
_utils = ModuleType('utils')
_maya.cmds = mock.MagicMock()
_maya.utils = mock.MagicMock()
sys.modules['maya'] = _maya
sys.modules['maya.cmds'] = _cmds
sys.modules['maya.utils'] = _utils
