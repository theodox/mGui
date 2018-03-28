from unittest import TestCase, main

from maya import cmds, standalone

standalone.initialize()


# Mocking out the various cmds and events needed to test this without a GUI

def _window(*args, **kwargs):
    if 'exists' in kwargs:
        return True
    return 'window1'

def _formLayout(*args, **kwargs):
    if 'exists' in kwargs:
        return True
    return 'window1|formLayout1'

def _button(*args, **kwargs):
    if 'exists' in kwargs:
        return True
    return 'window1|formLayout1|button1'

def _control(*args, **kwargs):
    if 'exists' in kwargs:
        return True


cmds.control = cmds.layout = _control
cmds.window = _window
cmds.formLayout = _formLayout
cmds.button = _button
cmds.setParent = lambda *args, **kwargs: None

from mGui import gui, forms, events
# Mocking this with an empty event because cmds.scriptJob is annoyingly complex
gui.Control.onDeleted = events.MayaEvent()


class TestNesting(TestCase):

    def setUp(self):
        with gui.Window() as win:
            with forms.VerticalForm() as vf:
                btn = gui.Button()
                btn2 = gui.Button()
                for i in xrange(3):
                    gui.Button()

        self._win = win
        self._vf = vf
        self._btn = btn
        self._btn2 = btn2

    def test_setattr(self):
        assert self._vf == self._win.vf
        assert self._btn == self._win.vf.btn
        assert self._btn2 == self._win.vf.btn2

    def test_container(self):
        assert self._vf in self._win
        assert self._btn in self._vf

    def test_clear(self):
        assert len(self._vf.controls) == 5
        self._vf.clear()
        assert len(self._vf.controls) == 0

        assert self._vf in self._win
        self._win.clear()
        assert self._vf not in self._win




if __name__ == '__main__':
    main()