'''
Created on Feb 13, 2014

@author: Stephen Theodore
'''





class CSS (dict):    
    '''
    A css is a dictionary of style values keyed to a particular target.
    
    If <target> is a class, the style applies to any instance of that class
    if <target> is a string, the style applies to a control with that name
    
    Styles can inherit content (NOT targets!) from each other. Thus:
    
            a = CSS('a', color = 'red', margin = 1)
            b = CSS('b', a, width = 128}
            print b
            # {'color':'red', 'margin':1, 'width':128}
            
    Multiple inheritance is allowed:
            a = CSS('a', color = 'red'}            
            b = CSS('b', width = 128}
            c = CSS('c', a, b, margin = 1}
            print c
            # {'color':'red', 'margin':1, 'width':128}
    
    Later assignments overwrite earlier ones. Explicit assignments are the 'latest' of all:
            a = CSS('a', color = 'red'}            
            b = CSS('b', color = 'blue', width = 128}
            c = CSS('c', a, b, width = 256}
            print c
            # {'color':'blue',  'width':256}
    
    Styles can be used as context managers. All styles declared inside a context
    manager automatically inherit from it:
    
            with styles.CSS('outer', width = 100, height = 100) as outer:
                with styles.CSS('inner', bgc = (1,0,0), size = 3) as inner:
                    q = styles.CSS('innermost', size = 4)
            assert q['width'] == outer['width']
            assert q['bgc'] == inner['bgc']
            assert q['size'] == 4
            
    Styles can be nested. The context manager syntax does this automatically, or
    users can explicitly add child styles with add_child. Using the find method
    to get the appropriate style for a control will walk the nested control
    hierarchy from the bottom upwards, so more specific styles would be at the
    bottom of the hierarchy
    
            with styles.CSS(MockCtrl, name ='outer') as outer:
                    with styles.CSS(MockButton, name = 'middle') as middle:
                        inner = styles.CSS(MockRedButton, name = 'inner')
      
            test = MockRedButton('mrb')
            assert outer.find(test)['name'] == 'inner'  
            # inner style wins because it's lowest in the the nesting. this IS NOT 
            # based on class hierarchy among targets! If inner looked at MockButton 
            # (the parent class of MockRedButton) it would STILL win in this example
            
    '''
    
    ACTIVE = None
    
    def __init__(self, target, *templates, **kwarg):
        super(CSS,self).__init__()
        if CSS.ACTIVE:
            templates = [CSS.ACTIVE] + [i for i in templates]
        map(self.update, templates)
        self.update(**kwarg)
        self.Target = target
        self.Children = []
        if CSS.ACTIVE:
            CSS.ACTIVE.Children.append(self)

    def __enter__(self):
        self._cache_css = CSS.ACTIVE
        CSS.ACTIVE = self
        return self
        
    def __exit__(self, exc, val, tb):
        CSS.ACTIVE = self._cache_css

    def applies(self, ctrl):
        '''
        return True if this style matches the name or class of <ctrl>
        '''
        return  (self.Target == ctrl.Key) or isinstance(ctrl, self.Target) 
    
    def find(self, ctrl):
        '''
        find the 
        '''
        for item in self.Children:
            recurse = item.find(ctrl)
            if recurse: return recurse
            
        if self.applies(ctrl):
            return self
        
                
    
        