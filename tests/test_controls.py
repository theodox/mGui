'''
Created on Mar 3, 2014

@author: Stephen Theodore
'''
import mock_maya
from unittest import TestCase, main

# LAST_ARGS = {}


# def control_mock(*args, **kwargs):
#     LAST_ARGS['args'] = args
#     LAST_ARGS['kwargs'] = kwargs


# import maya.standalone

# maya.standalone.initialize()

# import maya.cmds as cmds

# cmds.control = control_mock
# # ===============================================================================
# # cmds.layout = control_mock
# # cmds.window = control_mock
# # cmds.menu = control_mock
# # cmds.menuItem = control_mock
# # 
# # import mGui.styles as styles
# # class MockStyled(object):
# #    CMD = cmds.control
# # 
# # styles.Styled = MockStyled
# # ===============================================================================


CONTROL_CMDS = ['attrColorSliderGrp',
                'attrControlGrp',
                'attrFieldGrp',
                'attrFieldSliderGrp',
                'attrNavigationControlGrp',
                'button',
                'canvas',
                'channelBox',
                'checkBox',
                'checkBoxGrp',
                'cmdScrollFieldExecuter',
                'cmdScrollFieldReporter',
                'cmdShell',
                'colorIndexSliderGrp',
                'colorSliderButtonGrp',
                'colorSliderGrp',
                'commandLine',
                'componentBox',
                'control',
                'floatField',
                'floatFieldGrp',
                'floatScrollBar',
                'floatSlider',
                'floatSlider2',
                'floatSliderButtonGrp',
                'floatSliderGrp',
                'gradientControl',
                'gradientControlNoAttr',
                'helpLine',
                'hudButton',
                'hudSlider',
                'hudSliderButton',
                'iconTextButton',
                'iconTextCheckBox',
                'iconTextRadioButton',
                'iconTextRadioCollection',
                'iconTextScrollList',
                'iconTextStaticLabel',
                'image',
                'intField',
                'intFieldGrp',
                'intScrollBar',
                'intSlider',
                'intSliderGrp',
                'layerButton',
                'messageLine',
                'nameField',
                'nodeTreeLister',
                'palettePort',
                'picture',
                'progressBar',
                'radioButton',
                'radioButtonGrp',
                'radioCollection',
                'rangeControl',
                'scriptTable',
                'scrollField',
                'separator',
                'shelfButton',
                'soundControl',
                'swatchDisplayPort',
                'switchTable',
                'symbolButton',
                'symbolCheckBox',
                'text',
                'textField',
                'textFieldButtonGrp',
                'textFieldGrp',
                'textScrollList',
                'timeControl',
                'timePort',
                'toolButton',
                'toolCollection',
                'treeLister',
                'treeView']

LAYOUT_CMDS = [
    'columnLayout',
    'dockControl',
    'flowLayout',
    'formLayout',
    'frameLayout',
    'gridLayout',
    'layout',
    'menuBarLayout',
    'paneLayout',
    'rowColumnLayout',
    'rowLayout',
    'scrollLayout',
    'shelfLayout',
    'shelfTabLayout',
    'tabLayout',
    'toolBar']

import inspect
import mGui.properties as properties
import mGui.gui as gui
import mGui.core.progress as progress
import maya.cmds as cmds

class test_CtlProperty(TestCase):
    '''
    very dumb test that just makes sure the CtlProperty is calling the correct command, arg and kwarg
    '''

    class Example(object):
        CMD = cmds.control

        def __init__(self, *args, **kwargs):
            self.widget = 'path|to|widget'

        fred = properties.CtlProperty("fred", CMD)
        barney = properties.CtlProperty("barney", CMD)


    def test_call_uses_widget(self):
        t = self.Example()
        get = t.fred
        assert cmds.control.called_with(t.widget)

    def test_call_uses_q_flag(self):
        t = self.Example()
        get = t.fred
        assert cmds.control.called_with(q=True)

    def test_call_uses_q_control_flag(self):
        t = self.Example()
        get = t.fred
        assert cmds.control.called_with(fred=True)

    def test_set_uses_widget(self):
        t = self.Example()
        t.fred = 999
        assert cmds.control.called_with(t.widget)


    def test_set_uses_e_flag(self):
        t = self.Example()
        t.fred = 999
        assert cmds.control.called_with(e=True)

    def test_each_property_has_own_command(self):
        t = self.Example()
        get = t.fred
        assert cmds.control.called_with(fred=True)

        get = t.barney
        assert cmds.control.called_with(barney=True)

    def test_access_via_getattr(self):
        t = self.Example()
        get = getattr(t, 'fred')
        assert cmds.control.called_with(q=True)


    def test_access_via_dict_fails(self):
        t = self.Example()
        assert not 'fred' in t.__dict__


class TestControlsExist(TestCase):
    def test_has_all_controls(self):
        gui_items = [i[0] for i in inspect.getmembers(gui)]
        gui_items += [i[0] for i in inspect.getmembers(progress)]

        for item in CONTROL_CMDS:
            capped = item[0].upper() + item[1:]
            assert capped in gui_items, ("control %s is not defined in mGui.gui" % capped)

    def test_has_all_layouts(self):
        gui_items = [i[0] for i in inspect.getmembers(gui)]

        for item in LAYOUT_CMDS:
            capped = item[0].upper() + item[1:]
            assert capped in gui_items, ("control %s is not defined in mGui.gui" % capped)

    def test_has_window(self):
        gui_items = [i[0] for i in inspect.getmembers(gui)]
        assert 'Window' in gui_items

    def test_has_Menu(self):
        gui_items = [i[0] for i in inspect.getmembers(gui)]
        assert 'Menu' in gui_items

    def test_has_MenuItem(self):
        gui_items = [i[0] for i in inspect.getmembers(gui)]
        assert 'MenuItem' in gui_items



if __name__ == '__main__':
    main()