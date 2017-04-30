"""
mGui wrapper classes

Originally auto generated using helpers.tools
"""

import maya.cmds as cmds
from mGui.events import Event
from mGui.core import Control, Nested
from mGui.bindings import BindingContext as _BindingContext
import weakref
from itertools import count as _count


class Labeled(Control):
    """
    This is an abstract class which is inherited by all XXXGrp controls to allow
    easier styling. By setting a style with the Labeled class as a target you
    can make sure all the label and control widths line up neatly.  It's OK
    to use the column____2  and column____3 attributes in the same style since 
    Maya will ignore the unwanted ones in a Grp control that has the wrong number
    of columns.  For example:
    
    
    label_style_256 = mGui.styles.CSS (Labeled, 
                                        columnWidth2 = (64, 192), 
                                        columnWidth3 = (64, 128, 64),
                                        columnAttach2= ("right", "both"), 
                                        columnAttach3 =("right", "both", "both"),
                                        columnOffset2= (4, 0), 
                                        columnOffset3= (4, 0, 0), 
                                        margin = (4,4))
    would create a 64 pixel label for both 2-unit and 3-unit label controls like
    AttrFieldGrp
    """
    pass


class AttrColorSliderGrp(Labeled):
    """Wrapper class for cmds.attrColorSliderGrp"""
    CMD = getattr(cmds, 'attrColorSliderGrp', NotImplemented)
    _ATTRIBS = ['attribute', 'rowAttach', 'columnAttach', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4',
                'columnAlign3', 'columnAlign2', 'label', 'adjustableColumn', 'columnAlign', 'columnAttach6',
                'adjustableColumn5', 'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4', 'showButton',
                'hsvValue', 'columnWidth', 'adjustableColumn6', 'columnOffset2', 'columnOffset3', 'columnOffset4',
                'columnOffset5', 'columnOffset6', 'rgbValue', 'attrNavDecision', 'columnAttach4', 'columnAttach5',
                'columnAttach2', 'columnAttach3']
    _CALLBACKS = []


class AttrControlGrp(Labeled):
    """Wrapper class for cmds.attrControlGrp"""
    CMD = getattr(cmds, 'attrControlGrp', NotImplemented)
    _ATTRIBS = ['attribute', 'handlesAttribute', 'label', 'hideMapButton']
    _CALLBACKS = ['changeCommand']
    _BIND_TRIGGER = 'changeCommand'


class AttrFieldGrp(Labeled):
    """Wrapper class for cmds.attrFieldGrp"""
    CMD = getattr(cmds, 'attrFieldGrp', NotImplemented)
    _ATTRIBS = ['attribute', 'rowAttach', 'columnAttach', 'extraLabel', 'minValue', 'columnWidth2', 'columnWidth3',
                'columnWidth1', 'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5',
                'columnAlign4', 'columnAlign3', 'columnAlign2', 'label', 'numberOfFields', 'adjustableColumn',
                'columnAlign', 'maxValue', 'precision', 'step', 'hideMapButton', 'adjustableColumn2',
                'adjustableColumn3', 'adjustableColumn4', 'adjustableColumn5', 'adjustableColumn6', 'columnWidth',
                'columnOffset2', 'columnOffset3', 'columnOffset4', 'columnOffset5', 'columnOffset6', 'columnAttach6',
                'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand']
    _BIND_TRIGGER = 'changeCommand'


class AttrFieldSliderGrp(Labeled):
    """Wrapper class for cmds.attrFieldSliderGrp"""
    CMD = getattr(cmds, 'attrFieldSliderGrp', NotImplemented)
    _ATTRIBS = ['attribute', 'rowAttach', 'sliderMaxValue', 'columnAttach', 'minValue', 'columnWidth2', 'columnWidth3',
                'columnWidth1', 'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5',
                'columnAlign4', 'columnAlign3', 'columnAlign2', 'label', 'columnOffset3', 'adjustableColumn',
                'columnAlign', 'vertical', 'sliderMinValue', 'fieldMaxValue', 'maxValue', 'precision', 'step',
                'hideMapButton', 'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4', 'adjustableColumn5',
                'fieldMinValue', 'columnWidth', 'sliderStep', 'adjustableColumn6', 'columnOffset2', 'fieldStep',
                'columnOffset4', 'columnOffset5', 'columnOffset6', 'columnAttach6', 'columnAttach4', 'columnAttach5',
                'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand']
    _BIND_TRIGGER = 'changeCommand'


class AttrNavigationControlGrp(Labeled):
    """Wrapper class for cmds.attrNavigationControlGrp"""
    CMD = getattr(cmds, 'attrNavigationControlGrp', NotImplemented)
    _ATTRIBS = ['connectAttrToDropped', 'attribute', 'rowAttach', 'columnAttach', 'createNew', 'adjustableColumn3',
                'columnWidth2', 'columnWidth3', 'columnWidth1', 'columnWidth6', 'columnWidth4', 'columnWidth5',
                'columnAlign6', 'columnAlign5', 'columnAlign4', 'columnAlign3', 'columnAlign2', 'label',
                'columnOffset4', 'adjustableColumn', 'columnAlign', 'unignore', 'connectToExisting', 'disconnect',
                'ignoreNotSupported', 'adjustableColumn2', 'defaultTraversal', 'adjustableColumn4', 'adjustableColumn5',
                'adjustableColumn6', 'columnWidth', 'columnAttach3', 'ignore', 'columnOffset2', 'columnOffset3',
                'relatedNodes', 'columnOffset5', 'columnOffset6', 'columnAttach6', 'attrNavDecision', 'columnAttach4',
                'columnAttach5', 'columnAttach2', 'connectNodeToDropped', 'delete']
    _CALLBACKS = []


