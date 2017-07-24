import maya.cmds as cmds

import os
from mGui.menu_loader import load_menu

"""
This examples shows how you can use the mGui.menu_loader module to load a menu from a YAML text file.  The sample data
is included as menu_loader_example.yaml.  It also illustrates some of the features supported in mGui menus.
"""


def load():
    this_dir = os.path.dirname(__file__)
    with open(os.path.join(this_dir, "menu_loader_example.yaml"), 'rt') as handle:
        yaml = handle.read()
        load_menu(yaml)


def about(*_, **__):
    print cmds.confirmDialog(title='mGui', message="This is function was loaded from a yaml file", button="Wow!")


def regular(*_, **__):
    print cmds.confirmDialog(title='mGui', message="Menus commands can be loaded as fully qualified path names, "
                                                   "like <b>mGui.examples.menu_loader.regular</b>", button="Cool!")


def checkbox(*_, **kwargs):
    cmds.warning("checkbox menu is  %i" % int(kwargs['sender'].checkBox))


if __name__ == '__main__':
    load()