import sys
import maya.cmds as cmds
from mGui.core import Control
import maya.mel as mel


class UserCancelledProgress(RuntimeError):
    pass


class ProgressBar(Control):
    """
    mGui style wrapper for ProgressBar

    Use start() and end() to avoid the cumbersome (cmds.progressBar('xxx', e=True, beginProgress = True) form.

    Use iter() to wrap an operation in a progress bar:

        with Window("window") as w:
            with ColumnLayout("c") as col:
                progbar = ProgressBar("pb")

        w.show()

        for item in progbar.iter(range(0,100)):
            print item
    """
    CMD = cmds.progressBar

    _ATTRIBS = ['annotation', 'backgroundColor', 'beginProgress', 'defineTemplate', 'docTag', 'enable',
                'enableBackground', 'endProgress', 'exists', 'fullPathName', 'height', 'isCancelled',
                'isInterruptable', 'isObscured', 'manage', 'maxValue', 'minValue',
                'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'progress', 'status',
                'step', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']

    _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']
    _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus', 'isMainProgressBar']

    def start(self):
        """
        start progress bar
        """
        self.beginProgress = 1

    def end(self):
        """
        Stop and reset the progress bar
        """
        self.endProgress = 1

    def update(self, increment=1):
        """
        increment the progress bar by <increment>
        """
        self.step = increment

    def iter(self, generator, increment=1, close=True):
        """
        Start the progress bar. Loop over every item in <generator>
        and update increment the progress bar.  Each item in the generator
        is yielded up after the progress bar updates.

        If close is True, reset the progress bar by calling end() after the generator
        is exhausted.
        """
        should_close = close
        try:
            self.start()
            for item in generator:
                self.update(increment)
                yield item
        except:
            should_close = True
            raise

        finally:
            if should_close:
                self.end()


class MainProgressBar(ProgressBar):
    """
    A ProgressBar instance which wraps Maya's main progres bar ('$gMainProgressBar' in mel)

    start, end, and update can optionally include status messages
    """

    def __init__(self):

        def fake_init(self, *_, **__):
            return mel.eval('$tmp = $gMainProgressBar')

        self.CMD = fake_init
        super(MainProgressBar, self).__init__()
        self.CMD = cmds.progressBar

    def start(self, status=None, interruptable=False):
        super(MainProgressBar, self).start()
        if status is not None:
            self.status = status
        self.isInterruptable = interruptable

    def end(self, status=None):
        super(MainProgressBar, self).end()
        if status is not None:
            self.status = status

    def update(self, increment=1, status=None):
        super(MainProgressBar, self).update(increment)
        if status is not None:
            self.status = status

    def iter(self, generator, increment=1, close=True, interruptable=False, handler=None):
        """
        iterate over <generator>, updating the progress bar for each item. The progress bar will show the string
        representation of each item in the status bar.  Each item is yielded up after the progress bar updates.

        If interruptable is True, the user can cancel using the escape key. This raises a UserCancelledProgress
        exception.  If a callable is supplied as  <handler>, that function will be called with no arguments
        when the user requests the cancellation.

        If 'close' is true, the progress bar wil clean itself up with end() when completed
=       """
        should_close = close
        self.start(interruptable=interruptable)
        try:
            for item in generator:
                if self.isCancelled:
                    if handler:
                        handler()
                    raise UserCancelledProgress('User requested cancellation')

                self.update(increment, str(item))
                yield item

            if should_close:
                self.end("complete")
        except UserCancelledProgress:
            self.end(status="user cancelled")
            self.isInterruptable = False
            raise

        except:
            self.end(status=str(sys.exc_info())[1])
            self.isInterruptable = False
            raise
