from mGui import gui, forms, lists
from mGui.bindings import bind
from mGui.observable import ViewCollection
import random


def basic_list_binding():
    '''
    Illustrates the basics of binding to a list.  The collection 'bound' contains some strings,
    and we bind it to the VerticalList 'list_view'. Adding items to the collection
    automatically redraws the list with the new items.

    This example also illustrates how to use closures to capture inter-object references, and how
    to keep callback functions alive without creating a full class.
    '''

    with gui.BindingWindow(title='example window') as test_window:
        bound = ViewCollection('pPlane1', 'pCube2')
        with forms.VerticalThreePane() as main:
            header = gui.Text(label="The following items don't have vertex colors")
            list_view = lists.VerticalList(synchronous=True)
            bound > bind() > list_view.collection
            with forms.HorizontalStretchForm() as buttons:
                more = gui.Button(label='more!')
                close = gui.Button(label='close')

    # use closures to capture the UI names without a full class
    def close_window(*_, **__):
        cmds.deleteUI(test_window)

    def show_more(*_, **__):
        r = random.choice(("pPlane", "pCube", "pSphere")) + str(random.randint(2, 20))
        bound.append(r)

    # bind the functions to the handlers
    close.command += close_window, test_window
    more.command += show_more, test_window

    return test_window

if __name__ == '__main__':
    the_window = basic_list_binding()
    the_window.show()
