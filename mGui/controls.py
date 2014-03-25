'''
mGui wrapper classes

Originally auto generated using helpers.tools
'''

import maya.cmds as cmds
from .core import Control


class Labeled(Control):
    '''
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
    '''
    pass


class AttrColorSliderGrp(Labeled):
    '''Wrapper class for cmds.attrColorSliderGrp'''
    CMD = cmds.attrColorSliderGrp
    _ATTRIBS = ['attribute','rowAttach','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','adjustableColumn','columnAlign','columnAttach6','adjustableColumn5','adjustableColumn2','adjustableColumn3','adjustableColumn4','showButton','hsvValue','columnWidth','adjustableColumn6','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','rgbValue','attrNavDecision','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = []


class AttrControlGrp(Labeled):
    '''Wrapper class for cmds.attrControlGrp'''
    CMD = cmds.attrControlGrp
    _ATTRIBS = ['attribute','handlesAttribute','label','hideMapButton']
    _CALLBACKS = ['changeCommand']


class AttrFieldGrp(Labeled):
    '''Wrapper class for cmds.attrFieldGrp'''
    CMD = cmds.attrFieldGrp
    _ATTRIBS = ['attribute','rowAttach','columnAttach','extraLabel','minValue','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','numberOfFields','adjustableColumn','columnAlign','maxValue','precision','step','hideMapButton','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand']


class AttrFieldSliderGrp(Labeled):
    '''Wrapper class for cmds.attrFieldSliderGrp'''
    CMD = cmds.attrFieldSliderGrp
    _ATTRIBS = ['attribute','rowAttach','sliderMaxValue','columnAttach','minValue','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','columnOffset3','adjustableColumn','columnAlign','vertical','sliderMinValue','fieldMaxValue','maxValue','precision','step','hideMapButton','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','fieldMinValue','columnWidth','sliderStep','adjustableColumn6','columnOffset2','fieldStep','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand']


class AttrNavigationControlGrp(Labeled):
    '''Wrapper class for cmds.attrNavigationControlGrp'''
    CMD = cmds.attrNavigationControlGrp
    _ATTRIBS = ['connectAttrToDropped','attribute','rowAttach','columnAttach','createNew','adjustableColumn3','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','columnOffset4','adjustableColumn','columnAlign','unignore','connectToExisting','disconnect','ignoreNotSupported','adjustableColumn2','defaultTraversal','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','columnAttach3','ignore','columnOffset2','columnOffset3','relatedNodes','columnOffset5','columnOffset6','columnAttach6','attrNavDecision','columnAttach4','columnAttach5','columnAttach2','connectNodeToDropped','delete']
    _CALLBACKS = []


class Button(Control):
    '''Wrapper class for cmds.button'''
    CMD = cmds.button
    _ATTRIBS = ['actionIsSubstitute','actOnPress','align','label','recomputeSize']
    _CALLBACKS = ['command']

class Canvas(Control):
    '''Wrapper class for cmds.canvas'''
    CMD = cmds.canvas
    _ATTRIBS = ['rgbValue','hsvValue']
    _CALLBACKS = ['pressCommand']


class ChannelBox(Control):
    '''Wrapper class for cmds.channelBox'''
    CMD = cmds.channelBox
    _ATTRIBS = []
    _CALLBACKS = []


class CheckBox(Control):
    '''Wrapper class for cmds.checkBox'''
    CMD = cmds.checkBox
    _ATTRIBS = ['recomputeSize','align','editable','value','label']
    _CALLBACKS = ['changeCommand','offCommand','onCommand']


class CheckBoxGrp(Labeled):
    '''Wrapper class for cmds.checkBoxGrp'''
    CMD = cmds.checkBoxGrp
    _ATTRIBS = ['rowAttach','columnAttach','labelArray3','adjustableColumn3','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','numberOfCheckBoxes','value4','value3','value2','value1','editable','enable1','enable2','enable3','enable4','columnAlign','vertical','label1','label2','label3','label4','valueArray3','valueArray2','labelArray4','labelArray2','valueArray4','adjustableColumn2','adjustableColumn','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','changeCommand1','changeCommand2','changeCommand3','changeCommand4','offCommand','offCommand1','offCommand2','offCommand3','offCommand4','onCommand','onCommand1','onCommand2','onCommand3','onCommand4']


class CmdScrollFieldExecuter(Control):
    '''Wrapper class for cmds.cmdScrollFieldExecuter'''
    CMD = cmds.cmdScrollFieldExecuter
    _ATTRIBS = ['insertText','load','searchAndSelect','text','saveSelection','spacesPerTab','filterKeyPress','redo','select','indentSelection','searchWraps','currentLine','removeStoredContents','copySelection','hasFocus','showTooltipHelp','objectPathCompletion','storeContents','hasSelection','appendText','unindentSelection','saveSelectionToShelf','sourceType','cutSelection','selectAll','numberOfLines','replaceAll','executeAll','undo','showLineNumbers','commandCompletion','execute','searchString','loadContents','textLength','clear','selectedText','searchDown','searchMatchCase','source','pasteSelection','tabsForIndent']
    _CALLBACKS = ['receiveFocusCommand']


class CmdScrollFieldReporter(Control):
    '''Wrapper class for cmds.cmdScrollFieldReporter'''
    CMD = cmds.cmdScrollFieldReporter
    _ATTRIBS = ['selectAll','stackTrace','saveSelectionToShelf','suppressWarnings','cutSelection','suppressInfo','hasFocus','text','clear','textLength','copySelection','lineNumbers','suppressStackTrace','saveSelection','suppressResults','suppressErrors','pasteSelection','filterSourceType','select']
    _CALLBACKS = ['echoAllCommands','receiveFocusCommand']


class CmdShell(Control):
    '''Wrapper class for cmds.cmdShell'''
    CMD = cmds.cmdShell
    _ATTRIBS = ['numberOfHistoryLines','clear','command','numberOfSavedLines','prompt']
    _CALLBACKS = []


class ColorIndexSliderGrp(Labeled):
    '''Wrapper class for cmds.colorIndexSliderGrp'''
    CMD = cmds.colorIndexSliderGrp
    _ATTRIBS = ['rowAttach','columnAttach','extraLabel','minValue','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','adjustableColumn','columnAlign','maxValue','forceDragRefresh','invisible','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','value','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','dragCommand']


class ColorSliderButtonGrp(Labeled):
    '''Wrapper class for cmds.colorSliderButtonGrp'''
    CMD = cmds.colorSliderButtonGrp
    _ATTRIBS = ['image','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','buttonLabel','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','adjustableColumn','rowAttach','columnAlign','forceDragRefresh','columnAttach6','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','hsvValue','columnWidth','adjustableColumn6','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','rgbValue','symbolButtonDisplay','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['buttonCommand','changeCommand','dragCommand','symbolButtonCommand']


class ColorSliderGrp(Labeled):
    '''Wrapper class for cmds.colorSliderGrp'''
    CMD = cmds.colorSliderGrp
    _ATTRIBS = ['rowAttach','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','adjustableColumn','columnAlign','forceDragRefresh','columnAttach6','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','hsvValue','columnWidth','adjustableColumn6','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','rgbValue','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','dragCommand']


class CommandLine(Control):
    '''Wrapper class for cmds.commandLine'''
    CMD = cmds.commandLine
    _ATTRIBS = ['holdFocus','outputAnnotation','inputAnnotation','sourceType','numberOfHistoryLines','command']
    _CALLBACKS = ['enterCommand']


class ComponentBox(Control):
    '''Wrapper class for cmds.componentBox'''
    CMD = cmds.componentBox
    _ATTRIBS = []
    _CALLBACKS = []


class FloatField(Control):
    '''Wrapper class for cmds.floatField'''
    CMD = cmds.floatField
    _ATTRIBS = ['editable','precision','value','maxValue','step','minValue']
    _CALLBACKS = ['changeCommand','dragCommand','enterCommand','receiveFocusCommand']


class FloatFieldGrp(Labeled):
    '''Wrapper class for cmds.floatFieldGrp'''
    CMD = cmds.floatFieldGrp
    _ATTRIBS = ['rowAttach','columnAttach','extraLabel','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','value4','value3','numberOfFields','value1','enable1','enable2','adjustableColumn','enable4','value2','columnAlign','precision','adjustableColumn3','adjustableColumn2','enable3','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','value','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','dragCommand']


class FloatScrollBar(Control):
    '''Wrapper class for cmds.floatScrollBar'''
    CMD = cmds.floatScrollBar
    _ATTRIBS = ['largeStep','maxValue','value','minValue','step','horizontal']
    _CALLBACKS = ['changeCommand','dragCommand']


class FloatSlider(Control):
    '''Wrapper class for cmds.floatSlider'''
    CMD = cmds.floatSlider
    _ATTRIBS = ['horizontal','step','maxValue','value','minValue']
    _CALLBACKS = ['changeCommand','dragCommand']


class FloatSlider2(Control):
    '''Wrapper class for cmds.floatSlider2'''
    CMD = cmds.floatSlider2
    _ATTRIBS = []
    _CALLBACKS = []


class FloatSliderButtonGrp(Labeled):
    '''Wrapper class for cmds.floatSliderButtonGrp'''
    CMD = cmds.floatSliderButtonGrp
    _ATTRIBS = ['rowAttach','columnAttach','extraLabel','minValue','columnWidth2','columnWidth3','columnWidth1','columnWidth6','buttonLabel','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','field','columnOffset3','adjustableColumn','image','columnAlign','fieldMaxValue','maxValue','precision','step','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','fieldMinValue','columnWidth','value','sliderStep','adjustableColumn6','columnOffset2','fieldStep','columnOffset4','columnOffset5','columnOffset6','columnAttach6','symbolButtonDisplay','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['buttonCommand','changeCommand','dragCommand','symbolButtonCommand']


class FloatSliderGrp(Labeled):
    '''Wrapper class for cmds.floatSliderGrp'''
    CMD = cmds.floatSliderGrp
    _ATTRIBS = ['rowAttach','columnAttach','extraLabel','minValue','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','field','columnOffset3','adjustableColumn','columnAlign','fieldMaxValue','maxValue','precision','step','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','fieldMinValue','columnWidth','value','sliderStep','adjustableColumn6','columnOffset2','fieldStep','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','dragCommand']


class GradientControl(Control):
    '''Wrapper class for cmds.gradientControl'''
    CMD = cmds.gradientControl
    _ATTRIBS = ['upperLimitControl','adaptiveScaling','refreshOnRelease','selectedPositionControl','attribute','numberOfControls','staticPositions','staticNumberOfControls','verticalLayout','selectedInterpControl','selectedColorControl']
    _CALLBACKS = []


class GradientControlNoAttr(Control):
    '''Wrapper class for cmds.gradientControlNoAttr'''
    CMD = cmds.gradientControlNoAttr
    _ATTRIBS = ['currentKeyColorValue','currentKeyChanged','rampAsColor','optionVar','currentKeyCurveValue','valueAtPoint','asString','currentKeyInterpValue','currentKey']
    _CALLBACKS = ['changeCommand','dragCommand']


class HelpLine(Control):
    '''Wrapper class for cmds.helpLine'''
    CMD = cmds.helpLine
    _ATTRIBS = []
    _CALLBACKS = []


class HudButton(Control):
    '''Wrapper class for cmds.hudButton'''
    CMD = cmds.hudButton
    _ATTRIBS = ['allowOverlap','blockAlignment','buttonWidth','buttonShape','blockSize','section','label','padding','labelFontSize','block']
    _CALLBACKS = ['pressCommand','releaseCommand']


class HudSlider(Control):
    '''Wrapper class for cmds.hudSlider'''
    CMD = cmds.hudSlider
    _ATTRIBS = ['valueAlignment','internalPadding','decimalPrecision','labelWidth','labelFontSize','blockSize','valueFontSize','sliderLength','maxValue','value','minValue','padding','valueWidth','block','sliderIncrement','allowOverlap','label','type','section','blockAlignment']
    _CALLBACKS = ['dragCommand','pressCommand','releaseCommand']


class HudSliderButton(Control):
    '''Wrapper class for cmds.hudSliderButton'''
    CMD = cmds.hudSliderButton
    _ATTRIBS = ['valueAlignment','internalPadding','decimalPrecision','buttonLabelFontSize','valueFontSize','sliderLength','minValue','blockAlignment','buttonLabel','sliderLabelFontSize','sliderLabel','buttonShape','blockSize','section','type','allowOverlap','maxValue','padding','sliderIncrement','sliderLabelWidth','value','valueWidth','buttonWidth','block']
    _CALLBACKS = ['buttonPressCommand','buttonReleaseCommand','sliderDragCommand','sliderPressCommand','sliderReleaseCommand']


class IconTextButton(Control):
    '''Wrapper class for cmds.iconTextButton'''
    CMD = cmds.iconTextButton
    _ATTRIBS = ['imageOverlayLabel','actionIsSubstitute','style','font','marginHeight','sourceType','overlayLabelColor','align','image','label','selectionImage','image3','highlightImage','marginWidth','labelOffset','image2','disabledImage','commandRepeatable','image1','overlayLabelBackColor']
    _CALLBACKS = ['command', 'doubleClickCommand','handleNodeDropCallback','labelEditingCallback']


class IconTextCheckBox(Control):
    '''Wrapper class for cmds.iconTextCheckBox'''
    CMD = cmds.iconTextCheckBox
    _ATTRIBS = ['imageOverlayLabel','marginHeight','style','overlayLabelColor','overlayLabelBackColor','highlightImage','image1','selectionHighlightImage','label','value','selectionImage','align','image3','marginWidth','labelOffset','image2','disabledImage','font','image']
    _CALLBACKS = ['changeCommand','offCommand','onCommand']


class IconTextRadioButton(Control):
    '''Wrapper class for cmds.iconTextRadioButton'''
    CMD = cmds.iconTextRadioButton
    _ATTRIBS = ['imageOverlayLabel','marginHeight','style','overlayLabelColor','overlayLabelBackColor','highlightImage','image1','selectionHighlightImage','label','collection','selectionImage','align','image3','marginWidth','labelOffset','image2','disabledImage','font','image','select']
    _CALLBACKS = ['changeCommand','offCommand','onCommand']


class IconTextRadioCollection(Control):
    '''Wrapper class for cmds.iconTextRadioCollection'''
    CMD = cmds.iconTextRadioCollection
    _ATTRIBS = ['collectionItemArray','global','numberOfCollectionItems','select']
    _CALLBACKS = ['disableCommands']


class IconTextScrollList(Control):
    '''Wrapper class for cmds.iconTextScrollList'''
    CMD = cmds.iconTextScrollList
    _ATTRIBS = ['deselectAll','allowMultiSelection','dragFeedbackVisible','editIndexed','selectItem','itemAt','visualRectAt','numberOfIcons','editable','numberOfRows','removeAll','selectIndexedItem','append']
    _CALLBACKS = ['changeCommand','doubleClickCommand','dropRectCallback','selectCommand']


class IconTextStaticLabel(Control):
    '''Wrapper class for cmds.iconTextStaticLabel'''
    CMD = cmds.iconTextStaticLabel
    _ATTRIBS = ['imageOverlayLabel','style','font','overlayLabelBackColor','disabledImage','align','label','image3','marginWidth','image','labelOffset','image2','image1','marginHeight','overlayLabelColor']
    _CALLBACKS = []


class Image(Control):
    '''Wrapper class for cmds.image'''
    CMD = cmds.image
    _ATTRIBS = ['image']
    _CALLBACKS = []


class IntField(Control):
    '''Wrapper class for cmds.intField'''
    CMD = cmds.intField
    _ATTRIBS = ['step','editable','maxValue','value','minValue']
    _CALLBACKS = ['changeCommand','dragCommand','enterCommand','receiveFocusCommand']


class IntFieldGrp(Labeled):
    '''Wrapper class for cmds.intFieldGrp'''
    CMD = cmds.intFieldGrp
    _ATTRIBS = ['rowAttach','columnAttach','extraLabel','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','value4','value3','numberOfFields','value1','enable1','enable2','adjustableColumn','enable4','value2','columnAlign','adjustableColumn3','adjustableColumn2','enable3','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','value','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','dragCommand']


class IntScrollBar(Control):
    '''Wrapper class for cmds.intScrollBar'''
    CMD = cmds.intScrollBar
    _ATTRIBS = ['largeStep','maxValue','value','minValue','step','horizontal']
    _CALLBACKS = ['changeCommand','dragCommand']


class IntSlider(Control):
    '''Wrapper class for cmds.intSlider'''
    CMD = cmds.intSlider
    _ATTRIBS = ['horizontal','step','maxValue','value','minValue']
    _CALLBACKS = ['changeCommand','dragCommand']


class IntSliderGrp(Labeled):
    '''Wrapper class for cmds.intSliderGrp'''
    CMD = cmds.intSliderGrp
    _ATTRIBS = ['rowAttach','columnAttach','extraLabel','minValue','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','field','columnOffset3','adjustableColumn','columnAlign','fieldMaxValue','maxValue','step','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','fieldMinValue','columnWidth','value','sliderStep','adjustableColumn6','columnOffset2','fieldStep','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','dragCommand']


class LayerButton(Control):
    '''Wrapper class for cmds.layerButton'''
    CMD = cmds.layerButton
    _ATTRIBS = ['labelWidth','name','layerVisible','color','label','current','layerState','identification','transparent','select']
    _CALLBACKS = ['command','changeCommand','doubleClickCommand','renameCommand','typeCommand','visibleCommand']


class MessageLine(Control):
    '''Wrapper class for cmds.messageLine'''
    CMD = cmds.messageLine
    _ATTRIBS = []
    _CALLBACKS = []


class NameField(Control):
    '''Wrapper class for cmds.nameField'''
    CMD = cmds.nameField
    _ATTRIBS = ['object']
    _CALLBACKS = ['changeCommand','nameChangeCommand','receiveFocusCommand']


class NodeTreeLister(Control):
    '''Wrapper class for cmds.nodeTreeLister'''
    CMD = cmds.nodeTreeLister
    _ATTRIBS = ['expandToDepth','addFavorite','executeItem','clearContents','addItem','collapsePath','removeFavorite','favoritesList','expandPath','itemScript','selectPath','removeItem','resultsPathUnderCursor']
    _CALLBACKS = ['favoritesCallback']


class PalettePort(Control):
    '''Wrapper class for cmds.palettePort'''
    CMD = cmds.palettePort
    _ATTRIBS = ['colorEditable','colorEdited','hsvValue','setCurCell','topDown','editable','actualTotal','rgbValue','redraw','transparent','dimensions']
    _CALLBACKS = ['changeCommand']


class Picture(Control):
    '''Wrapper class for cmds.picture'''
    CMD = cmds.picture
    _ATTRIBS = ['tile','image']
    _CALLBACKS = []


class ProgressBar(Control):
    '''Wrapper class for cmds.progressBar'''
    CMD = cmds.progressBar
    _ATTRIBS = ['status','endProgress','isCancelled','maxValue','isInterruptable','isMainProgressBar','step','progress','beginProgress','minValue']
    _CALLBACKS = []


class RadioButton(Control):
    '''Wrapper class for cmds.radioButton'''
    CMD = cmds.radioButton
    _ATTRIBS = ['align','editable','collection','label','recomputeSize','data','select']
    _CALLBACKS = ['changeCommand','offCommand','onCommand']


class RadioButtonGrp(Labeled):
    '''Wrapper class for cmds.radioButtonGrp'''
    CMD = cmds.radioButtonGrp
    _ATTRIBS = ['rowAttach','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','select','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','label','columnWidth4','editable','data4','enable2','adjustableColumn','enable4','data3','data2','columnAlign','vertical','label1','label2','label3','label4','adjustableColumn3','enable1','labelArray4','labelArray2','labelArray3','adjustableColumn2','enable3','adjustableColumn4','adjustableColumn5','adjustableColumn6','numberOfRadioButtons','data1','shareCollection','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnWidth','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','changeCommand1','changeCommand2','changeCommand3','changeCommand4','offCommand','offCommand1','offCommand2','offCommand3','offCommand4','onCommand','onCommand1','onCommand2','onCommand3','onCommand4']


class RadioCollection(Control):
    '''Wrapper class for cmds.radioCollection'''
    CMD = cmds.radioCollection
    _ATTRIBS = ['collectionItemArray','global','numberOfCollectionItems','select']
    _CALLBACKS = []


class RangeControl(Control):
    '''Wrapper class for cmds.rangeControl'''
    CMD = cmds.rangeControl
    _ATTRIBS = ['maxRange','minRange','widthHeight']
    _CALLBACKS = ['changedCommand']


class ScriptTable(Control):
    '''Wrapper class for cmds.scriptTable'''
    CMD = cmds.scriptTable
    _ATTRIBS = ['insertRow','rows','selectedRow','clearTable','clearRow','deleteRow','cellChangedCmd','label','underPointerRow','getCellCmd','columnWidth','columns']
    _CALLBACKS = []


class ScrollField(Control):
    '''Wrapper class for cmds.scrollField'''
    CMD = cmds.scrollField
    _ATTRIBS = ['insertText','selection','insertionPosition','numberOfLines','text','clear','editable','command','wordWrap','font']
    _CALLBACKS = ['changeCommand','enterCommand','keyPressCommand']


class Separator(Control):
    '''Wrapper class for cmds.separator'''
    CMD = cmds.separator
    _ATTRIBS = ['horizontal','style']
    _CALLBACKS = []


class ShelfButton(Control):
    '''Wrapper class for cmds.shelfButton'''
    CMD = cmds.shelfButton
    _ATTRIBS = ['imageOverlayLabel','image','commandRepeatable','menuItemPython','menuItem','marginWidth','label','image1','actionIsSubstitute','style','font','selectionImage','labelOffset','sourceType','image3','image2','disabledImage','overlayLabelBackColor','align','highlightImage','command','marginHeight','overlayLabelColor']
    _CALLBACKS = ['doubleClickCommand','enableCommandRepeat','handleNodeDropCallback','labelEditingCallback']


class SoundControl(Control):
    '''Wrapper class for cmds.soundControl'''
    CMD = cmds.soundControl
    _ATTRIBS = []
    _CALLBACKS = []


class SwatchDisplayPort(Control):
    '''Wrapper class for cmds.swatchDisplayPort'''
    CMD = cmds.swatchDisplayPort
    _ATTRIBS = []
    _CALLBACKS = []


class SwitchTable(Control):
    '''Wrapper class for cmds.switchTable'''
    CMD = cmds.switchTable
    _ATTRIBS = []
    _CALLBACKS = []


class SymbolButton(Control):
    '''Wrapper class for cmds.symbolButton'''
    CMD = cmds.symbolButton
    _ATTRIBS = ['image','command']
    _CALLBACKS = []


class SymbolCheckBox(Control):
    '''Wrapper class for cmds.symbolCheckBox'''
    CMD = cmds.symbolCheckBox
    _ATTRIBS = ['innerMargin','offImage','image','disableOffImage','value','disableOnImage','onImage']
    _CALLBACKS = ['changeCommand','offCommand','onCommand']


class Text(Control):
    '''Wrapper class for cmds.text'''
    CMD = cmds.text
    _ATTRIBS = ['hyperlink','align','label','wordWrap','recomputeSize','font']
    _CALLBACKS = ['dropRectCallback']


class TextField(Control):
    '''Wrapper class for cmds.textField'''
    CMD = cmds.textField
    _ATTRIBS = ['insertText','insertionPosition','text','editable','fileName','font']
    _CALLBACKS = ['alwaysInvokeEnterCommandOnReturn','changeCommand','enterCommand','receiveFocusCommand']


class TextFieldButtonGrp(Labeled):
    '''Wrapper class for cmds.textFieldButtonGrp'''
    CMD = cmds.textFieldButtonGrp
    _ATTRIBS = ['insertText','enableButton','rowAttach','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','buttonLabel','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','insertionPosition','label','text','adjustableColumn','columnAlign','editable','fileName','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['buttonCommand','changeCommand','forceChangeCommand']


class TextFieldGrp(Labeled):
    '''Wrapper class for cmds.textFieldGrp'''
    CMD = cmds.textFieldGrp
    _ATTRIBS = ['insertText','text','rowAttach','columnAttach','columnWidth2','columnWidth3','columnWidth1','columnWidth6','columnWidth4','columnWidth5','columnAlign6','columnAlign5','columnAlign4','columnAlign3','columnAlign2','insertionPosition','label','adjustableColumn','columnAlign','editable','fileName','adjustableColumn2','adjustableColumn3','adjustableColumn4','adjustableColumn5','adjustableColumn6','columnWidth','columnOffset2','columnOffset3','columnOffset4','columnOffset5','columnOffset6','columnAttach6','columnAttach4','columnAttach5','columnAttach2','columnAttach3']
    _CALLBACKS = ['changeCommand','forceChangeCommand']


class TextScrollList(Control):
    '''Wrapper class for cmds.textScrollList'''
    CMD = cmds.textScrollList
    _ATTRIBS = ['showIndexedItem','deselectAll','selectIndexedItem','allowAutomaticSelection','selectItem','deselectItem','allowMultiSelection','appendPosition','font','numberOfRows','removeAll','removeIndexedItem','append','removeItem','numberOfSelectedItems','allItems','deselectIndexedItem','numberOfItems']
    _CALLBACKS = ['deleteKeyCommand','doubleClickCommand','selectCommand']


class TimeControl(Control):
    '''Wrapper class for cmds.timeControl'''
    CMD = cmds.timeControl
    _ATTRIBS = []
    _CALLBACKS = []


class TimePort(Control):
    '''Wrapper class for cmds.timePort'''
    CMD = cmds.timePort
    _ATTRIBS = []
    _CALLBACKS = []


class ToolButton(Control):
    '''Wrapper class for cmds.toolButton'''
    CMD = cmds.toolButton
    _ATTRIBS = ['imageOverlayLabel','style','allowMultipleTools','tool','toolCount','collection','toolArray','toolImage1','toolImage3','toolImage2','image3','image2','image1','popupIndicatorVisible','select']
    _CALLBACKS = ['changeCommand','doubleClickCommand','offCommand','onCommand']


class ToolCollection(Control):
    '''Wrapper class for cmds.toolCollection'''
    CMD = cmds.toolCollection
    _ATTRIBS = ['collectionItemArray','global','numberOfCollectionItems','select']
    _CALLBACKS = []


class TreeLister(Control):
    '''Wrapper class for cmds.treeLister'''
    CMD = cmds.treeLister
    _ATTRIBS = ['expandToDepth','addFavorite','executeItem','clearContents','addItem','collapsePath','removeFavorite','favoritesList','expandPath','itemScript','selectPath','removeItem','resultsPathUnderCursor']
    _CALLBACKS = ['favoritesCallback']


class TreeView(Control):
    '''Wrapper class for cmds.treeView'''
    CMD = cmds.treeView
    _ATTRIBS = ['buttonState','enableButton','image','showItem','buttonVisible','buttonTransparencyColor','allowReparenting','buttonStyle','itemVisible','font','children','select','clearSelection','attachButtonRight','expandItem','ornament','itemParent','buttonTextIcon','allowHiddenParents','numberOfButtons','buttonTransparencyOverride','textColor','buttonTooltip','itemIndex','enableKeys','displayLabelSuffix','reverseTreeOrder','highliteColor','addItem','isItemExpanded','highlite','selectionColor','borderHighliteColor','flatButton','isLeaf','displayLabel','borderHighlite','enableLabel','selectItem','labelBackgroundColor','ornamentColor','allowDragAndDrop','removeAll','fontFace','itemSelected','itemExists','hideButtons']
    _CALLBACKS = ['contextMenuCommand','dragAndDropCommand','editLabelCommand','expandCollapseCommand','itemDblClickCommand','itemRenamedCommand','pressCommand','rightPressCommand','selectCommand','selectionChangedCommand']


