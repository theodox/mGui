import maya.cmds as cmds
import mGui.gui as gui
import mGui.observable as observable
import mGui.lists as lists
import mGui.forms as forms
from mGui.bindings import bind

'''
This sample shows a basic example of using a bound collection

Key points:

    1) The ViewCollection object is a list of scene objects. Adding or removing
    items to the collection automatically adds or removes their widgets from the
    UI

    2) The ViewCollection can be filtered; this will show or hide widgets (but does
    not destroy them so they come back quickly if the filter changes)

    3) The ViewCollection is bound to the VerticalList -- Lists contain an internal
    BoundCollection and are an easy way to fill a list with widgets representing
    stuff in another list. So the working logic interacts with the ViewCollection,
    the List (or more correctly, the List's BoundCollection) displays stuff.

    4) The ExampleTemplate class is responsible for creating the actual
    UI for each object in the collection. It can be changed without altering the
    main UI

    5) The individual item widget can have their own events. They can be handled locally
    or forwarded. To forward an event, return any events you want to forward as keywords
    in the Templated() call.

    6) The List raises a NewWidget event when a new GUI item is created for a
    list item. You can look at the widget created and add event handlers at that
    time, as is done in the hook_widget_events function.  (This is optional,
    it's only needed if you want the outer code to handle events instead of
    localizing them to widgets. Typically this would only be for things which
    affect the original collection (such as deletion) rather than stuff which
    only affects a single item in the collection.

'''


class ExampleTemplate(lists.ItemTemplate):
    def widget(self, item):
        with forms.HorizontalExpandForm('tmp_%i' % id(item), parent=self.Parent, width=250,) as root:
                gui.IconTextButton('delete', style='iconAndTextHorizontal', image='delete', tag=item)
                with forms.VerticalForm('names'):
                    gui.NameField(0, object=item, width=250)
                with forms.VerticalForm('xform'):
                    gui.AttrFieldGrp('t', label='translate', attribute=item + ".t")

        return lists.Templated(item, root, request_delete=root.delete.command)


class BoundCollectionWindow(object):
    def __init__(self, collection):

        # this is the collection of stuff to manage
        self.Collection = observable.ViewCollection(*collection)

        with gui.BindingWindow('root', title='bound collection example') as self.Window:
            with gui.VerticalExpandForm('main') as main:
                gui.Separator(None, style='none', height=12)
                gui.Text(None, label="Here's stuff in my list")
                gui.Separator(None, style='none', height=12)

                with forms.HorizontalStretchForm('filter') as flt:
                    gui.TextField('filtertext', width=480)
                    gui.Separator(None, horizontal=False, style='none', width=4)
                    with gui.FlowLayout('display', width=32) as hmm:
                        gui.Text('shown').bind.label < bind() < self.Collection.bind.ViewCount
                        gui.Text(None, '/')
                        gui.Text('total').bind.label < bind() < self.Collection.bind.Count

                self.Collection > bind() > lists.VerticalList('itemList', itemTemplate=ExampleTemplate).Collection

        self.Window.main.itemList.NewWidget += self.hook_widget_events
        flt.filtertext.enterCommand += self.update_filter

    def update_filter(self, *args, **kwargs):
        sender = kwargs['sender']
        try:
            l_string = "lambda x : x %s"
            filter_exp = eval((l_string % sender.text))

            self.Collection.update_filter(filter_exp)
        except:
            self.Collection.update_filter(None)

    def do_delete(self, *args, **kwargs):
        self.Collection.remove(kwargs['sender'].Tag)
        cmds.delete(kwargs['sender'].Tag)

    def hook_widget_events(self, *args, **kwargs):
        kwargs['item'].Events['request_delete'] += self.do_delete

    def show(self):
        self.Window.show()

test = BoundCollectionWindow([])
test.show()
test.Collection.add(*cmds.ls(type='transform'))
