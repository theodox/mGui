
import weakref

from .controls import IntField, IconTextButton, Button
from ..forms import HorizontalStretchForm, VerticalStretchForm
from ..events import MayaEvent

class IntSpinner(IntField):
    
    def __init__(self, key=None, **kwargs):
        self._step = kwargs.pop('step', 1)
        height = kwargs.pop('height', kwargs.pop('h', 32))
        width = kwargs.pop('width', kwargs.pop('w', 256))
        with HorizontalStretchForm(key='IntSpinner#', height=height, width=width) as self._root:
            super(IntSpinner, self).__init__(key, height=height, width=width - height, **kwargs)
            with VerticalStretchForm():
                self._up = Button(height=height / 2, width=height, label='^') #, style='iconOnly') #, image='caret-top')
                self._down = Button(height=height / 2, width=height, label='v') #, style='iconOnly') #, image='caret-bottom')

        self._up.command += self._inc
        self._down.command += self._dec
        print(self.height, self.width)
    

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
