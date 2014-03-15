'''
forms.py

Extensions to formLayout for easier management
@author: Stephen Theodore


@note

Did some empirical testing, and it appears that lots of attachments is slower
than lots of simple forms. Thus generating a columnLayout containing 1000
buttons, each wrapped in its own formlayout takes .86 seconds on my machine;
where one formlayout with 1000 buttons takes 1.89 seconds if the buttons are
attached to both sides of form and 1.25 if they are not; a differences of
between 50 and 100%

The same 1000 buttons with no individual form layouts  = .53 seconds

For this reason prefer row or column or flowlayouts for repetitive stuff and use forms for the main architecture

pretty consistenly groups of 100-odd sets of 3 controls (300 total) came in under .25s

'''
from mGui.layouts import FormLayout
from mGui.styles import CSS, Bounds

import maya.cmds as cmds
import itertools





class FormBase(FormLayout):
    '''
    A wrapper for FormLayout with convenience methods for attaching controls.
    Use this when you need precise control over form behavior.
    
    Formbase is entirely manual - it does no automatic layout behavior.
    
    '''
    
    def __init__(self, key, *args, **kwargs):
        super(FormBase, self).__init__(key, *args, **kwargs)
        self.margin = self.Style.get('margin',  Bounds(0, 0) )
        self.spacing = self.Style.get('spacing', Bounds(0, 0) ) 


    def _fill(self, ctrl, margin, *sides):
        '''
        convenience wrapper for tedious formLayout editing
        '''
        ct = [ctrl for _ in sides]
        mr = [self.margin[_] for _ in sides]
        self.attachForm = zip(ct, sides, mr) 


    def top(self, ctrl, margin):
        '''
        Docks 'ctrl' against the top of the form, with the supplied margin on top, left and right
        '''
        
        self._fill(ctrl, margin, 'top', 'left', 'right')

    def left(self, ctrl, margin):
        '''
        dock 'ctrl' along the left side of the form with the supplied margin
        '''
        sides = ['top', 'left', 'bottom']
        self._fill(ctrl, margin, *sides)

    def right (self, ctrl, margin):
        '''
        dock 'ctrl' along the right side of the form with the supplied margin
        '''
        sides = ['top', 'right', 'bottom']
        self._fill(ctrl, margin, *sides)

    def bottom(self, ctrl, margin):
        '''
        dock 'ctrl' along the bottom of the form with the supplied margin
        '''
        sides = ['bottom', 'left', 'right']
        self._fill(ctrl, margin, *sides)


    def fill(self, ctrl, margin):
        '''
        docks 'ctrl' into the form filling it completely with suppled margin on all sides
        '''
        sides = ['top', 'bottom', 'left', 'right']
        self._fill(ctrl, margin, *sides)

    def snap(self, ctrl1, ctrl2, edge, margin):
        '''
        docs 'ctrl1' to 'ctrl2' along the supplied edge (top, left, etc) with the supplied margin
        '''
        self.attachControl = (ctrl1, edge, margin, ctrl2)


    def form_attachments(self, *sides):
        '''
        returns a list of (control, side, spacing) values used by attachForm style commands
        '''
        attachments = ( [side, self.spacing[side]]  for side in sides)
        ctls = itertools.product(self.Controls, attachments)
        return [ [a] + b for a, b in ctls]
        
    def form_series (self, side):
        '''
        returns a series of (control, side, space, control) for use in serial placement
        '''
        first, second = itertools.tee(self.Controls)
        second.next()
        return [ (s, side, self.spacing[side], f) for f, s in itertools.izip(first, second)]

    def percentage_series(self, side):
        
        side2 = {'left':'right', 'right':'left', 'top':'bottom', 'bottom':'top'}[side]
        

        widths = [i.width for i in self.Controls]
        total_width = sum(widths)
        proportions = map (lambda q: q * 100.0 / total_width, widths)
        p_l = len(proportions)
        left_edges = [sum(proportions[:r]) for r in range(0, p_l)]
        right_edges = [sum(proportions[:r]) for r in range(1,p_l + 1)]
        ap = []
        for c, l,r in itertools.izip(self.Controls, left_edges, right_edges):
            ap.append( ( c, side, self.spacing[side], l) ) 
            ap.append( ( c, side2,self.spacing[side2], r) ) 
        
        print ap
        return ap
    
    def dock(self, ctrl, top=None, left=None, right=None, bottom=None):
        '''
        docks ctrl into the form.
        
        for each of the optional flags (top, bottom, left, & right), the arguments are interpreted as follows:
        None (default):  Ignore this edge
        Number (eg 10):  dock to form with this margin along this edge
        (ctrl2, number): dock to other control 'ctrl2' along this edge, with supplied margin
        '''

        if not hasattr(top, '__iter__'): top = (None, top)
        if not hasattr(bottom, '__iter__'): bottom = (None, bottom)
        if not hasattr(left, '__iter__'): left = (None, left)
        if not hasattr(right, '__iter__'): right = (None, right)

        ac = lambda edge, other, margin : cmds.formLayout(self.Widget, e=True, ac=(ctrl, edge, margin, other)) 
        af = lambda edge, ignore, margin:  cmds.formLayout(self.Widget, e=True, af=(ctrl, edge, margin)) 
        
        if top[0]:
            ac('top', *top)
        elif top[1]:
            af('top', *top)

        if left[0]:
                ac('left', *left)
        elif left[1]:
                af('left', *left)

        if bottom[0]:
            ac('bottom', *bottom)
        elif bottom[1]:
            af('bottom', *bottom)

        if right[0]:
                ac('right', *right)
        elif right[1]:
                af('right', *right)

class FillForm (FormBase):
    '''
    Docks the first child so it fills the entire form with the specified margin
    '''
        
    def layout(self):
        self.fill(self.Controls[0], sum(self.margin) / 4)
        return len(self.Controls)
              
class VerticalForm(FormBase):
    
    def layout(self):
        
        af = []
        af = self.form_attachments('left', 'right')
        af.append ((self.Controls[0], 'top', self.spacing.top))
        af.append((self.Controls[-1], 'bottom', self.spacing.bottom))
        ac = self.form_series('top')
            
        self.attachForm = af
        self.attachControl = ac
        
        return len(self.Controls)
    
class HorizontalForm(FormBase):
    '''
    Lays out children horizontally. The first child is attacked to the left of
    the form, and the last to the right. The last division will expand with the
    form.
    '''
     
    def layout(self):
        af = self.form_attachments('top', 'bottom')
        af.append ((self.Controls[0], 'left', self.spacing.top))
        af.append((self.Controls[-1], 'right', self.spacing.bottom))
        ac = self.form_series('left')
                
        self.attachForm = af
        self.attachControl = ac
        
        return len(self.Controls)

class HorizontalStretchForm(FormBase):
    '''
    Lays out children horizontally. All children will scale proportionally as the form changes size
    '''
     
     
    # @todo - refactor this into a generic proportional layout,
    # parameterizes direcitons
    # allow controls to proclaim a width?
    def layout(self):
        
    
        af = self.form_attachments('top', 'bottom')
        ap = self.percentage_series('left')
        self.attachForm = af
        self.attachPosition = ap

        return len(self.Controls)
    
class VerticalStretchForm(FormBase):
    '''
    Lays out children vertically, with sizes proportional to their original heights
    '''
     
    def layout(self):
        
        af = []
        ap = []
        
        af = self.form_attachments('left', 'right')
        ap = self.percentage_series('top')
        self.attachForm = af
        self.attachPosition = ap

        return len(self.Controls) 
