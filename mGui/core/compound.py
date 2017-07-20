
import weakref

from .controls import IntField, IconTextButton
from ..forms import HorizontalStretchForm, VerticalStretchForm
from ..events import MayaEvent

class IntSpinner(IntField):
    
    def __init__(self, key=None, **kwargs):
        self._step = kwargs.pop('step', 1)
        with HorizontalStretchForm(key='IntSpinner#') as self._root:
            super(IntSpinner, self).__init__(key, **kwargs)
            with VerticalStretchForm(width=24):
                self._up = IconTextButton(height=12, style='iconOnly', image='caret-top')
                self._down = IconTextButton(height=12, style='iconOnly', image='caret-bottom')

        self._up.command += self._inc
        self._down.command += self._dec
    

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value

    def _inc(self, *args, **kwargs):
        self.value += self._step

    def _dec(self, *args, **kwargs):
        self.value -= self._step
