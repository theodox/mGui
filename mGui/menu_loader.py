"""
mGui.menuLoader

Allows loading of menus defined in YAML text files

@note: Depends on the availability of the yaml module (http://pyyaml.org/)

For an example of the Yaml formatting, see mgui.examples.menu_loader
"""

import sys

import maya.cmds
import maya.mel
import yaml

import copy
import inspect
import mGui.gui as gui
import traceback


# empty command for unbound item
def nullop(*args, **kwargs):
    pass


def get_insert_after_item(parent, match_label):
    """
    utility for finding an existing menu by label
    """
    result = None

    main_menu = gui.wrap(parent)
    for item in main_menu.controls:
        label_item = maya.cmds.menuItem(item, q=True, l=True)
        if match_label == label_item:
            result = item
            break

    return result


def load_menu(menu_string, parent=None):
    """
    given a string containing a YAML menu specification, load the menu and attach it to the supplied menu (where the
    menu is a maya UI widget string).

    If no parent is supplied, attach the menu to the main maya window
    """
    if not parent:
        parent = maya.mel.eval("string $f = $gMainWindow")
    menu_root = yaml.load(menu_string)
    return menu_root.instantiate(parent)


class CallbackProxy(object):
    """
    Wrap an arbitrary function call so that it can be used as a menu item callback.

    Callbacks are stored in the KEEPALIVE class field so that they don't expire or generate
    DeadReference errors
    """
    KEEPALIVE = []

    def __init__(self, func, caller):
        self.func = func
        self.caller = caller
        self.argspec = inspect.getargspec(func)
        self.KEEPALIVE.append(self)
        self.__name__ = func.__name__

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
    """
    This class is created from a YAML entry, like:

         !MMenu
            key: menu_key
            label: Menu Label

    the key is mandatory (unlike most mGui usage).  The label is the visible text of the menu . All other options are
    supplied using the key 'options'; they use the same flags as mGui.menus.Menu or cmds.menu.

    The items attached to the menu are declared in a field called items:

        !MMenu
        key:   mGuiExampleMenu
        label: mGui Example Menu
        options:
            tearOff: True
        items:


            - !MMenuItem
                key:  about
                label:  About this menu...
                annotation: Show the about dialog for this menu
                command: mGui.examples.menu_loader.about

            - !MMenuItem
                key:  sep
                options:
                  divider: True
                  dividerLabel: Supported options

            - !MMenuItem
                key:  regular
                label:  Regular menus
                annotation: A regular menu
                command: mGui.examples.menu_loader.regular

    for a complete example see mGui.examples.menu_loader.
    """
    yaml_tag = '!MMenu'

    def __new__(cls):
        res = yaml.YAMLObject.__new__(cls)
        setattr(res, 'key', 'Menu_Proxy')
        setattr(res, 'label', '')
        setattr(res, 'items', [])
        setattr(res, 'after', None)
        setattr(res, 'options', {})
        setattr(res, 'preMenuCommand', None)
        setattr(res, 'postMenuCommand', '')
        return res

    def instantiate(self, parent=None):
        opts = copy.copy(self.options)
        opts['parent'] = parent
        opts['label'] = self.label or self.key.replace('_', ' ')
        if self.postMenuCommand:
            opts['postMenuCommand'] = self.postMenuCommand

        with gui.Menu(self.key, **opts) as result:
            for item in self.items:
                item.instantiate()

        preMenuCommand = self.preMenuCommand or None
        if preMenuCommand:
            exec preMenuCommand

        return result


class EditMenuProxy(yaml.YAMLObject):
    """
    An EditMenu wraps an existing menu, such as one of the built in menus, allowing you to add new items to a menu
    you did not create.  The key value will need to be correct for mGui to match the existing menu.

    Example usage:

        !MEditMenu
            key:   mainEditMeshMenu
            label: Edit Mesh
            preMenuCommand:     import maya.mel; maya.mel.eval('PolygonsBuildMenu("mainEditMeshMenu")')

            items:

                - !MMenuItem
                    key: sep
                    options:
                      divider: True
                      dividerLabel: mGui

                - !MMenuItem
                    key: example
                    label: Added by mGui
                    annotation: this item was added by mGui

    here the preMenuCommand is included (it's the one from the main Maya UI loading code) to make sure that the menu is
    properly built -- many built in Maya menus are only created the first time a user clicks on them so the
    preMenuCommand can force them to instantiate before you edit them
    """

    yaml_tag = '!MEditMenu'

    def __new__(cls):
        res = yaml.YAMLObject.__new__(cls)
        setattr(res, 'key', 'Menu_Proxy')
        setattr(res, 'label', '')
        setattr(res, 'items', [])
        setattr(res, 'options', {})
        setattr(res, 'preMenuCommand', None)
        setattr(res, 'postMenuCommand', '')
        return res

    def instantiate(self, parent=None):
        opts = copy.copy(self.options)
        opts['parent'] = parent
        opts['label'] = self.label or self.key.replace('_', ' ')
        if self.postMenuCommand:
            opts['postMenuCommand'] = self.postMenuCommand

        preMenuCommand = self.preMenuCommand or None
        if preMenuCommand:
            exec preMenuCommand

        for item in self.items:
            item.instantiate(parent=self.key)

        return gui.wrap(self.key)


