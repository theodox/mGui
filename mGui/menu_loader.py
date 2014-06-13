"""
mGui.menuLoader

Allows loading of menus defined in YAML text files

@note: Depends on the availability of the yaml module (http://pyyaml.org/)
"""

import mGui.gui as gui
import yaml
import copy
import importlib
import maya.mel
import inspect


# empty command for unbound item
def nullop(*args, **kwargs):
    pass


class CallbackProxy(object):
    """
    Wrap an arbitrary function call so that it can be used as a menu item callback.

    Callbacks are stored in the KEEPALIVE folder so that they don't expire or generate
    DeadReference errors
    """
    KEEPALIVE = []

    def __init__(self, func, caller):
        self.func = func
        self.caller = caller
        self.argspec = inspect.getargspec(func)
        self.KEEPALIVE.append(self)

    def __call__(self, *args, **kwargs):
        no_kw = self.argspec.keywords is None
        no_args = self.argspec.varargs is None
        if no_args:
            if no_kw:
                self.func()
            else:
                self.func(**kwargs)
        else:
            if no_kw:
                self.func(*args)
            else:
                self.func(*args, **kwargs)


class MenuProxy(yaml.YAMLObject):
    yaml_tag = '!MMenu'

    def __new__(cls):
        res = yaml.YAMLObject.__new__(cls)
        setattr(res, 'key', 'Menu_Proxy')
        setattr(res, 'label', '')
        setattr(res, 'items', [])
        setattr(res, 'options', {})
        return res


    def instantiate(self, parent=None):
        opts = copy.copy(self.options)
        opts['parent'] = parent
        opts['label'] = self.label or self.key.replace('_', ' ')

        with gui.Menu(self.key, **opts) as result:
            for item in self.items:
                item.instantiate()
        return result


class MenuItemProxy(MenuProxy):
    yaml_tag = "!MMenuItem"


    def instantiate(self):
        opts = copy.copy(self.options)
        opts['label'] = self.label or self.key.replace('_', ' ')

        module, _, cmd = self.command.rpartition(".")
        imports = []
        segments = module.split(".")
        while segments:
            imports.append(".".join(segments))
            segments.pop()

        imports.reverse()
        mod = None
        for seg in imports:
            mod = importlib.import_module(seg)


        command = dict(inspect.getmembers(mod))[cmd]

        new_item = gui.MenuItem(self.key, **opts)
        cp = CallbackProxy(command, new_item)
        new_item.command += cp




def load_menu(menu_string):
    _main_menu = maya.mel.eval("string $f = $gMainWindow")
    menu_root = yaml.load(menu_string)
    return menu_root.instantiate(_main_menu)
