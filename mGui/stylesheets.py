'''
helper functions for creating default CSS sheet
'''

from mGui.styles import CSS, Bounds
from mGui.core.controls import Labeled, IconTextButton, IconTextCheckBox
from mGui.core import Control


def defaults(labels=128, controls=128, label_space = 8, field_space = 1, margin = (0,)):
    m = Bounds(*margin)
    with CSS(Control, margin=m, width=labels + controls) as defaults:
        
        # default style for labeled 'XXXGrp' controls
        CSS(Labeled, 
                 columnWidth2=(labels, controls),
                 columnWidth3=(labels, controls / 2 , controls / 2),
                 columnWidth4=(labels, controls / 3,  controls / 3, controls / 3),                     
                 columnAttach2= ['both'] * 2,
                 columnAttach3=['both'] * 3,
                 columnAttach4=['both'] * 4,
                 columnOffset2= [label_space, field_space],
                 columnOffset3= [label_space] + [field_space] * 2,
                 columnOffset4=[label_space] + [field_space] * 3,
                 adjustableColumn = 1,
                 rowAttach = (1, 'both', field_space))
    
        CSS(IconTextButton, style='iconAndTextHorizontal')
        CSS(IconTextCheckBox, style='iconAndTextHorizontal')
        


    return defaults

