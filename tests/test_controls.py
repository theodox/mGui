'''
Created on Mar 3, 2014

@author: Stephen Theodore
'''
from unittest import TestCase
import maya.cmds


def control_mock(*args, **kwargs):
    print kwargs
    return {'args':args, 'kwargs': kwargs}

maya.cmds.control = control_mock
maya.cmds.layout = control_mock

import mGui.core as core

class test_CtlProperty(TestCase):

    class Example(object):
        CMD = core.cmds.control
        
        def __init__(self, *args, **kwargs):
            self.Widget = 'path|to|widget'
        
        fred = core.CtlProperty("fred", CMD)
        
    def test_call_uses_widget(self):
        t = self.Example()
        assert t.fred['args'][0] == 'path|to|widget'
        
    def test_call_uses_q_flag(self):
        t = self.Example()
        assert 'q' in t.fred['kwargs'] 
        
    def test_call_uses_q_control_flag(self):
        t = self.Example()
        assert 'fred' in t.fred['kwargs'] 
        

