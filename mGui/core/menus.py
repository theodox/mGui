"""
mGui.menus

Wrapper classes for Menus and MenuItems
"""

from mGui.core import Nested, Control, cmds


class Menu(Nested):
    CMD = cmds.menu
    _ATTRIBS = ['allowOptionBoxes', 'deleteAllItems', 'defineTemplate', 'docTag', 'enable', 'enableBackground',
                'exists', 'familyImage', 'helpMenu', 'label', 'mnemonic', 'parent', 'useTemplate', 'visible',
                'postMenuCommandOnce']
    _CALLBACKS = ['postMenuCommand']
    _READ_ONLY = ['numberOfItems']

    @classmethod
    def from_existing(cls, widget):
        key = widget.split("|")[-1]
        result = super(Menu, cls).from_existing(key, widget)
        return result

    @property
    def itemArray(self):
        return [MenuItem.wrap(self.fullPathName + '|' + item) for item in self.CMD(self.widget, itemArray=True, q=True) or []]


class MenuItem(Control):
    CMD = cmds.menuItem
    _ATTRIBS = ["altModifier", "annotation", "allowOptionBoxes", "boldFont", "checkBox", "collection",
                "commandModifier", "ctrlModifier", "divider", "data", "defineTemplate", "docTag", "echoCommand",
                "enableCommandRepeat", "enable", "exists", "familyImage", "image", "insertAfter", "imageOverlayLabel",
                "italicized", "keyEquivalent", "label", "mnemonic", "optionBox", "optionBoxIcon", "optionModifier",
                "parent", "radioButton", "radialPosition", "shiftModifier", "subMenu", "sourceType", "tearOff",
                "useTemplate", "version", 'postMenuCommandOnce']
    _READ_ONLY = ['isCheckBox', 'isOptionBox', 'isRadioButton']
    _CALLBACKS = ['command', 'dragDoubleClickCommand', 'dragMenuCommand', 'postMenuCommand']


class OptionMenu(Nested):
    CMD = cmds.optionMenu
    _ATTRIBS = ['alwaysCallChangeCommand', 'annotation', 'backgroundColor', 'docTag', 'enableBackground', 'exists',
                'height', 'label', 'manage', 'parent', 'preventOverride', 'select', 'value', 'visible', 'width']
    _READ_ONLY = ['fullPathName', 'itemListLong', 'itemListShort', 'isObscured', 'numberOfItems', 'numberOfPopupMenus',
                  'popupMenuArray']
    _CALLBACKS = ['changeCommand', 'dragCallback', 'dropCallback', 'visibleChangeCommand']
    _BIND_SRC = 'value'
    _BIND_TGT = 'items'
    _BIND_TRIGGER = 'changeCommand'

    @property
    def items(self):
        return [i.tag for i in self.controls]

    @items.setter
    def items(self, value):
        selected = self.select
        self.clear()
        self.controls[:] = [MenuItem(val, parent=self, tag=val) for val in value]
        if selected:
            self.select = selected

    def clear(self):
        for long_name in self.itemListLong or []:
            cmds.deleteUI(long_name)


class ActiveOptionMenu(OptionMenu):
    """
    A variant of the default OptionMenu which will call the command attached to
    the menuItem.  This allows for dropdown menus  which behave like regular
    menus rather than like pure dropdown selectors

    """

    def __init__(self, key=None, *args, **kwargs):
        super(ActiveOptionMenu, self).__init__(key, *args, **kwargs)
        self.changeCommand += self.fire_menu_callback

    def fire_menu_callback(self, *args, **kwargs):
        """
        this ensures that the command attached to the selected MenuItem is fired when that menu is selected
        """
        selected = self.controls[self.select - 1]
        selected.command()


class PopupMenu(Nested):
    CMD = cmds.popupMenu
    _ATTRIBS = ['altModifier', 'allowOptionBoxes', 'button', 'ctrlModifier', 'deleteAllItems', 'defineTemplate',
                'exists', 'markingMenu', 'parent', 'shiftModifier', 'useTemplate', 'visible', 'postMenuCommandOnce']
    _CALLBACKS = ['postMenuCommand']
    _READ_ONLY = ['numberOfItems']

    @property
    def itemArray(self):
        return [MenuItem.wrap(self.fullPathName + '|' + item) for item in self.CMD(self.widget, itemArray=True, q=True) or []]

    def _preserve_callbacks(self, query_cmd=None):
        # popupMenu doesn't let you query the postMenuCommand flag, you have to use menu instead.
        super(PopupMenu, self)._preserve_callbacks(cmds.menu)
