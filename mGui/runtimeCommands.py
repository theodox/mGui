"""
runtimeCommands.py

Convenience methods for binding commands or callbacks to runtimeCommand objects.

"""

import maya.cmds as cmds

import mGui.events as events
import json
import inspect


def create_proxy_command(callable_object, *args, **kwargs):
    """
    generates an expression which imports a callable and executes it.

    Arguments may be passed through to the expression, but they must be built-in types (numbers, strings, etc)

    """

    info = ImportInfo(callable_object)

    comment = "# mGui callback for %s" % info.fully_qualified_name()
    import_line = info.import_statement()

    # gymnastics to format the arguments and keywords if they exist
    arg_string = json.dumps(args)[1:-1]
    k = list(map(str, list(kwargs.keys())))
    v = json.dumps(list(kwargs.values()))[1:-1].split(", ")
    kwarg_string = ",".join([kk + "=" + vv for kk, vv in zip(k, v)])
    arguments = "%s%s%s" % (
        arg_string,
        (", " if arg_string and kwarg_string else ""),
        kwarg_string,
    )
    fn = "%s(%s)\n" % (info.callable_name(), arguments)
    return "\n".join((comment, "", import_line, fn))


def create_runtime_command(name, callable_object, category="mGui", annotation="", args=(), kwargs=None):
    """
    creates a simple runTimeCommand which wraps the supplied function.  The function should be a no-argument callable
    which can be called using the pattern:

        from <module> import <fn>
        fn()

    For this reason, this is only appropriate for module-level functions.
    """
    kwargs = {} if kwargs is None else kwargs
    assert callable(callable_object), "function argument must be callable"

    if cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(name, edit=True, delete=True)

    cb_string = create_proxy_command(callable_object, *args, **kwargs)
    cmds.runTimeCommand(
        name,
        category=category,
        annotation=annotation,
        commandLanguage="python",
        command=cb_string,
    )
    return name


class RuntimeEvent(object):
    """
    Exposes a set of class methods for attaching mGui events to runTimeCommands.

    Typical usage:

        import mGui.runtimeCommands as rc
        def example(*args, **kwargs):
            print 'example:', args, kwargs

        rc.RuntimeEvent.create_command("sampleRuntimeCommand", example)

    This will create an event object in named 'sampleRuntimeCommand_event', add the example function to it as a
    handler, and make a new runTimeCommand which looks like:

        from mGui.runtimeCommands import fire_callback
        fire_callback("sampleRuntimeCommand_event")

    This runTimeCommand can be bound to a hotkey or invoked from MEL, which can make it useful for updating legacy gui
    code.

    @note: Don't instantiate this class, it's just a 'namespace' class with a set of related methods.
    """

    REGISTRY = {}

    @classmethod
    def create(cls, name):
        """
        Creates an mGui.events.Event object with the supplied name. If the named Event already exists, return it.
        :param name: string name of the new Event
        :return: mGui.events.Event object
        """
        if not name in cls.REGISTRY:
            cls.REGISTRY[name] = events.Event()
        return cls.REGISTRY[name]

    @classmethod
    def find(cls, name):
        """
        Return the named callback Event, if it exists.  If not, return None
        :param name: name of the Event object to return
        :return: the named Event object, or None if there is no object with that name
        """
        return cls.REGISTRY.get(name)

    @classmethod
    def add_handler(cls, name, handler):
        """
        Add the supplied callable object to the named event as a handler
        @see events.Event for how handlers work
        :param name: name of the Event object
        :param handler: callable handler function or class
        """
        cb = cls.find(name)
        cb += handler

    @classmethod
    def remove_handler(cls, name, handler):
        """
        Remove supplied callable object from the named event
        @see events.Event for how handlers work
        :param name: name of the Event object
        :param handler: callable handler function or class
        """
        cb = cls.find(name)
        cb -= handler

    @classmethod
    def create_command(cls, name, func, category="mGui", annotation=""):
        """
        Creates a new runtimeCommand (or replaces an existing one) which fires an mGui.event.Event when invoked.
        This allows you to bind multiple handlers to a single hotkey execution

        Note that the Event object will not automatically be recreated on maya startup. The recommended use
        is to invoke this command when Maya starts up and bind the hotkey to a new event; this will replace the
        existing runTimeCommand with a new identical one but also create and bind the runtime event.  Alternatively
        you could create a named event at startup time using RuntimeEvent.create().

        The HotkeyableEvent decorator is an easy way to make sure that the event is created and a handler
        assigned at startup

        :param name:        name of the new runtime command
        :param func:        (optional) callable function to be used as a handler for the new event
        :param category:    display category for the new runTimeCommand (defaults to 'mGui')
        :param annotation:  descriptive text for the new runTimeCommand
        :return: The event object for this command
        """
        new_event = cls.create(name + "_event")
        if func and callable(func):
            new_event += func

        create_runtime_command(name, fire_callback, category, annotation, args=(name + "_event",))
        return new_event


def fire_callback(name, *args, **kwargs):
    """
    Fire the runtimeEvent associated with <name>

    Print a warning if the event does not exist
    """
    rc = RuntimeEvent.find(name)
    if rc:
        rc(*args, **kwargs)
    else:
        cmds.warning("no RuntimeEvent named %s. Create one using RuntimeEvent.create" % name)


class Hotkeyable(object):
    """
    Decorator which calls create_runtime_command on the decorated function, allowing it to be used as a Maya
    RunTimeCommand. Since the decorated function will be called using create_runtime_command, it should be a
    module-level function which works with a simple absolute import (see create_runtime_command)

    Note the decorated function is returnd unchanged
    """

    def __init__(self, name, category="mGui", annotation=""):
        self._name = name
        self._category = category
        self._annotation = annotation

    def __call__(self, fn):
        create_runtime_command(self._name, fn, category=self._category, annotation=self._annotation)
        return fn


class HotkeyableEvent(object):
    """
    Decorator creates a RuntimeEvent for the decorated function and adds the function to the event as a handler.
    Since the function is an event handler it should use the standard mGui fn(*args, **kwargs) handler signature.

    Note the decorated function is returnd unchanged
    """

    def __init__(self, name, category="mGui", annotation=""):
        self._name = name
        self._category = category
        self._annotation = annotation

    def __call__(self, fn):
        RuntimeEvent.create_command(self._name, fn, category=self._category, annotation=self._annotation)
        return fn


class ImportInfo(object):
    """
    Utility class for formatting import statements from objects
    """

    def __init__(self, item):
        self.module = None
        if hasattr(item, "__module__"):
            self.module = item.__module__
        self.cls = None
        self.method = None

        if inspect.isfunction(item):
            self._format_function(item)
            return

        if inspect.ismethod(item):
            self._format_method(item)
            return

        if inspect.isclass(item):
            self._format_class(item)

    def _format_function(self, obj):
        self.cls = None
        self.method = obj.__name__

    def _format_method(self, obj):
        owner = dict(inspect.getmembers(obj))["__func__"]
        self.cls = owner.__name__
        self.method = obj.__name__

    def _format_class(self, obj):
        self.cls = obj.__name__
        self.method = None

    def fully_qualified_name(self):
        items = [i for i in [self.module, self.cls, self.method] if i]
        return ".".join(items)

    def import_statement(self):
        if self.cls:
            return "from %s import %s" % (self.module, self.cls)
        else:
            return "from %s import %s" % (self.module, self.method)

    def callable_name(self):
        if self.cls and self.method:
            return "%s.%s" % (self.cls, self.method)
        if self.cls:
            return self.cls
        if self.method:
            return self.method
        return ""
