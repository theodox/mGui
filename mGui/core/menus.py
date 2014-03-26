'''
mGui.menus

Wrapper classes for Menus and MenuItems
'''

from mGui.core import Nested, Control, cmds


class Menu(Nested):
    CMD = cmds.menu
    _ATTRIBS = ['allowOptionBoxes', 'deleteAllItems', 'defineTemplate', 'docTag',  'enable', 'enableBackground', 'exists', 'familyImage', 'helpMenu',   'label', 'mnemonic', 'parent',  'useTemplate', 'visible']
    _CALLBACKS = ['postMenuCommand', 'postMenuCommandOnce']
    _READ_ONLY = ['itemArray', 'numberOfItems']


class MenuItem(Control):
    CMD = cmds.menuItem
    _ATTRIBS= ["altModifier","annotation","allowOptionBoxes","boldFont","checkBox","collection","commandModifier","ctrlModifier","divider","data","defineTemplate","docTag","echoCommand","enableCommandRepeat","enable","exists","familyImage","image","insertAfter","imageOverlayLabel","italicized","keyEquivalent","label","mnemonic","optionBox","optionBoxIcon","optionModifier","parent","radioButton","radialPosition","shiftModifier","subMenu","sourceType","tearOff","useTemplate", "version"]
    _READ_ONLY = ['isCheckBox', 'isOptionBox', 'isRadioButton']             
    _CALLBACKS = ['command', 'dragDoubleClickCommand', 'dragMenuCommand','postMenuCommand', 'postMenuCommandOnce']
    

