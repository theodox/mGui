import maya.cmds as cmds

import os
from mGui.menu_loader import load_menu


def load():
    this_dir = os.path.dirname(__file__)
    with open(os.path.join(this_dir, "MenuLoader.YAML"), 'rt') as handle:
        yaml = handle.read()
        load_menu(yaml)


def about(*_, **__):
    print cmds.confirmDialog(title='mGui', message="This is function was loaded from a yaml file", button="Wow!")


def regular(*_, **__):
    print cmds.confirmDialog(title='mGui', message="Menus commands can be loaded as fully qualified path names, "
                                                   "like <b>mGui.examples.menu_loader.regular</b>", button="Cool!")


def checkbox(*_, **kwargs):
    cmds.warning("checkbox menu is  %i" % int(kwargs['sender'].checkBox))
