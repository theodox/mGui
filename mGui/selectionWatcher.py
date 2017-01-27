'''
Defines scriptJob based classes which allow binding to conditions or selection state
'''

from mGui.scriptJobs import SelectionChanged, SomethingSelected, ScriptJobC
from mGui.bindings import BindableObject
from mGui.core import Layout, Window
import maya.cmds as cmds


def _get_active_ui(fallback):
    result = dict()
    parent = fallback or Layout.current() or Window.current()
    if parent:
        result['parent'] = parent
    return result


class ConditionWatcher(BindableObject):
    """
    A BindableObject which exposes the state of a Maya condition.  You can use any condition defined in
    mGui.scriptJobs and bind to a boolean value which will update when that condition changes. For example:

        with Window(None,title='xxx') as z:
            sw = ConditionWatcher(RedoAvailable(None))
            with ColumnLayout('zzz', 'zzz') as col:
                this_button = Button('b', 'Button')
                this_button.bind.label < bind(str) < sw

        z.show()

    creates a window with a button labeld 'True' when redo is available and 'false' when it is not.

    In most cases, you'll want to pass in a ScriptJobC created with the "None" argument so that it fires on all
    changes, but you can pass in True to fire only when the condition changes to True, or False for changes to False.
    """
    _BIND_SRC = 'state'

    def __init__(self, condition, parent=None):
        """
        constructor.

        :param parent:  condition:  a class derived from mGui.scriptJobs.scriptJobC, such as 'RedoAvailable' or
        'PlayingBack'.
        :param parent:  a UI element name. The selection monitoring script job will be attached to that element and
        automatically stopped when that element is deleted

        """
        assert isinstance(condition, ScriptJobC), "condition must be an mGui.scriptJobs.ScriptJobC class"
        self.condition_changed = condition
        self.condition_changed += self._forward_update

        self.condition_changed.start(**_get_active_ui(parent))
        self._forward_update()

    def _forward_update(self, *args, **kwargs):
        self.update_bindings()

    @property
    def state(self):
        return self.condition_changed.get_state() == 1


class SelectionWatcher(ConditionWatcher):
    """
    A BindableObject which updates to reflect whether or not anything is selected in the scene.

        with Window(None,title='xxx') as z:
            sw = SelectionWatcher()
            with ColumnLayout('zzz', 'zzz') as col:
                this_button = Button('b', 'Button')
                this_button.bind.enable < bind() < sw

    creates a window with a button that will be enabled only when something is selected.

    By default the SelectionWatcher will parented to the currently active layout and it's associated scriptJob will
    be deleted when the UI is deleted. You can pass an explicit UI parent to the constructor if you want to attach to
    a different UI object ( mGui objects or maya strings both work).

    The watcher has one bindable property:

    - is_selected: a boolean value, true if anything is selected

    If you need to bind to the actual selection list, you should use a SelectionListWatcher instead
    """
    _BIND_SRC = 'is_selected'

    def __init__(self, parent=None):
        """
        constructor.

        :param parent:  a UI element name. The selection monitoring script job will be attached to that element and
        automatically stopped when that element is deleted
        :param itemTypes: an option list of string node type names
        """
        super(SelectionWatcher, self).__init__(SomethingSelected(None), parent)

    @property
    def is_selected(self):
        return self.state


class SelectionListWatcher(BindableObject):
    """
    A BindableObject which can be attached to a piece of UI and will update the maya selection list automatically
    using a script job.  For examnple:

        with Window(None,title='xxx') as z:
            sw = SelectionListWatcher()
            with ColumnLayout(None, 'zzz') as col:
                this_button = Button('b', 'Button')
                this_button.bind.label < bind(str) < sw

    creates a window with a button whose name will be updated to reflect the currently active selection (the default
    bind target of the SelectionListWatcher is the selected_items property).

    The watcher has two properties:

    - selected_items: a boolean value, true if anything is selected
    - is_selected: a list of all currently selected items (or an empty list)

    By default the SelectionListWatcher will update for all selection changes. You can, however, filter the list by
    providing a list of node type strings, in which case the select

    By default the SelectionListWatcher will parented to the currently active layout and it's associated scriptJob will
    be deleted when the UI is deleted. You can pass an explicit UI parent to the constructor if you want to attach to
    a different UI object ( mGui objects or maya strings both work).


    """
    _BIND_SRC = 'selected_items'

    def __init__(self, parent=None, types=None):
        """
        constructor.

        :param parent:  a UI element name. The selection monitoring script job will be attached to that element and
        automatically stopped when that element is deleted
        :param types: an optional collection of string node type names


        """

        self.selection_changed = SelectionChanged()
        self.selection_changed += self._forward_update
        self.filter = types
        self.selection_changed.start(**_get_active_ui(parent))
        self._forward_update()

    def _forward_update(self, *args, **kwargs):
        self.update_bindings()

    @property
    def selected_items(self):
        if self.filter:
            return cmds.ls(sl=True, l=True, type=self.filter) or []
        else:
            return cmds.ls(sl=True, l=True) or []

    @property
    def is_selected(self):
        return any(self.selected_items)

    @property
    def selection_size(self):
        return len(self.selected_items)

    @property
    def hilited(self):
        if self.filter:
            return cmds.ls(hl=True, l=True, type=self.filter) or []
        else:
            return cmds.ls(hl=True, l=True) or []

    @property
    def is_hilited(self):
        return any(self.hilited)
