'''
Created on Feb 13, 2014

@author: Stephen Theodore
'''
class CSS (dict):    
    def __init__(self, id, **kwarg):
        super(CSS,self).__init__()
        if kwarg.get('parent'):
            p = kwarg['parent']
            del kwarg['parent']
            self.update(p)
        self.update(**kwarg)
        self.ID = id
        
    
class StyleBlock(object):
    ACTIVE = {}
    
    def __init__(self, style):
        self.Style = style
        StyleBlock.ACTIVE = self.Style

        
    def __enter__(self):
        return self
    
    def __exit__( self, typ, value, traceback ):
        self.ACTIVE = None
        
    @classmethod
    def current(cls):
        return cls.ACTIVE or {}
    
    @classmethod
    def set(cls, style):
        cls.ACTIVE = style
