'''
Created on Feb 15, 2014

@author: Stephen Theodore
'''


from .layouts import FormLayout;
from .layouts import FrameLayout;
from .layouts import ColumnLayout;
from .layouts import ScrollLayout;
from collections import namedtuple


#===============================================================================
# class LayoutUnit(object):
#    def __init__(self, value, unit):
#        self.Value = value
#        self.Unit = unit
#    
#    def pixels(self):
#        u
# 
# 
# class Margin(object):
#    def __init__(self, left = 0, right = 0, top = 0, bottom = 0):
#        self.Left = left
#        self.Top = top
#        self.Right = right
#        self.Bottom = bottom
#        
# class CSSSpecParser(object):
#    
#    
#    def parse(self, **style):
#        top = 0;
#        left = 0;
#        bottom = 0;
#        right = 0;
#        if 'margin' in kwargs:
#            margin_vals = kwargs.get('margin', (0,))
#            if len(margin_vals) == 0: margin_vals = (margin_vals[0], margin_vals[0], margin_vals[0], margin_vals[0] )
#            opts = dict([a for a in zip(("left", "right","top","bottom"), margin_vals)])
#            self.Margin = Margin(**opts)
#            del kwargs['margin']
#        for each_margin in (('margin-left', 'margin-right', 'margin-top', 'margin-bottom')):
#            if each_margin in kwargs:
#                kwargs.get
# 
#    def parse_value(self, val):
#        '''
#        givne 
#        '''
#        if val == 'auto': return None
#        
#        try:
#            return CSSValue(float(val), 'px')
#        except ValueError:
#            units = [('in', 72), ('cm', 180), ('mm',1800), ('em', 1)
#            
#            val = val.replace('p', ' p')
#            val = val.replace('e', ' e')
#            val = val.replace('%', ' %')
#                percentage
# in    inch
# cm    centimeter
# mm    millimeter
# em    1em is equal to the current font size. 2em means 2 times the size of the current font. E.g., if an element is displayed with a font of 12 pt, then '2em' is 24 pt. The 'em' is a very useful unit in CSS, since it can adapt automatically to the font that the reader uses
# ex    one ex is the x-height of a font (x-height is usually about half the font-size)
# pt    point (1 pt is the same as 1/72 inch)
# pc    pica (1 pc is the same as 12 points)
# px    pixels (a dot on the computer screen)
#            
#            
#            spec,_, valtype = val.partition(' ')
#            if not valtype in ('%', 'px', 'em'):
#                raise ValueError("%s is not a recognized CSS unit", valtype)
#            return  CSSValue(float(spec), valtype)
#        
#===============================================================================
        

class Div(FormLayout):
    
    
    def __init__(self, id, *args, **kwargs):

            
        super(Div, self).__init__(id, *args, kwargs)
        
    def __exit__(self,):
        