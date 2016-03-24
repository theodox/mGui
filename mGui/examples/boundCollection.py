import maya.cmds as cmds
import mGui.gui as gui
import mGui.observable as observable
import mGui.lists as lists
import mGui.forms as forms
from mGui.bindings import bind

"""
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

"""


class ExampleTemplate(lists.ItemTemplate):
    def widget(self, item):
        with forms.HorizontalExpandForm('tmp_%i' % id(item), width=250, tag = item ) as root:
            delete_button=  gui.IconTextButton( style='iconAndTextHorizontal', image='delete')
            with forms.VerticalForm('names') as filler:
                name_field = gui.NameField(object=item, width=250)
            with forms.VerticalForm('xform'):
                gui.AttrFieldGrp('t', label='translate', attribute=item + ".t")

        delete_button.tag = root
        return lists.Templated(item, root, request_delete=root.delete_button.command)


class BoundCollectionWindow(object):
    KEEPALIVE = None
    # this is handy for the example, you don't want to do it this way
    # if you really need multiple windows: the single Keepalive will
    # only support the latest one at a time...

    def __init__(self, collection):

        # this is the collection of stuff to manage
        self.collection = observable.ViewCollection(*collection)

        with gui.BindingWindow(title='bound collection example') as self.window:
            with forms.VerticalExpandForm('main') as main:
                gui.Separator(style='none', height=12)
                gui.Text(label="Here's stuff in my list")
                gui.Separator(style='none', height=12)

                with forms.HorizontalStretchForm('filter') as flt:
                    gui.TextField('filtertext', width=480)
                    gui.Separator(horizontal=False, style='none', width=4)
                    with forms.HorizontalExpandForm('display', width=32) as hmm:
                        shown = gui.Text('shown').bind.label < bind() < self.collection.bind.viewCount
                        gui.Text(label='/')
                        total = gui.Text('total').bind.label < bind() < self.collection.bind.count

                self.collection > bind() > lists.VerticalList('itemList', itemTemplate=ExampleTemplate).collection

        self.window.main.itemList.onWidgetCreated += self.hook_widget_events
        flt.filtertext.enterCommand += self.update_filter
        self.KEEPALIVE = self

    def update_filter(self, *args, **kwargs):
        sender = kwargs['sender']
        try:
            l_string = "lambda x : x %s"
            filter_exp = eval((l_string % sender.text))

            self.collection.update_filter(filter_exp)
        except:
            self.collection.update_filter(None)

    def do_delete(self, *args, **kwargs):
        template = kwargs['sender'].tag
        original = template.tag
        name_field = template.filler.name_field
        obj = name_field.object
        cmds.delete(obj)
        self.collection.remove(original)

    def hook_widget_events(self, *args, **kwargs):
        print "I HOOKED", args, kwargs
        kwargs['item'].events['request_delete'] += self.do_delete

    def show(self):
        self.window.show()


def run():
    """
    Example:
    import mGui.examples.boundCollection as boundCollection
    win = boundCollection.run()
    """
    test = None
    try:
        test = BoundCollectionWindow([])
        test.show()
        test.collection.add(*cmds.ls(type='transform'))
    except:
        import traceback
        print traceback.format_exc()
    return test
