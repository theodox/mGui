import random
from mGui import gui, forms, lists
from mGui.observable import ViewCollection
from mGui.bindings import bind


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
            gui.Text(label="The following items don't have vertex colors")
            list_view = lists.VerticalList(synchronous=True)
            bound > bind() > list_view.collection
            with forms.HorizontalStretchForm('buttons'):
                more = gui.Button('more!')
                close = gui.Button('close')

    # use closures to capture the UI names without a full class
    def close_window(*_, **__):
        cmds.deleteUI(test_window)

    def show_more(*_, **__):
        r = random.choice(("pPlane", "pCube", "pSphere")) + str(random.randint(2, 20))
        bound.append(r)

    # bind the functions to the handlers
    more *= show_more
    close *= close_window

    return test_window

if __name__ == '__main__':
    the_window = basic_list_binding()
    the_window.show()
