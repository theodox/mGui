'''
Created on Mar 7, 2014

@author: Stephen Theodore
'''
import unittest
import mGui.styles as styles

class MockCtrl(object):
    
    def __init__(self, key, **kwargs):
        self.Style = kwargs
        self.Key = key
        
class MockButton(MockCtrl):
    pass

class MockRedButton(MockButton):
    pass

class MockList(object):
    pass



class Test_CSS(unittest.TestCase):

    def test_css_params(self):
        example = styles.CSS(object().__class__, width = 10, height = 10 )
        assert example['width'] == 10
        assert example['height'] == 10
        
        
    def test_css_derive_unique(self):
        p = styles.CSS('outer',  width = 10, height = 10 )
        c = styles.CSS('inner', p,  color = 'red',  height = 3)
        assert c['color'] == 'red'

    def test_css_derive_inherit(self):
        p = styles.CSS('outer',  width = 10, height = 10 )
        c = styles.CSS('inner', p, color = 'red',  height = 3)
        assert c['width'] == p['width']
      
    def test_css_derive_override(self):
        p = styles.CSS('outer',  width = 10, height = 10 )
        c = styles.CSS('inner', p, color = 'red',  height = 3)
        assert c['height'] == 3
        
    def test_css_nesting(self):
        with styles.CSS('outer', width = 100, height = 100) as outer:
            with styles.CSS('inner', bgc = (1,0,0), size = 3) as inner:
                q = styles.CSS('innermost', size = 4)
            z = styles.CSS('2dlevel', q, bgc = (2,0,0))
        assert inner in outer.Children
        assert q in inner.Children
        assert z in outer.Children
        
    def test_css_nesting_values(self):
        with styles.CSS('outer', width = 100, height = 100) as outer:
            with styles.CSS('inner', bgc = (1,0,0), size = 3) as inner:
                q = styles.CSS('innermost', size = 4)
        assert q['width'] == outer['width']
        assert q['bgc'] == inner['bgc']
        assert q['size'] == 4
        
    def test_css_nesting_and_manual_values(self):
        with styles.CSS('outer', width = 100, height = 100) as outer:
            with styles.CSS('inner', bgc = (1,0,0), size = 3) as inner:
                q = styles.CSS('innermost', size = 4)
            z = styles.CSS('upper', q, bgc=(2,0,0))
        assert z['bgc'] == (2,0,0)

    def test_css_inherit_order(self):
        a = styles.CSS('a', color = 'red', margin = 1)
        b = styles.CSS('b', color = 'blue', width = 128, float = 'left')
        c = styles.CSS('c', color = 'green', width = 256)
        d = styles.CSS('test', a, b, c)
        assert d['color'] == 'green'
        assert d['width'] == 256
        assert d['float'] == 'left'
        assert d['margin'] == 1
        
        e = styles.CSS('test', c, a, b)
        assert e['color'] == 'blue'
        assert e['width'] == 128


    def test_style_applies_on_class(self):
        example = MockCtrl('hello')
        style = styles.CSS(MockCtrl, found=1)
        assert style.applies(example)
        
    def test_style_applies_on_name(self):
        example = MockCtrl('hello')
        style = styles.CSS('hello', found=1)
        assert style.applies(example)
        
    def test_style_finds_lowest_in_hierarchy(self):
        '''
        note as written, this privileges POSITION hierarchy over CLASS hierarchy... is that bad?
        '''
        with styles.CSS(MockCtrl, name ='outer') as outer:
            with styles.CSS(MockButton, name = 'middle') as middle:
                inner = styles.CSS(MockRedButton, name = 'inner')
  
        test = MockRedButton('mrb')
        assert outer.find(test)['name'] == 'inner'
        
                
    def test_style_finds_lowest_in_hierarchy_despite_class_hierarchy(self):
        '''
        see docs. Style hierarchy position matters, not class hieratchy!
        '''
        with styles.CSS(MockCtrl, name ='outer') as outer:
            with styles.CSS(MockRedButton, name = 'middle') as middle:
                inner = styles.CSS(MockButton, name = 'inner')
  
        test = MockRedButton('mrb')
        assert outer.find(test)['name'] == 'inner'
        
        