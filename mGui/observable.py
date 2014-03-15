'''
Observable.py
@author: stevetheodore
'''
import events
from bindings import BindableObject


class ObservableCollection(BindableObject):
    '''
    Encapsulates a collection suitable for data binding. The contents are
    managed internally but visible to other classes as the Contents property
    
    The collection emits events when it is updated:
    
       * ItemAdded(item, collection = self) for each item added
       * ItemRemoved(item, collection = self) for each item removed
       * Reordered(collection = self) when the internal collection is sorted
       * CollectionChanged(collection = self) for all changes apart from reordering
    
    This collections outgoing data bindings will be updated automatically on
    these events as well, so it's not necessary to explicitly handle them
    although that can be done if you need more control over the changes.
    
    NOTE: it's a Bad Idea(tm) to mess directly with the internal collection. The
    bindable version of it a tuple (so it's immutable). The intended use is for
    display of a list, not list management!
    
    Inherits methods from BindableObject, so you can manually trigger an update with update_bindings
    '''
    _BIND_SRC = 'Contents'
    _BIND_TGT = None
    
    def __init__(self, *items):
        self._Internal_Collection = [i for i in items]
        self.CollectionChanged = events.Event(collection = self)
        self.ItemAdded = events.Event(collection = self)
        self.ItemRemoved = events.Event(collection = self)
        self.Reordered = events.Event(collection = self)

    @property
    def Contents(self):
        '''
        The contents of the collection.  Bindable.
        '''
        return tuple([i for i in self._Internal_Collection])
    
    @property
    def Count(self):
        '''
        The number of items in the collection. Bindable.
        '''
        return len(self._Internal_Collection)

            
    def add (self, *additions):
        '''
        Add items to the collection, with notifications.
        '''
        if len(additions):
            for each_new  in additions:
                self._Internal_Collection.append(each_new )
                self.ItemAdded(each_new, len(self._Internal_Collection) - 1)
            
            self.CollectionChanged()
            self.update_bindings()
            
    def insert (self, index, item): 
        '''
        Add <item> at position <index>
        '''   
        self._Internal_Collection.insert(index, item)    
        self.ItemAdded(item, index)
        self.CollectionChanged()
        self.update_bindings()
        
        
        
    def remove(self, *delenda):
        '''
        Removes items from the collection
        '''
        _found = False
        for item in delenda:
            found  = self._Internal_Collection.index(item)
            if found > -1:
                self.ItemRemoved(item, found)
                _found = True
        for item in delenda:
            self._Internal_Collection.remove(item)
        if _found: # if this > -1  something was deleted
            self.CollectionChanged()
            self.update_bindings()
            
    def clear(self):
        '''
        Clear the collection
        '''
        self._Internal_Collection = []
        self.CollectionChanged()
        self.update_bindings()
                
        
    def sort (self, comp=None, key=None, reverse=False):
        '''
        Sort the collection with the supplied comparison, key and reverse
        arguments (see list.sort)
        '''
        self._Internal_Collection.sort(comp, key, reverse)
        self.Reordered()
        self.update_bindings()
                

    def __iter__(self):
        '''
        iterates over the contents of the collection
        '''
        for item in self._Internal_Collection:
            yield item


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
        self._last_count = len(self._Internal_Collection)
        
    @property
    def View(self):
        '''
        Returns a tuple of all the items in this collection which pass the
        current filter. Bindable.
        '''
        t = tuple([i for i in self._Internal_Collection if self.Filter(i)])
        self._last_count = len(t)
        return t
    
    @property
    def ViewCount(self):
        '''
        The number of items currently passing the filter. Bindable
        '''
        return self._last_count
                
    def update_filter(self, filter_fn):
        '''
        Change the filter expression. This will trigger a ViewChanged event
        '''
        if not filter_fn:
            self.Filter = lambda p: p
        else:
            self.Filter = filter_fn
        
        self._last_count = len(self.View)
        self.ViewChanged()
        self.update_bindings()
        
        

        
class BoundCollection(BindableObject):
    _BIND_TGT = 'set_collection'
    
    def __init__(self, conversion = lambda x: x):
        self._Internal_Collection  = ()
        self._Public_Collecton = {}
        self.Conversion = conversion
        self.CollectionChanged = events.Event()
        
    def set_collection(self, new_contents):
        current = set(self._Internal_Collection)
        incoming = set(new_contents)
        additions = incoming.difference(current)
        deletions = current.difference(incoming)
        for d in deletions:
            del (self._Public_Collecton[d])
        for a in additions:
            self._Public_Collecton[a] = self.Conversion(a)
        self._Internal_Collection = new_contents
        if len(additions) + len(deletions):
            self.CollectionChanged(collection = [self._Public_Collecton[i] for i in self._Internal_Collection])
    
    def __iter__(self):
        for item in self.Contents: yield item
        
    @property
    def Contents(self):
        return [self._Public_Collecton[i] for i in self._Internal_Collection]
    @property
    def Count(self):
        return len(self._Internal_Collection)

        
        
        
    

