'''
Observable.py
@author: stevetheodore
'''
import events
from bindings import BindableObject



class ObservableCollection(BindableObject):
    _BIND_SRC = 'Items'
    _BIND_TGT = None
    
    def __init__(self, *items):
        self.Items = [i for i in items]
        self.CollectionChanged = events.Event(collection = self)
        self.ItemAdded = events.Event(collection = self)
        self.ItemRemoved = events.Event(collection = self)
        self.Reordered = events.Event(collection = self)
        
    def __iter__(self):
        for item in self.Items:
            yield item
    
    def add (self, *additions):
        _len = len(self.Items)
        for each_new  in additions:
            self.Items.append(each_new )
            self.ItemAdded(each_new, len(self.Items) - 1)
        self.update_bindings()
        
    def remove(self, *delenda):
        for item in delenda:
            found  = self.Items.index(item)
            if found:
                self.ItemRemoved(item, found)
            for item in delenda:
                self.Items.remove(item)
            if found: # if this > -1  something was deleted
                self.CollectionChanged()
                self.update_bindings()
                
    def clear(self):
        self.Items = []
        self.CollectionChanged()
        self.update_bindings()
                
        
    def sort (self, comp=None, key=None, reverse=False):
        self.Items.sort(comp, key, reverse)
        self.Reordered()
        self.update_bindings()
                
    
    @property        
    def Count(self):
        return len(self.Items)
        
class ViewCollection(ObservableCollection):
    '''
    An ObservableCollection with a filter (a predicate function like the ones
    used in a built-in python filter expression).  Changing the filter
    expression updates the 'View', which is the current filtered version of the
    underlying container.
    
    The class exposes the same events as ObservableCollection, as well as a
    ViewChanged event which triggers when the filter is chaanged
    '''
    _BIND_SRC = 'View'
    
    def __init__(self, *items):
        super(ViewCollection, self).__init__(*items)
        self.ViewChanged = events.Event(collection = self)

        self.Filter = lambda p: p
        self._last_count = 0
        
    @property 
    def View(self):
        '''
        Returns a tuple of all the items in this collection which pass the current filter
        '''
        return  tuple(* filter(self.Filter, self.Items))
    
    @property
    def ViewCount(self):
        return len(self.View)
                
    def update_filter(self, filter_fn):
        '''
        Change the filter expression. This will trigger a ViewChanged event
        '''
        if not filter_fn:
            self.Filter = lambda p: p
        else:
            self.Filter = filter
        
        self.ViewChanged()
        self.update_bindings()
        
        
        
class Fred (BindableObject):
    def __init__(self):
        self.Values = []
        

    def refresh(self, *arg, **kwargs):
        self.update_bindings()
        

          
        
testdata = [1,2,3,4,5,6,7]
test = ViewCollection (*testdata)


global fred    
fred = Fred()
fred + 'Values' << test + 'View'
print fred.bindings
#@events.EventHandler
def updated(*args, **kwargs):
    global  fred
    print "view:",  fred.Values
    
print test.View

#test.ViewChanged += fred.refresh
#test.ViewChanged += updated

test.update_filter( lambda x: x % 2 == 0) 
print fred.Values
test.add(88)
print fred.Values
test.update_filter( lambda x: x % 3 == 1) 
print fred.Values
test.update_filter( lambda x: x % 4 == 1) 
print fred.Values
test.update_filter( lambda x: x % 5 == 1) 
print fred.Values
print test.CollectionChanged._Handlers

