'''
helper functions for creating default CSS sheet
'''

from mGui.styles import CSS, Bounds
from mGui.controls import *
from mGui.core import Control, Labeled



def defaults(labels = 64, controls = 192, margin = 4):
    m = Bounds(margin)
    
    control_rt = controls
    control_mid, control_r = ((controls * .75) - m.right), ((controls * .25) - m.right)
    
    
    with CSS(Control, margin = m, width = labels + controls) as defaults:
        CSS(Labeled, columnWidth2 = (labels, control_rt), 
                     columnWidth3 = (labels, control_mid, control_r),
                     columnAttach2= ("right", "both"), 
                     columnAttach3 =("right", "both", "both"),
                     columnOffset2= (m.right, 0), 
                     columnOffset3= (m.right, 0, 0) )
        CSS(IconTextButton, style = 'iconAndTextHorizontal')
        CSS(IconTextCheckBox, style = 'iconAndTextHorizontal')
        
    
    return defaults

                                