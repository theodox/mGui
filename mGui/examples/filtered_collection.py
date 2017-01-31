__author__ = 'stevet'
import re
import time
import inspect

from maya import cmds

from mGui import gui, forms, lists
from mGui.bindings import bind
from mGui.observable import ViewCollection
from mGui.qt.QTextField import QTextField
from mGui.scriptJobs import Idle

"""
This example illustrates the optional QTextField object, which (unlike a regular Maya text field)
will fire events on every key pres.

This example DOES NOT WORK in Maya 2017 or later due to the QT5 update.
"""

_items = gui.__all__ + forms.__all__ + lists.__all__

items = ViewCollection(*_items)


class InputBuffer(object):

    '''
    accumulate inputs until a certain amount of time passes
    '''

    def __init__(self, parent, fn, interval=1):
        self.last = time.time()
        self.interval = interval
        self.fn = fn
        self.buffer = []
        self.accumulate = inspect.getargspec(fn).varargs
        self.idleEvent = Idle()
        self.idleEvent += self.update
        self.idleEvent.start(p=parent)

    def handle(self, input, *_, **__):
        self.buffer.append(input)

    def update(self, *_, **__):
        if time.time() - self.last < self.interval:
            return
        if self.buffer:
            if self.accumulate:
                self.fn(*self.buffer)
            else:
                self.fn(self.buffer[-1])
            self.buffer = []
        self.last = time.time()


def main():
    def create_filter(fn):
        regex = re.compile(fn, re.I)
        test = lambda p: regex.search(p)
        items.update_filter(test)

    with gui.Window() as w:
        with forms.NavForm() as nav:
            with forms.VerticalForm() as navbar:
                one = gui.Button()
                two = gui.Button()
                three = gui.Button()
            with forms.HeaderForm() as main:
                filter_field = QTextField()
                main_list = lists.VerticalList()

        items > bind() > main_list.collection
        items.bind.viewCount > bind() > three.bind.label
        items.bind.count > bind() > two.bind.label
        w.update_bindings()

    w.buffer = InputBuffer(w, create_filter)
    filter_field.textChanged += w.buffer.handle
    cmds.scriptJob(lj=True)
    return w


if __name__ == '__main__':
    win = main()
    win.show()