class MenuItemProxy(MenuProxy):
    """
    This class proxies an individual menu item. The flags are the same as those for `cmds.menuItem` or
    mGui.menus.MenuItem, and are passed using the 'options' key.  For  example:

        - !MMenuItem
            key:  check
            label:  checkboxes
            annotation: Toggle me!
            options:
              checkBox: True

    creates a checkbox item, and

        - !MMenuItem
            key:  sep
            options:
              divider: True
              dividerLabel: Supported options

    creates a labeled divider.

    To attach a callback, use the 'command' key.  The value for the key is a the fully qualified name
    of a function to be called when the menui selected.  For example:

        - !MMenuItem
            key:  about
            label:  About this menu...
            annotation: Show the about dialog for this menu
            command: mGui.examples.menu_loader.about

    this will load the function `mGui.examples.menu_loader.about` -- assuming that the module mGui.examples.menu_loader
    is available on the python path -- and attach it to this menu item as a callback
    """
    yaml_tag = "!MMenuItem"

    def instantiate(self, parent=None):
        try:
            opts = copy.copy(self.options)
            opts['label'] = self.label or self.key.replace('_', ' ')
            after = self.after
            if after:
                insertAfter = get_insert_after_item(parent, after)
                if insertAfter:
                    opts['insertAfter'] = insertAfter

            if parent:
                maya.cmds.setParent(parent, menu=True)
            new_item = gui.MenuItem(self.key, **opts)

            if hasattr(self, 'command') and self.command:
                module, _, cmd = self.command.rpartition(".")
                imports = []
                segments = module.split(".")
                while segments:
                    imports.append(".".join(segments))
                    segments.pop()

                imports.reverse()
                mod = None
                for seg in imports:
                    mod = import_module(seg, mod)

                command = dict(inspect.getmembers(mod))[cmd]

                cp = CallbackProxy(command, new_item)
                new_item.command += cp

            return new_item

        except:
            # Any exception in the menu creation process shows a confirm dialog with a stack trace. This is intended
            # to make it harder to accidentally ship a pre-configured menu that looks right but does not work.
            maya.cmds.confirmDialog(message=traceback.format_exc())


class RadioMenuItemProxy(MenuItemProxy):
    """
    This represents a radio menu item.  Radio menus requuire a RadioMenuCollectionProxy to coordinate their state.
    It uses the same syntax as a MenuItemProxy


    """
    yaml_tag = "!MRadioMenuItem"

    def instantiate(self, parent=None):
        self.options['radioButton'] = False
        new_menu = super(RadioMenuItemProxy, self).instantiate(parent)
        return new_menu


class RadioMenuCollectionProxy(yaml.YAMLObject):
    """
    Repesents a RadioMenuItemCollection.  The Radio items in the collection should be added in the 'items' key:

        - !MRadioCollection
                key: radio

                items:
                    - !MRadioMenuItem
                      key: fm
                      label: FM

                    - !MRadioMenuItem
                      key: am
                      label: AM

                    - !MRadioMenuItem
                      key: pm
                      label: CB

    Note that unlike regular radio collections the underlying radioMenuItemCollection objects cannot be queried (
    thanks, Maya!) so you'll have to manage the state yourself.  RadioMenuItemCollection objects do not have change
    callbacks.
    """
    yaml_tag = "!MRadioCollection"

    def __new__(cls):
        res = yaml.YAMLObject.__new__(cls)
        setattr(res, 'items', [])
        setattr(res, 'options', {})
        return res

    def instantiate(self, parent=None):
        opts = copy.copy(self.options)
        radioCollection = gui.RadioMenuItemCollection(**opts)
        for item in self.items:
            item.instantiate()

        radioCollection.CMD()
        return radioCollection


class SubMenuProxy(MenuItemProxy):
    """
    Represents a menu item with submenus -- equivalent to `cmds.menuItem(subMenu=True)

    The submenu items should ba added in the 'items' key:

         - !MSubMenu
                key: submenu
                label: submenus

                items:
                    - !MMenuItem
                      key: sub1
                      label: Item 1

                    - !MMenuItem
                      key: sub2
                      label: Item 2

    """
    yaml_tag = "!MSubMenu"

    def instantiate(self, parent=None):
        self.options['subMenu'] = True

        # we _dont_ use gui.SubMenu because we're just creating the widget here
        new_menu = super(SubMenuProxy, self).instantiate(parent)

        # now we wrap it in a gui.Submeny
        new_menu = gui.SubMenu.wrap(new_menu.widget)
        for item in self.items:
            kid = item.instantiate(parent=new_menu)
            new_menu.add(kid)

        menu_parent = new_menu.widget.rpartition("|")[0]
        maya.cmds.setParent(menu_parent, menu=True)

        return new_menu


"""
Below is a cut-and-paste of the 2.7 importlib module, included so that mGui can work in 2.6 and 2.7.  Luckily it is
pure python so it 'just works' when cut-and-pasted, and it should cover forseeable Mayas unless/until they
switch to 3.0

If you know who to credit for this, let me know. I assume the original is (c) the Python Software foundation
and licensed under the PSF License (https://wiki.python.org/moin/PythonSoftwareFoundationLicenseFaq).
"""


def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                             "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


'''
end python foundation code
'''
