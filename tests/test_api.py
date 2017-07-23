from unittest import TestCase, main
import maya.standalone

try:
    maya.standalone.initialize()
except:
    pass

from mGui.gui import *
from mGui.forms import *
from mGui.lists import *

"""These tests just ensure that the mGui.gui api is the same from version to version"""


class TestMGuiAPI(TestCase):

    def test_ActiveOptionMenu(self):
        assert ActiveOptionMenu

    def test_AttrColorSliderGrp(self):
        assert AttrColorSliderGrp

    def test_AttrControlGrp(self):
        assert AttrControlGrp

    def test_AttrFieldGrp(self):
        assert AttrFieldGrp

    def test_AttrFieldSliderGrp(self):
        assert AttrFieldSliderGrp

    def test_AttrNavigationControlGrp(self):
        assert AttrNavigationControlGrp

    def test_BindingWindow(self):
        assert BindingWindow

    def test_Button(self):
        assert Button

    def test_Canvas(self):
        assert Canvas

    def test_ChannelBox(self):
        assert ChannelBox

    def test_CheckBox(self):
        assert CheckBox

    def test_CheckBoxGrp(self):
        assert CheckBoxGrp

    def test_CheckBoxMenuItem(self):
        assert CheckBoxMenuItem

    def test_CmdScrollFieldExecuter(self):
        assert CmdScrollFieldExecuter

    def test_CmdScrollFieldReporter(self):
        assert CmdScrollFieldReporter

    def test_CmdShell(self):
        assert CmdShell

    def test_ColorIndexSliderGrp(self):
        assert ColorIndexSliderGrp

    def test_ColorSliderButtonGrp(self):
        assert ColorSliderButtonGrp

    def test_ColorSliderGrp(self):
        assert ColorSliderGrp

    def test_ColumnLayout(self):
        assert ColumnLayout

    def test_CommandLine(self):
        assert CommandLine

    def test_ComponentBox(self):
        assert ComponentBox

    def test_ComponentEditor(self):
        assert ComponentEditor

    def test_Control(self):
        assert Control

    def test_DockControl(self):
        assert DockControl

    def test_Event(self):
        assert Event

    def test_FloatField(self):
        assert FloatField

    def test_FloatFieldGrp(self):
        assert FloatFieldGrp

    def test_FloatScrollBar(self):
        assert FloatScrollBar

    def test_FloatSlider(self):
        assert FloatSlider

    def test_FloatSlider2(self):
        assert FloatSlider2

    def test_FloatSliderButtonGrp(self):
        assert FloatSliderButtonGrp

    def test_FloatSliderGrp(self):
        assert FloatSliderGrp

    def test_FlowLayout(self):
        assert FlowLayout

    def test_FormLayout(self):
        assert FormLayout

    def test_FrameLayout(self):
        assert FrameLayout

    def test_GradientControl(self):
        assert GradientControl

    def test_GradientControlNoAttr(self):
        assert GradientControlNoAttr

    def test_GridLayout(self):
        assert GridLayout

    def test_HardwareRenderPanel(self):
        assert HardwareRenderPanel

    def test_HelpLine(self):
        assert HelpLine

    def test_HudButton(self):
        assert HudButton

    def test_HudSlider(self):
        assert HudSlider

    def test_HudSliderButton(self):
        assert HudSliderButton

    def test_HyperGraph(self):
        assert HyperGraph

    def test_HyperPanel(self):
        assert HyperPanel

    def test_HyperShade(self):
        assert HyperShade

    def test_IconTextButton(self):
        assert IconTextButton

    def test_IconTextCheckBox(self):
        assert IconTextCheckBox

    def test_IconTextRadioButton(self):
        assert IconTextRadioButton

    def test_IconTextRadioCollection(self):
        assert IconTextRadioCollection

    def test_IconTextScrollList(self):
        assert IconTextScrollList

    def test_IconTextStaticLabel(self):
        assert IconTextStaticLabel

    def test_Image(self):
        assert Image

    def test_IntField(self):
        assert IntField

    def test_IntFieldGrp(self):
        assert IntFieldGrp

    def test_IntScrollBar(self):
        assert IntScrollBar

    def test_IntSlider(self):
        assert IntSlider

    def test_IntSliderGrp(self):
        assert IntSliderGrp

    def test_Labeled(self):
        assert Labeled

    def test_LayerButton(self):
        assert LayerButton

    def test_Layout(self):
        assert Layout

    def test_MAYA_VERSION(self):
        assert MAYA_VERSION

    def test_MTreeView(self):
        assert MTreeView

    def test_Menu(self):
        assert Menu

    def test_MenuBarLayout(self):
        assert MenuBarLayout

    def test_MenuDivider(self):
        assert MenuDivider

    def test_MenuItem(self):
        assert MenuItem

    def test_MessageLine(self):
        assert MessageLine

    def test_ModelEditor(self):
        assert ModelEditor

    def test_ModelPanel(self):
        assert ModelPanel

    def test_NameField(self):
        assert NameField

    def test_Nested(self):
        assert Nested

    def test_NodeOutliner(self):
        assert NodeOutliner

    def test_NodeTreeLister(self):
        assert NodeTreeLister

    def test_OptionMenu(self):
        assert OptionMenu

    def test_OutlinerEditor(self):
        assert OutlinerEditor

    def test_OutlinerPanel(self):
        assert OutlinerPanel

    def test_PalettePort(self):
        assert PalettePort

    def test_PaneLayout(self):
        assert PaneLayout

    def test_Panel(self):
        assert Panel

    def test_PanelConfiguration(self):
        assert PanelConfiguration

    def test_PanelFactory(self):
        assert PanelFactory

    def test_PanelHistory(self):
        assert PanelHistory

    def test_Picture(self):
        assert Picture

    def test_PopupMenu(self):
        assert PopupMenu

    def test_ProgressBar(self):
        assert ProgressBar

    def test_REGISTRY(self):
        assert REGISTRY

    def test_RadioButton(self):
        assert RadioButton

    def test_RadioButtonGrp(self):
        assert RadioButtonGrp

    def test_RadioCollection(self):
        assert RadioCollection

    def test_RadioMenuItem(self):
        assert RadioMenuItem

    def test_RadioMenuItemCollection(self):
        assert RadioMenuItemCollection

    def test_RangeControl(self):
        assert RangeControl

    def test_RowColumnLayout(self):
        assert RowColumnLayout

    def test_RowLayout(self):
        assert RowLayout

    def test_ScriptTable(self):
        assert ScriptTable

    def test_ScriptedPanel(self):
        assert ScriptedPanel

    def test_ScrollField(self):
        assert ScrollField

    def test_ScrollLayout(self):
        assert ScrollLayout

    def test_Separator(self):
        assert Separator

    def test_ShelfButton(self):
        assert ShelfButton

    def test_ShelfLayout(self):
        assert ShelfLayout

    def test_ShelfTabLayout(self):
        assert ShelfTabLayout

    def test_SoundControl(self):
        assert SoundControl

    def test_SpreadSheetEditor(self):
        assert SpreadSheetEditor

    def test_SubMenu(self):
        assert SubMenu

    def test_SwatchDisplayPort(self):
        assert SwatchDisplayPort

    def test_SwitchTable(self):
        assert SwitchTable

    def test_SymbolButton(self):
        assert SymbolButton

    def test_SymbolCheckBox(self):
        assert SymbolCheckBox

    def test_TabLayout(self):
        assert TabLayout

    def test_Text(self):
        assert Text

    def test_TextField(self):
        assert TextField

    def test_TextFieldButtonGrp(self):
        assert TextFieldButtonGrp

    def test_TextFieldGrp(self):
        assert TextFieldGrp

    def test_TextScrollList(self):
        assert TextScrollList

    def test_TimeControl(self):
        assert TimeControl

    def test_TimePort(self):
        assert TimePort

    def test_ToolBar(self):
        assert ToolBar

    def test_ToolButton(self):
        assert ToolButton

    def test_ToolCollection(self):
        assert ToolCollection

    def test_TreeLister(self):
        assert TreeLister

    def test_TreeView(self):
        assert TreeView

    def test_Visor(self):
        assert Visor

    def test_Window(self):
        assert Window


