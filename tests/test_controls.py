'''
Created on Mar 3, 2014

@author: Stephen Theodore
'''
from unittest import TestCase
import maya.cmds

LAST_ARGS = {}

def control_mock(*args, **kwargs):
    LAST_ARGS['args'] = args
    LAST_ARGS['kwargs']=  kwargs

maya.cmds.control = control_mock
maya.cmds.layout = control_mock
maya.cmds.window = control_mock

import mGui.core as core

class test_CtlProperty(TestCase):
    '''
    very dumb test that just makes sure the CtlProperty is calling the correct command, arg and kwarg
    '''

    class Example(object):
        CMD = core.cmds.control
        
        def __init__(self, *args, **kwargs):
            self.Widget = 'path|to|widget'
        
        fred = core.CtlProperty("fred", CMD)
        barney = core.CtlProperty("barney", CMD)
        
    def setUp(self):
        LAST_ARGS['args'] = (None,)
        LAST_ARGS['kwargs']= {}
        
    def test_call_uses_widget(self):
        t = self.Example()
        get = t.fred
        assert LAST_ARGS['args'][0] == 'path|to|widget'
        
    def test_call_uses_q_flag(self):
        t = self.Example()
        get = t.fred
        assert 'q' in LAST_ARGS['kwargs'] 
        
    def test_call_uses_q_control_flag(self):
        t = self.Example()
        get = t.fred
        assert 'fred' in LAST_ARGS['kwargs'] 
        
    def test_set_uses_widget(self):
        t = self.Example()
        t.fred = 999
        assert LAST_ARGS['args'][0] ==  'path|to|widget'

    def test_set_uses_e_flag(self):
        t = self.Example()
        t.fred = 999
        assert 'e' in LAST_ARGS['kwargs']
        
    def test_each_property_has_own_command(self):
        t = self.Example()
        get = t.fred
        assert 'fred' in LAST_ARGS['kwargs']
        get = t.barney
        assert 'barney' in LAST_ARGS['kwargs']
    
    def test_access_via_getattr(self):
        t = self.Example()
        get = getattr(t, 'fred')
        assert 'fred' in LAST_ARGS['kwargs']

    def test_access_via_dict_fails(self):
        t = self.Example()
        assert not 'fred' in t.__dict__
        
