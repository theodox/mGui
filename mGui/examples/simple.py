import mGui.gui as gui
import mGui.stylesheets as stylesheets
from mGui.bindings import BindProxy, BindingContext, bind, Bindable

class ExampleWindow(Bindable):
    """
    This example simple window with color sliders
    
    This showcases two different methods of passing information between parts of the UI.
    
    The sliders and buttons use more or less conventional events to update the
    instance field "Color", which is an RGB value.  This is pretty much the way
    its always done in Maya, although this example uses the += event binding
    syntax to attach the event handlers rather than the vanilla command = handler 
    syntax.
    
    The color and the text display, however, are driven by bindings; the buttons and sliders
    update the Color field, and the bindings make sure that the swatch and overlay text
    display the current values. Since the window is a BindingWindow, it comes with a 
    built-in BindingContext (see bindings.py for details) so all the text and color
    bindings are updated with a single call.
    
    The slider handlers can all share a function through the use of the Tag field.
    
    Also of interest, the CSS style at the top sets the style context for all of the 
    FloatSliderButtonGrp widgets so they are lined up neatly.  Notice that inherits from
    stylesheets.defaults(), which includes a base style for all '_Grp' controls to set the 
    text aligments and sizes of the labels consistently.
    
    Note on Maya 2011 this color swacth does not fill the entire right-hand
    panel; on Maya 2014 it does. This appears to be a change in the behavior of
    the underlying widget between versions.
    """

    
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
                        gui.FloatSliderButtonGrp('red', label = 'red', tag = 0)
                        gui.FloatSliderButtonGrp('green', label = 'green', tag = 1)
                        gui.FloatSliderButtonGrp('blue', label = 'blue', tag = 2)
                    with gui.FillForm('swatch', width = 256):
                        gui.Canvas('canvas').bind.rgbValue <  bind() <  self.bind.Color
                        gui.Text('display').bind.label < bind(pretty) < self.bind.Color
    
            for grp in sliders.controls:
                grp.changeCommand += self.update_color
                grp.buttonCommand += self.average
                
    def update_color(self, *args, **kwargs):
        self.Color[kwargs['sender'].tag] = kwargs['sender'].value
        self.Window.bindingContext.update()
        
    def average(self, *args, **kwargs):
        kwargs['sender'].value = sum(self.Color) / 3
        self.update_color(*args, **kwargs)

    def show(self):
        self.Window.show()
        

e = ExampleWindow()
e.show()