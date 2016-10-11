__author__ = 'stevet'
from mGui.gui import *
from mGui.forms import *
from mGui.lists import *
from mGui.bindings import *
from mGui.observable import ViewCollection
from mGui.qt.QTextField import QTextField
from mGui.scriptJobs import Idle
from ul_profile import do_cprofile
import time
import inspect
from functools import  partial


items = ViewCollection(*locals().keys())


class InputBuffer(object):
    '''
    accumulate inputs until a certain amount of time passes
    '''
    def __init__(self, parent, fn, interval = 1):
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
        if time.time() - self.last <  self.interval:
            return 
        if self.buffer:
            print 'fire'
            if self.accumulate:
                self.fn(*self.buffer)
            else:
                self.fn(self.buffer[-1])
            self.buffer = []
        self.last = time.time()





with Window() as w:
    with NavForm() as nav:
        with VerticalForm() as navbar :
            one = Button()
            two = Button()
            three = Button()
        with HeaderForm() as main:
            filter_field = QTextField()
            main_list = VerticalList()

    items > bind( ) > main_list.collection
    items.bind.viewCount > bind() > three.bind.label
    items.bind.count > bind() > two.bind.label
    w.update_bindings()
w.show()



import re
def create_filter (fn):
    regex = re.compile(fn, re.I)
    test = lambda p: regex.search(p)
    items.update_filter(test)


buffer = InputBuffer(w, create_filter)

filter_field.textChanged += buffer.handle


cmds.scriptJob(lj=True)