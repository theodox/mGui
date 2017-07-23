
import weakref

from .controls import IntField, IconTextButton, Button, Text
from ..forms import HorizontalStretchForm, VerticalStretchForm
from ..events import MayaEvent


class CompoundControl(type):
    # Some magic will happen here?
    pass


class IntSpinner:
    __metaclass__ = CompoundControl

    _CONTROLS = {
        'root': HorizontalStretchForm,
        'field': IntField,
        'label': Text,
        'decrement': Button,
        'increment': Button,
        'form': VerticalStretchForm,
    }
    _HIERARCHY = {
        'root': (
            'label',
            'field', {
                'form': (
                    'increment',
                    'decrement'
                )
            }
        )
    }


class IntSpinner(object):

    def __init__(self, key=None, **kwargs):
        self._step = kwargs.pop('step', 1)
        value = kwargs.pop('value', 0)

        height = kwargs.pop('height', kwargs.pop('h', 32))
        width = kwargs.pop('width', kwargs.pop('w', 256))
        with HorizontalStretchForm(key='IntSpinner#', **kwargs) as self.root:
            self.field = IntField(height=height, width=width - height, value=value)
            with VerticalStretchForm() as self.form:
                self.increment = Button(height=height / 2, width=height, label='^')
                self.decrement = Button(height=height / 2, width=height, label='v')

        self.increment.command += self._inc
        self.decrement.command += self._dec

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value

    def _inc(self, *args, **kwargs):
        self.field.value += self._step

    def _dec(self, *args, **kwargs):
        self.field.value -= self._step

    def __getattr__(self, attr):
        if hasattr(self, 'root') and hasattr(self.root, attr):
            return getattr(self.root, attr)
        return super(IntSpinner, self).__getattribute__(attr)

    def __setattr__(self, attr, value):
        if hasattr(self, 'root') and hasattr(self.root, attr):
            setattr(self.root, attr, value)
        else:
            self.__dict__[attr] = value
