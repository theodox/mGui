from mGui.gui import *
from mGui.forms import *
from mGui.lists import *
from mGui.observable import *
from mGui.bindings import *
import random



def basic_list_binding():
    '''
    Illustrates the basics of binding to a list.  The collection 'bound' contains some strings,
    and we bind it to the VerticalList 'list_view'. Adding items to the collection
    automatically redraws the list with the new items.

    This example also illustrates how to use closures to capture inter-object references, and how
    to keep callback functions alive without creating a full class.
    '''

    with BindingWindow(title = 'example window') as test_window:
    
        bound = ViewCollection('pPlane1', 'pCube2')
        with VerticalThreePane() as main:
            Text(label = "The following items don't have vertex colors")
            list_view = VerticalList(synchronous = True)
            bound > bind() > list_view.collection
            with HorizontalStretchForm('buttons'):
                more = Button('more!')
                close = Button('close')

    # use closures to capture the UI names without a full class
    def close_window(*_, **__):
        cmds.deleteUI(test_window)
        
    def show_more(*_, **__):
        r = random.choice(("pPlane", "pCube", "pSphere")) + str(random.randint(2,20))
        bound.append(r)

    # these keep the functions above from dropping out of scope
    test_window.close_window = close_window
    test_window.more = show_more

    # bind the functions to the handlers
    more += test_window.more
    close += test_window.close_window

    return test_window
    
the_window = basic_list_binding()
the_window.show()