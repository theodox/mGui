import mGui.gui as gui
import mGui.stylesheets as stylesheets
from mGui.bindings import BindProxy, BindingContext


class ExampleWindow(object):
    '''
    simple window with color sliders
    '''    
    def __init__(self):
        self.Color = [0,0,0]
        with stylesheets.defaults(  margin = (0,) ) as defaults:
            stylesheets.CSS(gui.FloatSliderButtonGrp, columnWidth3 = (64, 96,32),  minValue = 0, maxValue = 1 )
        
        with defaults:
            with gui.Window('window', title = 'simple example',  width=512) as self.Window:
                with gui.HorizontalStretchForm('main', width = 512):
                    with gui.VerticalForm('controls', width = 256) as sliders:
                        gui.FloatSliderButtonGrp('red', label = 'red', tag = 0 )
                        gui.FloatSliderButtonGrp('green', label = 'green', tag = 1)
                        gui.FloatSliderButtonGrp('blue', label = 'blue', tag = 2)
                    with gui.FillForm('swatch', width = 256):
                        self.canvas = gui.Canvas('canvas', rgbValue = self.Color)
                        self.b = gui.Text('display') + 'label' << BindProxy( self, 'Color', translator = lambda x: str(x))    

        for grp in sliders.Controls:
            grp.changeCommand += self.update_color
            grp.buttonCommand += self.average
            
    def update_color(self, *args, **kwargs):
        self.Color[kwargs['sender'].Tag] = kwargs['sender'].value
        self.canvas.rgbValue = self.Color
        self.b()
        
    def average(self, *args, **kwargs):
        kwargs['sender'].value = sum(self.Color) / 3
        self.update_color(*args, **kwargs)
         

test = ExampleWindow()
test.Window.show()