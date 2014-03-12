'''
Observable.py
@author: stevetheodore
'''
import events
from bindings import BindableObject



class ObservableCollection(BindableObject):
    _BIND_SRC = 'count'
    _BIND_TGT = None
    
    def __init__(self, *items):
        self.Items = [i for i in items]
        
    def __iter__(self):
        for item in self.Items:
            yield item
    
    def add (self, *additions):
        _len = len(self.Items)
        for each_new  in additions:
            self.Items.append(each_new )
            self.ItemAdded(each_new, len(self.Items) - 1)
        
    def remove(self, *delenda):
        for item in delenda:
            found  = self.Items.index(item)
            if found:
                self.ItemRemoved(item, found)
            for item in delenda:
                self.Items.remove(item)
            if found: # if this > -1  something was deleted
                self.CollectionChanged()
            
    def clear(self):
        self.Items = []
        self.CollectionChanged()
        
    def sort (self, cmp=None, key=None, reverse=False):
        self.Items.sort(cmp, key, reverse)
        self.Reordered()
        
    def count(self):
        return len(self.Items)
        
class FilteredColleciton(ObservableCollection):
    
    def __init__(self,  *items, filter = None)
        super(FilteredColleciton, self).__init__(*items)
        self.Filter = filter or lambda p : p
        
    