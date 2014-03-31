import mGui.gui as gui
import mGui.stylesheets as stylesheets
from mGui.bindings import BindProxy, BindingContext, bind, Bindable

class ExampleWindow(Bindable):
    '''
    This example simple window with color sliders
    '''    

    
    def __init__(self):
        self.Color = [0,0,0]
        
        # 2-digit formmating
        pretty = lambda x:'{0[0]:.2f} {0[1]:.2f} {0[2]:.2f}'.format(x)

        with stylesheets.CSS(gui.FloatSliderButtonGrp, 
                            stylesheets.defaults(), 
                            columnWidth3 = (64, 96,32),  minValue = 0, maxValue = 1, backgroundColor = (1,1,1) ):

            with gui.BindingWindow('window', title = 'simple example',  width=512) as self.Window:
                with gui.HorizontalStretchForm('main', width = 512):
                    with gui.VerticalForm('controls', width = 256) as sliders:
                        self.xXX= gui.FloatSliderButtonGrp('red', label = 'red', tag = 0)
                        gui.FloatSliderButtonGrp('green', label = 'green', tag = 1)
                        gui.FloatSliderButtonGrp('blue', label = 'blue', tag = 2)
                    with gui.FillForm('swatch', width = 256):
                        gui.Canvas('canvas').bind.rgbValue <  bind() <  self.bind.Color
                        gui.Text('display').bind.label < bind(pretty) < self.bind.Color
    
            for grp in sliders.Controls:
                grp.changeCommand += self.update_color
                grp.buttonCommand += self.average
                
    def update_color(self, *args, **kwargs):
        self.Color[kwargs['sender'].Tag] = kwargs['sender'].value
        self.Window.bindingContext.update()
        
    def average(self, *args, **kwargs):
        kwargs['sender'].value = sum(self.Color) / 3
        self.update_color(*args, **kwargs)

    def show(self):
        self.Window.show()
        

e = ExampleWindow()
e.show()