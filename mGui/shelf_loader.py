"""
mGui.shelf_loader

Allows loading of shelves defined in python dictionaries.

"""
import os
from maya import cmds
from mGui import gui


def _process_command(cmd):
    return cmd if isinstance(cmd, basestring) else '\n'.join(cmd)


class BaseLoader(object):

    def __init__(self, data_dict):
        self.__dict__.update(data_dict)


class ShelfLayoutProxy(BaseLoader):
    proxy = gui.ShelfLayout

    # Shelf Defaults
    parent = 'ShelfLayout'
    key = 'ShelfProxy'
    controls = tuple()

    def __init__(self, data_dict):
        super(ShelfLayoutProxy, self).__init__(data_dict)
        self.controls = [ShelfButtonProxy(ctrl) for ctrl in self.controls]

    def instantiate(self, parent=None):
        if parent is None:
            parent = gui.wrap(self.parent)

        # initializes all the shelves
        current_tab = parent.selectTab
        for child in parent.childArray:
            parent.selectTab = child

        parent.selectTab = current_tab

        for shelf in parent.controls:
            if shelf.key == self.key:
                break
        else:
            with parent.as_parent():
                shelf = self.proxy(self.key)
                # Needed so that we don't throw a weird maya error until the next restart.
                # Pulled this from the shelf editor mel script.
                cmds.optionVar(stringValue=('shelfName{}'.format(parent.numberOfChildren), self.key))
                cmds.optionVar(intValue=('shelfLoad{}'.format(parent.numberOfChildren), True))
                cmds.optionVar(stringValue=('shelfFile{}'.format(parent.numberOfChildren), ''))

        for ctrl in self.controls:
            ctrl.instantiate(shelf)

        cmds.saveAllShelves(parent)



class ShelfButtonProxy(BaseLoader):
    proxy = gui.ShelfButton

    # Button Defaults
    key = 'ShelfButtonProxy'
    annotation = ''
    docTag = ''
    image = 'commandButton.png'
    imageOverlayLabel = ''
    overlayLabelColor = (0.8, 0.8, 0.8)
    enableBackground = False
    overlayLabelBackColor = (0, 0, 0, 0.5)
    label = ''
    sourceType = 'python'
    command = ''
    doubleClickCommand = ''
    menuItems = tuple()
    font = 'plainLabelFont'

    def __init__(self, data_dict):
        super(ShelfButtonProxy, self).__init__(data_dict)
        self.menuItems = [MenuItemProxy(item) for item in self.menuItems]

    def instantiate(self, parent=None):
        if not parent.controls:
            parent.controls[:] = [self.proxy.wrap(child) for child in parent.childArray]
        for ctrl in parent.controls:
            # docTag actually gets serialized, and doesn't have a practical use
            # which makes it perfect for a sentinel
            if ctrl.docTag == (self.docTag or self.key):
                break
        else:
            with parent.as_parent():
                ctrl = self.proxy(self.key)

        ctrl.annotation = self.annotation
        ctrl.docTag = (self.docTag or self.key)
        ctrl.image = os.path.expandvars(self.image)
        ctrl.label = self.label
        ctrl.sourceType = self.sourceType
        if self.command:
            ctrl.command = _process_command(self.command)
        ctrl.imageOverlayLabel = self.imageOverlayLabel
        ctrl.overlayLabelColor = self.overlayLabelColor
        ctrl.overlayLabelBackColor = self.overlayLabelBackColor
        ctrl.enableBackground = self.enableBackground
        if self.doubleClickCommand:
            ctrl.doubleClickCommand = _process_command(self.doubleClickCommand)
        ctrl.font = self.font

        for item in self.menuItems:
            item.instantiate(ctrl)


class MenuItemProxy(BaseLoader):
    proxy = gui.MenuItem

    # MenuItem Defaults
    key = 'MenuItemProxy'
    command = ''
    sourceType = ''

    def instantiate(self, parent=None):
        popup = gui.PopupMenu.wrap(parent.fullPathName + "|" + parent.popupMenuArray[0])
        for item in popup.itemArray:
            item = self.proxy.wrap(popup.fullPathName + "|" + item)
            # widget gets recreated by Maya, but the key is used as the label.
            if item.label == self.key:
                break
        else:
            with popup.as_parent():
                item = self.proxy(self.key)

        item.sourceType = self.sourceType
        if self.command:
            item.command = _process_command(self.command)


def load_shelf(shelf_dict):
    shelf = ShelfLayoutProxy(shelf_dict)
    shelf.instantiate()
