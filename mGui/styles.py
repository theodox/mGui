'''
Defines the CSS class, a cascading style sheet like class for GUI layout.

Also defines the Bounds class, which reprsents margins
'''

class Bounds(object):
    '''
    A bounding area (in pixels).  Can be constructed 3 ways:
    
        Bounds (10) : 10 pixel margin on all sides
        Bounds (5, 10):  5 pixel horizontal and 10 pixel vertical margin
        Bounds (5, 10, 15, 20) : eplicit left, top, right, bottom
    
    left, right, top and bottom can be accessed by point or dictionary style
    notation
        B = Bounds(10,20)
        B.left
        # 10
        B['top']
        # 20
    '''
    def __init__(self, *args):
        vals = list(args) * 2  + [0] * 4
        if len(args) == 1:
            vals = list(args) * 4
        self.left, self.top, self.right, self.bottom = vals[:4]

    def __getitem__(self, key):
        return {
        'left':self.left,
        'right':self.right,
        'top':self.top,
        'bottom': self.bottom
         }[key]
         
        
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
            
            
    The context manager functionality is REUSABLE. The examples above show how
    nested contexts can be use to prioritize the search order for different
    styles.  The other use is to activate a style for use in the creation of
    controls:
        with styles.CSS(StyledMockCtrl, width = 100, height = 100, expected = False) as outer:
            with styles.CSS(StyledMockButton, bgc = (1,0,0), size = 3, expected = None):
                deepest = styles.CSS(StyledMockRedButton, size = 4, expected = True)
                        
        with outer:
            test = StyledMockRedButton('fred')  # uses deepest on creation, as in earlier example
            test2 = StyledMockList('barney')    # uses uses outer, since its the closes match for the class
            test3 = UnStyledButton('nostyle')   # if the class does not derive from Styled, nothing happens
            test4 = StyledMockButton('custom', style = CSS('custom', width = 11, height=91)) 
                                                # explicitly passed style wins over the styles in outer.
                                
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

    def applies(self, *args):
        '''
        return True if this style matches the arguments.  Arguments are EITHER a control OR a class, key pair
        '''
        if len(args) == 1:
            ctrl = args[0]
            return  (self.Target == ctrl.Key) or isinstance(ctrl, self.Target) 
        if len(args) == 2:
            cls, key = args
            if self.Target == key:
                return True
            if isinstance(self.Target, type):
                return issubclass(cls, self.Target)
            return False
    
    
    def find(self, *args):
        '''
        find the style in this nested style which matches the supplied arg.  See applies for arguments.
        '''
        for item in self.Children:
            recurse = item.find(*args)
            if recurse: return recurse
            
        if self.applies(*args):
            return self
        
    @classmethod
    def current(cls):
        return cls.ACTIVE
    
class Styled(object):
    '''
    Mixin class which makes an object try to hook the appropriate style from CSS.curretn
    '''
    def __new__(self, *args, **kwargs):
        obj = object.__new__(self)
        self.Style = kwargs.get('css', {})
        current_style = CSS.current()
        if current_style and not self.Style:
            self.Style = current_style.find(self, args[0]) or self.Style
        
        # intercept the style argument before __init__ so any
        # non-style arguments are passed directly
        if 'css' in kwargs:
            del kwargs['css']
                
        return obj
   
                                