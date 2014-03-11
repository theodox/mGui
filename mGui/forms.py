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
from mGui.styles import CSS

import maya.cmds as cmds
import itertools





class FormBase( FormLayout ):
    
    def __init__(self, key, *args, **kwargs):
        super(FormBase, self).__init__(key, *args, **kwargs)
        self.margin = self.Style.get('margin', 0)
        self.spacing = self.Style.get('spacing', 0)


    def _fill( self, ctrl, margin, *sides ):
        '''
        convenience wrapper for tedious formLayout editing
        '''
        ct = [ctrl for _ in sides]
        mr = [margin for _ in sides]
        self.attachForm=zip( ct, sides, mr ) 


    def top( self, ctrl, margin ):
        '''
        Docks 'ctrl' against the top of the form, with the supplied margin on top, left and right
        '''
        sides = ['top', 'left', 'right']
        self._fill( ctrl, margin, *sides )

    def left( self, ctrl, margin ):
        '''
        dock 'ctrl' along the left side of the form with the supplied margin
        '''
        sides = ['top', 'left', 'bottom']
        self._fill( ctrl, margin, *sides )

    def right ( self, ctrl, margin ):
        '''
        dock 'ctrl' along the right side of the form with the supplied margin
        '''
        sides = ['top', 'right', 'bottom']
        self._fill( ctrl, margin, *sides )

    def bottom( self, ctrl, margin ):
        '''
        dock 'ctrl' along the bottom of the form with the supplied margin
        '''
        sides = ['bottom', 'left', 'right']
        self._fill( ctrl, margin, *sides )


    def fill( self, ctrl, margin ):
        '''
        docks 'ctrl' into the form filling it completely with suppled margin on all sides
        '''
        sides = ['top', 'bottom', 'left', 'right']
        self._fill( ctrl, margin, *sides )

    def snap( self, ctrl1, ctrl2, edge, margin ):
        '''
        docs 'ctrl1' to 'ctrl2' along the supplied edge (top, left, etc) with the supplied margin
        '''
        self.attachControl=( ctrl1, edge, margin, ctrl2 )



    def dock( self, ctrl, top=None, left=None, right=None, bottom=None ):
        '''
        docks ctrl into the form.
        
        for each of the optional flags (top, bottom, left, & right), the arguments are interpreted as follows:
        None (default):  Ignore this edge
        Number (eg 10):  dock to form with this margin along this edge
        (ctrl2, number): dock to other control 'ctrl2' along this edge, with supplied margin
        '''

        if not hasattr( top, '__iter__' ): top = ( None, top )
        if not hasattr( bottom, '__iter__' ): bottom = ( None, bottom )
        if not hasattr( left, '__iter__' ): left = ( None, left )
        if not hasattr( right, '__iter__' ): right = ( None, right )

        ac = lambda edge, other, margin : cmds.formLayout( self.Widget, e=True, ac=( ctrl, edge, margin, other ) ) 
        af = lambda edge, ignore, margin:  cmds.formLayout( self.Widget, e=True, af=( ctrl, edge, margin ) ) 
        
        if top[0]:
            ac( 'top', *top )
        elif top[1]:
            af( 'top', *top )

        if left[0]:
                ac( 'left', *left )
        elif left[1]:
                af( 'left', *left )

        if bottom[0]:
            ac( 'bottom', *bottom )
        elif bottom[1]:
            af( 'bottom', *bottom )

        if right[0]:
                ac( 'right', *right )
        elif right[1]:
                af( 'right', *right )

class DockForm (FormBase):
    
        
    def layout(self):
        self.fill(self.Controls[0], self.margin)
        return len(self.Controls)
              
class VerticalForm(FormBase):
    
    def layout(self):
        m1, m2 = itertools.tee(self.Controls)
        ac  = []
        af = []
        af.append ( (m1.next(), 'top', self.margin))
        
        for b, t in itertools.izip(m1, m2):
            ac.append( (b, 'top', self.margin, t) )
            af.append( (t, 'left', self.margin) )
            af.append( (t, 'right', self.margin)) 

        last = m2.next()
        af.append((last, 'left', self.margin))
        af.append((last, 'right', self.margin))

        self.attachControl = ac
        self.attachForm = af
        
        return len(self.Controls)
    
class HorizontalForm(FormBase):
     
    def layout(self):
        m1, m2 = itertools.tee(self.Controls)
        ac  = []
        af = []
        
        # experimantal...
        
        totalmargin = lambda q: self.margin + q.Style.get('margin', 0)
        
        first = m1.next()
        af.append( ( first, 'left', totalmargin(first) ))
        
        for b, t in itertools.izip(m1, m2):
            ac.append( (b, 'left',  totalmargin(t), t) )
            af.append( (t, 'top',  totalmargin(t) ) )
            af.append( (t, 'bottom',  totalmargin(t)) )

        last = m2.next()
        af.append( (last, 'top',  totalmargin(last)) )
        af.append(  (last, 'bottom',  totalmargin(last) ) )

        self.attachControl = ac
        self.attachForm = af

        return len(self.Controls)