class Button(Control):
    """Wrapper class for cmds.button"""
    CMD = getattr(cmds, 'button', NotImplemented)
    _ATTRIBS = ['actionIsSubstitute', 'actOnPress', 'align', 'label', 'recomputeSize']
    _CALLBACKS = ['command']


class Canvas(Control):
    """Wrapper class for cmds.canvas"""
    CMD = getattr(cmds, 'canvas', NotImplemented)
    _ATTRIBS = ['rgbValue', 'hsvValue']
    _CALLBACKS = ['pressCommand']


class ChannelBox(Control):
    """Wrapper class for cmds.channelBox"""
    CMD = getattr(cmds, 'channelBox', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class CheckBox(Control):
    """Wrapper class for cmds.checkBox"""
    CMD = getattr(cmds, 'checkBox', NotImplemented)
    _ATTRIBS = ['recomputeSize', 'align', 'editable', 'value', 'label']
    _CALLBACKS = ['changeCommand', 'offCommand', 'onCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class CheckBoxGrp(Labeled):
    """Wrapper class for cmds.checkBoxGrp"""
    CMD = getattr(cmds, 'checkBoxGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'labelArray3', 'adjustableColumn3', 'columnWidth2', 'columnWidth3',
                'columnWidth1', 'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5',
                'columnAlign4', 'columnAlign3', 'columnAlign2', 'label', 'numberOfCheckBoxes', 'value4', 'value3',
                'value2', 'value1', 'editable', 'enable1', 'enable2', 'enable3', 'enable4', 'columnAlign', 'vertical',
                'label1', 'label2', 'label3', 'label4', 'valueArray3', 'valueArray2', 'labelArray4', 'labelArray2',
                'valueArray4', 'adjustableColumn2', 'adjustableColumn', 'adjustableColumn4', 'adjustableColumn5',
                'adjustableColumn6', 'columnWidth', 'columnOffset2', 'columnOffset3', 'columnOffset4', 'columnOffset5',
                'columnOffset6', 'columnAttach6', 'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'changeCommand1', 'changeCommand2', 'changeCommand3', 'changeCommand4', 'offCommand',
                  'offCommand1', 'offCommand2', 'offCommand3', 'offCommand4', 'onCommand', 'onCommand1', 'onCommand2',
                  'onCommand3', 'onCommand4']
    _BIND_TRIGGER = 'changeCommand'


class CmdScrollFieldExecuter(Control):
    """Wrapper class for cmds.cmdScrollFieldExecuter"""
    CMD = getattr(cmds, 'cmdScrollFieldExecuter', NotImplemented)
    _ATTRIBS = ['insertText', 'load', 'searchAndSelect', 'text', 'saveSelection', 'spacesPerTab', 'filterKeyPress',
                'redo', 'select', 'indentSelection', 'searchWraps', 'currentLine', 'removeStoredContents',
                'copySelection', 'hasFocus', 'showTooltipHelp', 'objectPathCompletion', 'storeContents', 'hasSelection',
                'appendText', 'unindentSelection', 'saveSelectionToShelf', 'sourceType', 'cutSelection', 'selectAll',
                'numberOfLines', 'replaceAll', 'executeAll', 'undo', 'showLineNumbers', 'commandCompletion', 'execute',
                'searchString', 'loadContents', 'textLength', 'clear', 'selectedText', 'searchDown', 'searchMatchCase',
                'source', 'pasteSelection', 'tabsForIndent']
    _CALLBACKS = ['receiveFocusCommand']


class CmdScrollFieldReporter(Control):
    """Wrapper class for cmds.cmdScrollFieldReporter"""
    CMD = getattr(cmds, 'cmdScrollFieldReporter', NotImplemented)
    _ATTRIBS = ['selectAll', 'stackTrace', 'saveSelectionToShelf', 'suppressWarnings', 'cutSelection', 'suppressInfo',
                'hasFocus', 'text', 'clear', 'textLength', 'copySelection', 'lineNumbers', 'suppressStackTrace',
                'saveSelection', 'suppressResults', 'suppressErrors', 'pasteSelection', 'filterSourceType', 'select']
    _CALLBACKS = ['echoAllCommands', 'receiveFocusCommand']


class CmdShell(Control):
    """Wrapper class for cmds.cmdShell"""
    CMD = getattr(cmds, 'cmdShell', NotImplemented)
    _ATTRIBS = ['numberOfHistoryLines', 'clear', 'command', 'numberOfSavedLines', 'prompt']
    _CALLBACKS = []


class ColorIndexSliderGrp(Labeled):
    """Wrapper class for cmds.colorIndexSliderGrp"""
    CMD = getattr(cmds, 'colorIndexSliderGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'extraLabel', 'minValue', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4',
                'columnAlign3', 'columnAlign2', 'label', 'adjustableColumn', 'columnAlign', 'maxValue',
                'forceDragRefresh', 'invisible', 'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4',
                'adjustableColumn5', 'adjustableColumn6', 'columnWidth', 'value', 'columnOffset2', 'columnOffset3',
                'columnOffset4', 'columnOffset5', 'columnOffset6', 'columnAttach6', 'columnAttach4', 'columnAttach5',
                'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class ColorSliderButtonGrp(Labeled):
    """Wrapper class for cmds.colorSliderButtonGrp"""
    CMD = getattr(cmds, 'colorSliderButtonGrp', NotImplemented)
    _ATTRIBS = ['image', 'columnAttach', 'columnWidth2', 'columnWidth3', 'columnWidth1', 'columnWidth6', 'buttonLabel',
                'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4', 'columnAlign3',
                'columnAlign2', 'label', 'adjustableColumn', 'rowAttach', 'columnAlign', 'forceDragRefresh',
                'columnAttach6', 'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4', 'adjustableColumn5',
                'hsvValue', 'columnWidth', 'adjustableColumn6', 'columnOffset2', 'columnOffset3', 'columnOffset4',
                'columnOffset5', 'columnOffset6', 'rgbValue', 'symbolButtonDisplay', 'columnAttach4', 'columnAttach5',
                'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['buttonCommand', 'changeCommand', 'dragCommand', 'symbolButtonCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'rgbValue'
    _BIND_TGT = 'rgbValue'


class ColorSliderGrp(Labeled):
    """Wrapper class for cmds.colorSliderGrp"""
    CMD = getattr(cmds, 'colorSliderGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'columnWidth2', 'columnWidth3', 'columnWidth1', 'columnWidth6',
                'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4', 'columnAlign3',
                'columnAlign2', 'label', 'adjustableColumn', 'columnAlign', 'forceDragRefresh', 'columnAttach6',
                'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4', 'adjustableColumn5', 'hsvValue',
                'columnWidth', 'adjustableColumn6', 'columnOffset2', 'columnOffset3', 'columnOffset4', 'columnOffset5',
                'columnOffset6', 'rgbValue', 'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'rgbValue'
    _BIND_TGT = 'rgbValue'


class CommandLine(Control):
    """Wrapper class for cmds.commandLine"""
    CMD = getattr(cmds, 'commandLine', NotImplemented)
    _ATTRIBS = ['holdFocus', 'outputAnnotation', 'inputAnnotation', 'sourceType', 'numberOfHistoryLines', 'command']
    _CALLBACKS = ['enterCommand']


class ComponentBox(Control):
    """Wrapper class for cmds.componentBox"""
    CMD = getattr(cmds, 'componentBox', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class FloatField(Control):
    """Wrapper class for cmds.floatField"""
    CMD = getattr(cmds, 'floatField', NotImplemented)
    _ATTRIBS = ['editable', 'precision', 'value', 'maxValue', 'step', 'minValue']
    _CALLBACKS = ['changeCommand', 'dragCommand', 'enterCommand', 'receiveFocusCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class FloatFieldGrp(Labeled):
    """Wrapper class for cmds.floatFieldGrp"""
    CMD = getattr(cmds, 'floatFieldGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'extraLabel', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4',
                'columnAlign3', 'columnAlign2', 'label', 'value4', 'value3', 'numberOfFields', 'value1', 'enable1',
                'enable2', 'adjustableColumn', 'enable4', 'value2', 'columnAlign', 'precision', 'adjustableColumn3',
                'adjustableColumn2', 'enable3', 'adjustableColumn4', 'adjustableColumn5', 'adjustableColumn6',
                'columnWidth', 'value', 'columnOffset2', 'columnOffset3', 'columnOffset4', 'columnOffset5',
                'columnOffset6', 'columnAttach6', 'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class FloatScrollBar(Control):
    """Wrapper class for cmds.floatScrollBar"""
    CMD = getattr(cmds, 'floatScrollBar', NotImplemented)
    _ATTRIBS = ['largeStep', 'maxValue', 'value', 'minValue', 'step', 'horizontal']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class FloatSlider(Control):
    """Wrapper class for cmds.floatSlider"""
    CMD = getattr(cmds, 'floatSlider', NotImplemented)
    _ATTRIBS = ['horizontal', 'step', 'maxValue', 'value', 'minValue']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class FloatSlider2(Control):
    """Wrapper class for cmds.floatSlider2"""
    CMD = getattr(cmds, 'floatSlider2', NotImplemented)
    _ATTRIBS = ['horizontal', 'step', 'maxValue', 'value', 'minValue']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class FloatSliderButtonGrp(Labeled):
    """Wrapper class for cmds.floatSliderButtonGrp"""
    CMD = getattr(cmds, 'floatSliderButtonGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'extraLabel', 'minValue', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'buttonLabel', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5',
                'columnAlign4', 'columnAlign3', 'columnAlign2', 'label', 'field', 'columnOffset3', 'adjustableColumn',
                'image', 'columnAlign', 'fieldMaxValue', 'maxValue', 'precision', 'step', 'adjustableColumn2',
                'adjustableColumn3', 'adjustableColumn4', 'adjustableColumn5', 'fieldMinValue', 'columnWidth', 'value',
                'sliderStep', 'adjustableColumn6', 'columnOffset2', 'fieldStep', 'columnOffset4', 'columnOffset5',
                'columnOffset6', 'columnAttach6', 'symbolButtonDisplay', 'columnAttach4', 'columnAttach5',
                'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['buttonCommand', 'changeCommand', 'dragCommand', 'symbolButtonCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class FloatSliderGrp(Labeled):
    """Wrapper class for cmds.floatSliderGrp"""
    CMD = getattr(cmds, 'floatSliderGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'extraLabel', 'minValue', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4',
                'columnAlign3', 'columnAlign2', 'label', 'field', 'columnOffset3', 'adjustableColumn', 'columnAlign',
                'fieldMaxValue', 'maxValue', 'precision', 'step', 'adjustableColumn2', 'adjustableColumn3',
                'adjustableColumn4', 'adjustableColumn5', 'fieldMinValue', 'columnWidth', 'value', 'sliderStep',
                'adjustableColumn6', 'columnOffset2', 'fieldStep', 'columnOffset4', 'columnOffset5', 'columnOffset6',
                'columnAttach6', 'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class GradientControl(Control):
    """Wrapper class for cmds.gradientControl"""
    CMD = getattr(cmds, 'gradientControl', NotImplemented)
    _ATTRIBS = ['upperLimitControl', 'adaptiveScaling', 'refreshOnRelease', 'selectedPositionControl', 'attribute',
                'numberOfControls', 'staticPositions', 'staticNumberOfControls', 'verticalLayout',
                'selectedInterpControl', 'selectedColorControl']
    _CALLBACKS = []


class GradientControlNoAttr(Control):
    """Wrapper class for cmds.gradientControlNoAttr"""
    CMD = getattr(cmds, 'gradientControlNoAttr', NotImplemented)
    _ATTRIBS = ['currentKeyColorValue', 'currentKeyChanged', 'rampAsColor', 'optionVar', 'currentKeyCurveValue',
                'valueAtPoint', 'asString', 'currentKeyInterpValue', 'currentKey']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'


class HelpLine(Control):
    """Wrapper class for cmds.helpLine"""
    CMD = getattr(cmds, 'helpLine', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class HudButton(Control):
    """Wrapper class for cmds.hudButton"""
    CMD = getattr(cmds, 'hudButton', NotImplemented)
    _ATTRIBS = ['allowOverlap', 'blockAlignment', 'buttonWidth', 'buttonShape', 'blockSize', 'section', 'label',
                'padding', 'labelFontSize', 'block']
    _CALLBACKS = ['pressCommand', 'releaseCommand']


class HudSlider(Control):
    """Wrapper class for cmds.hudSlider"""
    CMD = getattr(cmds, 'hudSlider', NotImplemented)
    _ATTRIBS = ['valueAlignment', 'internalPadding', 'decimalPrecision', 'labelWidth', 'labelFontSize', 'blockSize',
                'valueFontSize', 'sliderLength', 'maxValue', 'value', 'minValue', 'padding', 'valueWidth', 'block',
                'sliderIncrement', 'allowOverlap', 'label', 'type', 'section', 'blockAlignment']
    _CALLBACKS = ['dragCommand', 'pressCommand', 'releaseCommand']
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'
    _BIND_TRIGGER = 'releaseCommand'


class HudSliderButton(Control):
    """Wrapper class for cmds.hudSliderButton"""
    CMD = getattr(cmds, 'hudSliderButton', NotImplemented)
    _ATTRIBS = ['valueAlignment', 'internalPadding', 'decimalPrecision', 'buttonLabelFontSize', 'valueFontSize',
                'sliderLength', 'minValue', 'blockAlignment', 'buttonLabel', 'sliderLabelFontSize', 'sliderLabel',
                'buttonShape', 'blockSize', 'section', 'type', 'allowOverlap', 'maxValue', 'padding', 'sliderIncrement',
                'sliderLabelWidth', 'value', 'valueWidth', 'buttonWidth', 'block']
    _CALLBACKS = ['buttonPressCommand', 'buttonReleaseCommand', 'sliderDragCommand', 'sliderPressCommand',
                  'sliderReleaseCommand']
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'
    _BIND_TRIGGER = 'sliderReleaseCommand'


class IconTextButton(Control):
    """Wrapper class for cmds.iconTextButton"""
    CMD = getattr(cmds, 'iconTextButton', NotImplemented)
    _ATTRIBS = ['imageOverlayLabel', 'actionIsSubstitute', 'font', 'marginHeight', 'style', 'sourceType',
                'overlayLabelColor', 'align', 'image', 'label', 'selectionImage', 'image3', 'highlightImage',
                'marginWidth', 'labelOffset', 'image2', 'disabledImage', 'commandRepeatable', 'image1',
                'overlayLabelBackColor']
    _CALLBACKS = ['command', 'doubleClickCommand', 'handleNodeDropCallback', 'labelEditingCallback']


class IconTextCheckBox(Control):
    """Wrapper class for cmds.iconTextCheckBox"""
    CMD = getattr(cmds, 'iconTextCheckBox', NotImplemented)
    _ATTRIBS = ['imageOverlayLabel', 'marginHeight', 'style', 'overlayLabelColor', 'overlayLabelBackColor',
                'highlightImage', 'image1', 'selectionHighlightImage', 'label', 'value', 'selectionImage', 'align',
                'image3', 'marginWidth', 'labelOffset', 'image2', 'disabledImage', 'font', 'image']
    _CALLBACKS = ['changeCommand', 'offCommand', 'onCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class IconTextScrollList(Control):
    """Wrapper class for cmds.iconTextScrollList"""
    CMD = getattr(cmds, 'iconTextScrollList', NotImplemented)
    _ATTRIBS = ['deselectAll', 'allowMultiSelection', 'dragFeedbackVisible', 'editIndexed', 'selectItem', 'itemAt',
                'visualRectAt', 'numberOfIcons', 'editable', 'numberOfRows', 'removeAll', 'selectIndexedItem', 'append']
    _CALLBACKS = ['changeCommand', 'doubleClickCommand', 'dropRectCallback', 'selectCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'selectItem'
    _BIND_TGT = 'selectItem'


class IconTextStaticLabel(Control):
    """Wrapper class for cmds.iconTextStaticLabel"""
    CMD = getattr(cmds, 'iconTextStaticLabel', NotImplemented)
    _ATTRIBS = ['imageOverlayLabel', 'style', 'font', 'overlayLabelBackColor', 'disabledImage', 'align', 'label',
                'image3', 'marginWidth', 'image', 'labelOffset', 'image2', 'image1', 'marginHeight',
                'overlayLabelColor']
    _CALLBACKS = []
    _BIND_SRC = 'label'
    _BIND_TGT = 'label'


class Image(Control):
    """Wrapper class for cmds.image"""
    CMD = getattr(cmds, 'image', NotImplemented)
    _ATTRIBS = ['image']
    _CALLBACKS = []


class IntField(Control):
    """Wrapper class for cmds.intField"""
    CMD = getattr(cmds, 'intField', NotImplemented)
    _ATTRIBS = ['step', 'editable', 'maxValue', 'value', 'minValue']
    _CALLBACKS = ['changeCommand', 'dragCommand', 'enterCommand', 'receiveFocusCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class IntFieldGrp(Labeled):
    """Wrapper class for cmds.intFieldGrp"""
    CMD = getattr(cmds, 'intFieldGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'extraLabel', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4',
                'columnAlign3', 'columnAlign2', 'label', 'value4', 'value3', 'numberOfFields', 'value1', 'enable1',
                'enable2', 'adjustableColumn', 'enable4', 'value2', 'columnAlign', 'adjustableColumn3',
                'adjustableColumn2', 'enable3', 'adjustableColumn4', 'adjustableColumn5', 'adjustableColumn6',
                'columnWidth', 'value', 'columnOffset2', 'columnOffset3', 'columnOffset4', 'columnOffset5',
                'columnOffset6', 'columnAttach6', 'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class IntScrollBar(Control):
    """Wrapper class for cmds.intScrollBar"""
    CMD = getattr(cmds, 'intScrollBar', NotImplemented)
    _ATTRIBS = ['largeStep', 'maxValue', 'value', 'minValue', 'step', 'horizontal']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class IntSlider(Control):
    """Wrapper class for cmds.intSlider"""
    CMD = getattr(cmds, 'intSlider', NotImplemented)
    _ATTRIBS = ['horizontal', 'step', 'maxValue', 'value', 'minValue']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class IntSliderGrp(Labeled):
    """Wrapper class for cmds.intSliderGrp"""
    CMD = getattr(cmds, 'intSliderGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'extraLabel', 'minValue', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4',
                'columnAlign3', 'columnAlign2', 'label', 'field', 'columnOffset3', 'adjustableColumn', 'columnAlign',
                'fieldMaxValue', 'maxValue', 'step', 'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4',
                'adjustableColumn5', 'fieldMinValue', 'columnWidth', 'value', 'sliderStep', 'adjustableColumn6',
                'columnOffset2', 'fieldStep', 'columnOffset4', 'columnOffset5', 'columnOffset6', 'columnAttach6',
                'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'dragCommand']
    _BIND_TRIGGER = 'changeCommand'


class LayerButton(Control):
    """Wrapper class for cmds.layerButton"""
    CMD = getattr(cmds, 'layerButton', NotImplemented)
    _ATTRIBS = ['labelWidth', 'name', 'layerVisible', 'color', 'label', 'current', 'layerState', 'identification',
                'transparent', 'select']
    _CALLBACKS = ['command', 'changeCommand', 'doubleClickCommand', 'renameCommand', 'typeCommand', 'visibleCommand']
    _BIND_TRIGGER = 'changeCommand'


class MessageLine(Control):
    """Wrapper class for cmds.messageLine"""
    CMD = getattr(cmds, 'messageLine', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class NameField(Control):
    """Wrapper class for cmds.nameField"""
    CMD = getattr(cmds, 'nameField', NotImplemented)
    _ATTRIBS = ['object']
    _CALLBACKS = ['changeCommand', 'nameChangeCommand', 'receiveFocusCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'object'
    _BIND_TGT = 'object'


class NodeTreeLister(Control):
    """Wrapper class for cmds.nodeTreeLister"""
    CMD = getattr(cmds, 'nodeTreeLister', NotImplemented)
    _ATTRIBS = ['expandToDepth', 'addFavorite', 'executeItem', 'clearContents', 'addItem', 'collapsePath',
                'removeFavorite', 'favoritesList', 'expandPath', 'itemScript', 'selectPath', 'removeItem',
                'resultsPathUnderCursor']
    _CALLBACKS = ['favoritesCallback']


class PalettePort(Control):
    """Wrapper class for cmds.palettePort"""
    CMD = getattr(cmds, 'palettePort', NotImplemented)
    _ATTRIBS = ['colorEditable', 'colorEdited', 'hsvValue', 'setCurCell', 'topDown', 'editable', 'actualTotal',
                'rgbValue', 'redraw', 'transparent', 'dimensions']
    _CALLBACKS = ['changeCommand']
    _BIND_TRIGGER = 'changeCommand'


class Picture(Control):
    """Wrapper class for cmds.picture"""
    CMD = getattr(cmds, 'picture', NotImplemented)
    _ATTRIBS = ['tile', 'image']
    _CALLBACKS = []


class RadioButton(Control):
    """Wrapper class for cmds.radioButton"""
    CMD = getattr(cmds, 'radioButton', NotImplemented)
    _ATTRIBS = ['align', 'editable', 'collection', 'label', 'recomputeSize', 'data', 'select']
    _CALLBACKS = ['changeCommand', 'offCommand', 'onCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'


class RadioButtonGrp(Labeled):
    """Wrapper class for cmds.radioButtonGrp"""
    CMD = getattr(cmds, 'radioButtonGrp', NotImplemented)
    _ATTRIBS = ['rowAttach', 'columnAttach', 'columnWidth2', 'columnWidth3', 'columnWidth1', 'columnWidth6', 'select',
                'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4', 'columnAlign3', 'columnAlign2', 'label',
                'columnWidth4', 'editable', 'data4', 'enable2', 'adjustableColumn', 'enable4', 'data3', 'data2',
                'columnAlign', 'vertical', 'label1', 'label2', 'label3', 'label4', 'adjustableColumn3', 'enable1',
                'labelArray4', 'labelArray2', 'labelArray3', 'adjustableColumn2', 'enable3', 'adjustableColumn4',
                'adjustableColumn5', 'adjustableColumn6', 'numberOfRadioButtons', 'data1', 'shareCollection',
                'columnOffset2', 'columnOffset3', 'columnOffset4', 'columnOffset5', 'columnOffset6', 'columnWidth',
                'columnAttach6', 'columnAttach4', 'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'changeCommand1', 'changeCommand2', 'changeCommand3', 'changeCommand4', 'offCommand',
                  'offCommand1', 'offCommand2', 'offCommand3', 'offCommand4', 'onCommand', 'onCommand1', 'onCommand2',
                  'onCommand3', 'onCommand4']
    _BIND_TRIGGER = 'changeCommand'


class RadioCollection(Control):
    """Wrapper class for cmds.radioCollection

    This class adds an artificial 'changeCommand' event to the default maya RadioCollection
    so it's possible to track the collection instead of the individual items in the collection
    in a binding or with events
    """
    CMD = getattr(cmds, 'radioCollection', NotImplemented)
    _ATTRIBS = ['collectionItemArray', 'global', 'numberOfCollectionItems', 'select']
    _CALLBACKS = []

    _BIND_SRC = 'select'
    _BIND_TRIGGER = 'changeCommand'
    _CHILD_CLASS = RadioButton

    def __init__(self, key=None, **kwargs):
        super(RadioCollection, self).__init__(key=key, **kwargs)
        self.changeCommand = Event(sender=weakref.proxy(self))
        self.members = []
        self.last_state = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise
        for item in self.collectionItemArray:
            proxy = self._CHILD_CLASS.wrap(item)
            self.members.append(proxy)
            proxy.changeCommand += self._handle_change

    def _handle_change(self, *_, **__):
        state = self.select
        if state != self.last_state:
            self.changeCommand()
            self.last_state = state

    def forget(self, *args, **kwargs):
        self.members = None
        super(RadioCollection, self).forget()


class IconTextRadioButton(Control):
    """Wrapper class for cmds.iconTextRadioButton"""
    CMD = getattr(cmds, 'iconTextRadioButton', NotImplemented)
    _ATTRIBS = ['imageOverlayLabel', 'marginHeight', 'style', 'overlayLabelColor', 'overlayLabelBackColor',
                'highlightImage', 'image1', 'selectionHighlightImage', 'label', 'collection', 'selectionImage', 'align',
                'image3', 'marginWidth', 'labelOffset', 'image2', 'disabledImage', 'font', 'image', 'select']
    _CALLBACKS = ['changeCommand', 'offCommand', 'onCommand']
    _BIND_TRIGGER = 'changeCommand'
    _BIND_SRC = 'select'
    _BIND_TGT = 'select'


class IconTextRadioCollection(RadioCollection):
    """Wrapper class for cmds.iconTextRadioCollection"""
    CMD = getattr(cmds, 'iconTextRadioCollection', NotImplemented)
    _ATTRIBS = ['collectionItemArray', 'global', 'numberOfCollectionItems', 'select']
    _CALLBACKS = ['disableCommands']
    _BIND_SRC = 'select'
    _BIND_TGT = 'select'
    _CHILD_CLASS = IconTextRadioButton


class RangeControl(Control):
    """Wrapper class for cmds.rangeControl"""
    CMD = getattr(cmds, 'rangeControl', NotImplemented)
    _ATTRIBS = ['maxRange', 'minRange', 'widthHeight']
    _CALLBACKS = ['changedCommand']
    _BIND_TRIGGER = 'changedCommand'


class ScriptTable(Control):
    """Wrapper class for cmds.scriptTable"""
    CMD = getattr(cmds, 'scriptTable', NotImplemented)
    _ATTRIBS = ['insertRow', 'rows', 'selectedRow', 'clearTable', 'clearRow', 'deleteRow', 'cellChangedCmd', 'label',
                'underPointerRow', 'getCellCmd', 'columnWidth', 'columns']
    _CALLBACKS = []


class ScrollField(Control):
    """Wrapper class for cmds.scrollField"""
    CMD = getattr(cmds, 'scrollField', NotImplemented)
    _ATTRIBS = ['insertText', 'selection', 'insertionPosition', 'numberOfLines', 'text', 'clear', 'editable', 'command',
                'wordWrap', 'font']
    _CALLBACKS = ['changeCommand', 'enterCommand', 'keyPressCommand']
    _BIND_TRIGGER = 'changeCommand'


class Separator(Control):
    """Wrapper class for cmds.separator"""
    CMD = getattr(cmds, 'separator', NotImplemented)
    _ATTRIBS = ['horizontal', 'style']
    _CALLBACKS = []


class ShelfButton(Control):
    """Wrapper class for cmds.shelfButton"""
    CMD = getattr(cmds, 'shelfButton', NotImplemented)
    _ATTRIBS = ['imageOverlayLabel', 'image', 'commandRepeatable', 'menuItemPython', 'menuItem', 'marginWidth', 'label',
                'image1', 'actionIsSubstitute', 'style', 'font', 'selectionImage', 'labelOffset', 'sourceType',
                'image3', 'image2', 'disabledImage', 'overlayLabelBackColor', 'align', 'highlightImage', 'command',
                'marginHeight', 'overlayLabelColor']
    _CALLBACKS = ['doubleClickCommand', 'enableCommandRepeat', 'handleNodeDropCallback', 'labelEditingCallback']


class SoundControl(Control):
    """Wrapper class for cmds.soundControl"""
    CMD = getattr(cmds, 'soundControl', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class SwatchDisplayPort(Control):
    """Wrapper class for cmds.swatchDisplayPort"""
    CMD = getattr(cmds, 'swatchDisplayPort', NotImplemented)
    _ATTRIBS = ['borderWidth', 'borderColor', 'widthHeight', 'shadingNode']
    _CALLBACKS = ['pressCommand']


class SwitchTable(Control):
    """Wrapper class for cmds.switchTable"""
    CMD = getattr(cmds, 'switchTable', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class SymbolButton(Control):
    """Wrapper class for cmds.symbolButton"""
    CMD = getattr(cmds, 'symbolButton', NotImplemented)
    _ATTRIBS = ['image']
    _CALLBACKS = ['command']


class SymbolCheckBox(Control):
    """Wrapper class for cmds.symbolCheckBox"""
    CMD = getattr(cmds, 'symbolCheckBox', NotImplemented)
    _ATTRIBS = ['innerMargin', 'offImage', 'image', 'disableOffImage', 'value', 'disableOnImage', 'onImage']
    _CALLBACKS = ['changeCommand', 'offCommand', 'onCommand']
    _BIND_SRC = 'value'
    _BIND_TGT = 'value'
    _BIND_TRIGGER = 'changeCommand'


class Text(Control):
    """Wrapper class for cmds.text"""
    CMD = getattr(cmds, 'text', NotImplemented)
    _ATTRIBS = ['hyperlink', 'align', 'label', 'wordWrap', 'recomputeSize', 'font']
    _CALLBACKS = ['dropRectCallback']
    _BIND_TGT = 'label'
    _BIND_SRC = 'label'


class TextField(Control):
    """Wrapper class for cmds.textField"""
    CMD = getattr(cmds, 'textField', NotImplemented)
    _ATTRIBS = ['alwaysInvokeEnterCommandOnReturn', 'insertText', 'insertionPosition', 'text', 'editable', 'fileName', 'font']
    _CALLBACKS = ['changeCommand', 'enterCommand', 'receiveFocusCommand']
    _BIND_SRC = 'text'
    _BIND_TGT = 'text'
    _BIND_TRIGGER = 'changeCommand'


class TextFieldButtonGrp(Labeled):
    """Wrapper class for cmds.textFieldButtonGrp"""
    CMD = getattr(cmds, 'textFieldButtonGrp', NotImplemented)
    _ATTRIBS = ['insertText', 'enableButton', 'rowAttach', 'columnAttach', 'columnWidth2', 'columnWidth3',
                'columnWidth1', 'columnWidth6', 'buttonLabel', 'columnWidth4', 'columnWidth5', 'columnAlign6',
                'columnAlign5', 'columnAlign4', 'columnAlign3', 'columnAlign2', 'insertionPosition', 'label', 'text',
                'adjustableColumn', 'columnAlign', 'editable', 'fileName', 'adjustableColumn2', 'adjustableColumn3',
                'adjustableColumn4', 'adjustableColumn5', 'adjustableColumn6', 'columnWidth', 'columnOffset2',
                'columnOffset3', 'columnOffset4', 'columnOffset5', 'columnOffset6', 'columnAttach6', 'columnAttach4',
                'columnAttach5', 'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['buttonCommand', 'changeCommand', 'forceChangeCommand']
    _BIND_SRC = 'text'
    _BIND_TGT = 'text'
    _BIND_TRIGGER = 'changeCommand'


class TextFieldGrp(Labeled):
    """Wrapper class for cmds.textFieldGrp"""
    CMD = getattr(cmds, 'textFieldGrp', NotImplemented)
    _ATTRIBS = ['insertText', 'text', 'rowAttach', 'columnAttach', 'columnWidth2', 'columnWidth3', 'columnWidth1',
                'columnWidth6', 'columnWidth4', 'columnWidth5', 'columnAlign6', 'columnAlign5', 'columnAlign4',
                'columnAlign3', 'columnAlign2', 'insertionPosition', 'label', 'adjustableColumn', 'columnAlign',
                'editable', 'fileName', 'adjustableColumn2', 'adjustableColumn3', 'adjustableColumn4',
                'adjustableColumn5', 'adjustableColumn6', 'columnWidth', 'columnOffset2', 'columnOffset3',
                'columnOffset4', 'columnOffset5', 'columnOffset6', 'columnAttach6', 'columnAttach4', 'columnAttach5',
                'columnAttach2', 'columnAttach3']
    _CALLBACKS = ['changeCommand', 'forceChangeCommand']
    _BIND_SRC = 'text'
    _BIND_TGT = 'text'
    _BIND_TRIGGER = 'changeCommand'


class TextScrollList(Control):
    """Wrapper class for cmds.textScrollList"""
    CMD = getattr(cmds, 'textScrollList', NotImplemented)
    _ATTRIBS = ['showIndexedItem', 'deselectAll', 'selectIndexedItem', 'allowAutomaticSelection', 'selectItem',
                'deselectItem', 'allowMultiSelection', 'appendPosition', 'font', 'numberOfRows', 'removeAll',
                'removeIndexedItem', 'append', 'removeItem', 'numberOfSelectedItems', 'allItems', 'deselectIndexedItem',
                'numberOfItems']
    _CALLBACKS = ['deleteKeyCommand', 'doubleClickCommand', 'selectCommand']
    _BIND_TRIGGER = 'selectCommand'
    _BIND_SRC = 'selectItem'
    _BIND_TGT = 'selectItem'

    @property
    def items(self):
        return self.allItems or []

    @items.setter
    def items(self, items):
        self.removeAll = True
        self.append = tuple(str(i) for i in items)

    def clear(self):
        self.removeAll = True


class TimeControl(Control):
    """Wrapper class for cmds.timeControl"""
    CMD = getattr(cmds, 'timeControl', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class TimePort(Control):
    """Wrapper class for cmds.timePort"""
    CMD = getattr(cmds, 'timePort', NotImplemented)
    _ATTRIBS = []
    _CALLBACKS = []


class ToolButton(Control):
    """Wrapper class for cmds.toolButton"""
    CMD = getattr(cmds, 'toolButton', NotImplemented)
    _ATTRIBS = ['imageOverlayLabel', 'style', 'allowMultipleTools', 'tool', 'toolCount', 'collection', 'toolArray',
                'toolImage1', 'toolImage3', 'toolImage2', 'image3', 'image2', 'image1', 'popupIndicatorVisible',
                'select']
    _CALLBACKS = ['changeCommand', 'doubleClickCommand', 'offCommand', 'onCommand']
    _BIND_TRIGGER = 'changeCommand'


class ToolCollection(Control):
    """Wrapper class for cmds.toolCollection"""
    CMD = getattr(cmds, 'toolCollection', NotImplemented)
    _ATTRIBS = ['collectionItemArray', 'global', 'numberOfCollectionItems', 'select']
    _CALLBACKS = []


class TreeLister(Control):
    """Wrapper class for cmds.treeLister"""
    CMD = getattr(cmds, 'treeLister', NotImplemented)
    _ATTRIBS = ['expandToDepth', 'addFavorite', 'executeItem', 'clearContents', 'addItem', 'collapsePath',
                'removeFavorite', 'favoritesList', 'expandPath', 'itemScript', 'selectPath', 'removeItem',
                'resultsPathUnderCursor']
    _CALLBACKS = ['favoritesCallback']


class TreeView(Control):
    """Wrapper class for cmds.treeView"""
    CMD = getattr(cmds, 'treeView', NotImplemented)
    _ATTRIBS = ['buttonState', 'enableButton', 'image', 'showItem', 'buttonVisible', 'buttonTransparencyColor',
                'allowReparenting', 'buttonStyle', 'itemVisible', 'font', 'children', 'select', 'clearSelection',
                'attachButtonRight', 'expandItem', 'ornament', 'itemParent', 'buttonTextIcon', 'allowHiddenParents',
                'numberOfButtons', 'buttonTransparencyOverride', 'textColor', 'buttonTooltip', 'itemIndex',
                'enableKeys', 'displayLabelSuffix', 'reverseTreeOrder', 'highliteColor', 'addItem', 'isItemExpanded',
                'highlite', 'selectionColor', 'borderHighliteColor', 'flatButton', 'isLeaf', 'displayLabel',
                'borderHighlite', 'enableLabel', 'selectItem', 'labelBackgroundColor', 'ornamentColor',
                'allowDragAndDrop', 'removeAll', 'fontFace', 'itemSelected', 'itemExists', 'hideButtons']
    _CALLBACKS = ['contextMenuCommand', 'dragAndDropCommand', 'editLabelCommand', 'expandCollapseCommand',
                  'itemDblClickCommand', 'itemRenamedCommand', 'pressCommand', 'rightPressCommand', 'selectCommand',
                  'selectionChangedCommand']
    _BIND_TRIGGER = 'selectionChangedCommand'


class WorkspaceControl(Nested):
    '''Wrapper class for cmds.workspaceControl'''
    CMD = getattr(cmds, 'workspaceControl', NotImplemented)
    _ATTRIBS = ['restore', 'dockToPanel', 'tabPosition', 'initialHeight', 'widthProperty', 'requiredControl',
                'close', 'tabToControl', 'floating', 'stateString', 'r', 'dockToMainWindow',
                'uiScript', 'label', 'checksPlugins', 'initialWidth', 'minimumWidth', 'collapse',
                'requiredPlugin', 'dockToControl', 'horizontal', 'heightProperty', 'loadImmediately', 'duplicatable']
    _CALLBACKS = ['initCallback']

    def __init__(self, key=None, **kwargs):
        if key is None:
            for i in _count(1):
                key = 'WorkspaceControl{!s}'.format(i)
                if not self.CMD(key, exists=True):
                    break
        super(WorkspaceControl, self).__init__(key, **kwargs)
        self.bindingContext = _BindingContext()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def __enter__(self):
        self.bindingContext.__enter__()
        return super(WorkspaceControl, self).__enter__()

    def __exit__(self, typ, value, traceback):
        self.bindingContext.__exit__(None, None, None)
        mGui_expand_stack = True
        super(WorkspaceControl, self).__exit__(typ, value, traceback)

    def update_bindings(self):
        self.bindingContext.update(True)

    def forget(self, *args, **kwargs):
        super(WorkspaceControl, self).forget()
        self.bindingContext = None