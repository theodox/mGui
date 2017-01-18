import os
import yaml
from maya import cmds
from mGui import gui

class ShelfLayoutProxy(yaml.YAMLObject):
    yaml_tag = '!MShelfLayout'
    proxy = gui.ShelfLayout

    # Shelf Defaults
    parent = 'ShelfLayout'
    key = 'ShelfProxy'
    controls = tuple()

    def instantiate(self, parent=None):
        if parent is None:
            parent = gui.derive(self.parent)

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

        for ctrl in self.controls:
            ctrl.instantiate(shelf)


class ShelfButtonProxy(yaml.YAMLObject):
    yaml_tag = '!MShelfButton'
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

    def instantiate(self, parent=None):
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
        ctrl.image = self.image
        ctrl.label = self.label
        ctrl.sourceType = self.sourceType
        ctrl.command = self.command
        ctrl.imageOverlayLabel = self.imageOverlayLabel
        ctrl.overlayLabelColor = self.overlayLabelColor
        ctrl.overlayLabelBackColor = self.overlayLabelBackColor
        ctrl.enableBackground = self.enableBackground
        ctrl.doubleClickCommand = self.doubleClickCommand
        ctrl.font = self.font

        for item in self.menuItems:
            item.instantiate(ctrl)


class MenuItemProxy(yaml.YAMLObject):
    yaml_tag = '!MMenuItem'
    proxy = gui.MenuItem

    # MenuItem Defaults
    key = 'MenuItemProxy'
    command = ''
    sourceType = ''

    def instantiate(self, parent=None):
        popup = parent.popupMenuArray[0]
        for item in popup.itemArray:
            # widget gets recreated by Maya, but the key is used as the label.
            if item.label == self.key:
                break
        else:
            with popup.as_parent():
                item = self.proxy(self.key)

        item.sourceType = self.sourceType
        item.command = self.command


def load_shelf(shelf_string):
    shelf = yaml.load(shelf_string)
    shelf.instantiate()