class TestFormsAPI(TestCase):
    def test_FillForm(self):
        assert FillForm

    def test_FooterForm(self):
        assert FooterForm

    def test_FormLayout(self):
        assert FormLayout

    def test_HeaderForm(self):
        assert HeaderForm

    def test_HorizontalExpandForm(self):
        assert HorizontalExpandForm

    def test_HorizontalForm(self):
        assert HorizontalForm

    def test_HorizontalStretchForm(self):
        assert HorizontalStretchForm

    def test_HorizontalThreePane(self):
        assert HorizontalThreePane

    def test_LayoutDialogForm(self):
        assert LayoutDialogForm

    def test_NavForm(self):
        assert NavForm

    def test_VerticalExpandForm(self):
        assert VerticalExpandForm

    def test_VerticalForm(self):
        assert VerticalForm

    def test_VerticalStretchForm(self):
        assert VerticalStretchForm

    def test_VerticalThreePane(self):
        assert VerticalThreePane


def TestListsAPI(TestCase):
    def test_BoundIconTextScrollList(self):
        assert BoundIconTextScrollList

    def test_BoundScrollList(self):
        assert BoundScrollList

    def test_ColumnList(self):
        assert ColumnList

    def test_FormList(self):
        assert FormList

    def test_HorizontalList(self):
        assert HorizontalList

    def test_ItemTemplate(self):
        assert ItemTemplate

    def test_ScrollListBase(self):
        assert ScrollListBase

    def test_Templated(self):
        assert Templated

    def test_VerticalList(self):
        assert VerticalList

    def test_WrapList(self):
        assert WrapList


class TestControlAPI(TestCase):
    def test_wrap(self):
        assert callable(Control.wrap)

    def test_Nested_exists(self):
        assert 'exists' in Control._ATTRIBS

    def test_Control_onDeleted(self):
        assert hasattr(Control, 'parent')

    def test_Control_onDeleted(self):
        assert hasattr(Control, 'delete')

    def test_Control_onDeleted(self):
        assert hasattr(Control, 'forget')


class TestNestedAPI(TestCase):
    def test_Nested_ProxyFactory(self):
        assert Nested.ProxyFactory

    def test_Nested_add(self):
        assert Nested.add

    def test_Nested_add_current(self):
        assert Nested.add_current

    def test_Nested_as_parent(self):
        assert Nested.as_parent

    def test_Nested_clear(self):
        assert Nested.clear

    def test_Nested_current(self):
        assert Nested.current

    def test_Nested_delete(self):
        assert Nested.delete

    def test_Nested_find(self):
        assert Nested.find

    def test_Nested_forget(self):
        assert Nested.forget

    def test_Nested_layout(self):
        assert callable(Nested.layout)

    def test_Nested_recurse(self):
        assert callable(Nested.recurse)

    def test_Nested_register_callback(self):
        assert Nested.register_callback

    def test_Nested_remove(self):
        assert Nested.remove

    def test_Nested_replace(self):
        assert Nested.replace

    def test_Nested_stylesheet(self):
        assert Nested.stylesheet


class TestWindowAPI(TestCase):
    def test_show(self):
        assert callable(Window.show)

    def hide(self):
        assert callable(Windows.hide)
