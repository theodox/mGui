"""
This is a list of common attributes which are always present in all controls.  They are inherited from the Control
base class so we suppress them in template generation
"""
CONTROL_ATTRIBS = [
    'en', 'enable',
    'm', 'manage',
    'ann', 'annotation',
    'vis', 'visible',
    'ebg', 'enableBackground',
    'ex', 'exists',
    'io', 'isObscured',
    'vcc', 'visibleChangeCommand',
    'fpn', 'fullPathName',
    'po', 'preventOverride',
    'npm', 'numberOfPopupMenus',
    'dgc', 'dragCallback',
    'dt', 'defineTemplate',
    'bgc', 'backgroundColor',
    'e', 'edit',
    'h', 'height',
    'dtg', 'docTag',
    'q', 'query',
    'p', 'parent',
    'dpc', 'dropCallback',
    'w', 'width',
    'ut', 'useTemplate',
    'pma', 'popupMenuArray']

'''
Common attribs for all layouts (a superset of the control attribs)
'''
LAYOUT_ATTRIBS = [
    'ca', 'childArray',
    'nch', 'numberOfChildren']

'''
This is a list of all the control commands, which we use to generate the wrappers
'''
CONTROL_COMMANDS = [
    'attrColorSliderGrp',
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

'''
All of the default layout items
'''
LAYOUT_COMMANDS = [
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


'''
All the default panel types
'''
PANEL_COMMANDS = ["componentEditor",
                  "hardwareRenderPanel",
                  "hyperGraph",
                  "hyperPanel",
                  "hyperShade",
                  "modelEditor",
                  "modelPanel",
                  "nodeOutliner",
                  "outlinerEditor",
                  "outlinerPanel",
                  "panel",
                  "panelConfiguration",
                  "panelHistory",
                  "scriptedPanel",
                  "spreadSheetEditor",
                  "visor",
                  "webBrowser"
]