import maya.cmds as cmds
from mGui import gui, forms, lists, observable
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
        with forms.HorizontalExpandForm( tag=item) as root:
            delete_button = gui.IconTextButton(width=48, style='iconOnly', image='deleteShader')
            name_field = gui.NameField(object=item, width = 256)
            gui.Separator(style = 'none', width = 16)

            tx = gui.FloatField(width = 48, pre = 2)
            ty = gui.FloatField(width = 48, pre = 2)
            tz = gui.FloatField(width = 48, pre = 2)
            gui.Separator(style = 'none', width = 16)

            # using 'connectControl' here is a good alternative to binding
            cmds.connectControl(tx, item + ".tx")
            cmds.connectControl(ty, item + ".ty")
            cmds.connectControl(tz, item + ".tz")

        delete_button.tag = root
        return lists.Templated(item, root, request_delete=delete_button.command)


class BoundCollectionWindow(object):
    KEEPALIVE = None
    # this is handy for the example, you don't want to do it this way
    # if you really need multiple windows: the single Keepalive will
    # only support the latest one at a time...

    def __init__(self, collection):

        # this is the collection of stuff to manage
        self.collection = observable.ViewCollection(*collection)

        with gui.BindingWindow(title='bound collection example', height = 512, width=512) as self.window:
            with forms.VerticalExpandForm(margin = (16,), spacing = (8,12)) as main:
                gui.Text(label="Type a filter and [enter] to limit the list")

                with forms.HorizontalExpandForm(width = 512, ) as flt:
                    filter_text = gui.TextField(width=400)
                    filter_text.alwaysInvokeEnterCommandOnReturn = True
                    gui.Separator(horizontal=False, style='none', width=4)
                    with forms.HorizontalExpandForm( width=100) as display:
                        gui.Text("showing")
                        shown = gui.Text(width = 24)
                        shown.bind.label < bind() < self.collection.bind.viewCount
                        gui.Text(label='/')
                        total = gui.Text(width=24)
                        total.bind.label < bind() < self.collection.bind.count

                with forms.HorizontalExpandForm() as labels:
                    gui.Separator(style=None, width=48)
                    gui.Text ("item", width = 256, align='center')
                    gui.Separator(style=None, width=16)
                    gui.Text("translation", width = 128, align = 'center')
                    gui.Separator(style=None, width=16)

                item_list = lists.VerticalList(itemTemplate=ExampleTemplate)
                self.collection > bind() > item_list.collection

        item_list.onWidgetCreated += self.hook_widget_events
        filter_text.enterCommand += self.update_filter
        self.KEEPALIVE = self

    def update_filter(self, *args, **kwargs):
        sender = kwargs['sender']
        def filter_exp(x):
            return sender.text in x
        if sender.text:
            self.collection.update_filter(filter_exp)
        else:
            self.collection.update_filter(None)
        cmds.setFocus(self.window.main.flt.filter_text)

    def do_delete(self, *args, **kwargs):
        template = kwargs['sender'].tag
        original = template.tag
        name_field = template.filler.name_field
        obj = name_field.object
        cmds.delete(obj)
        self.collection.remove(original)

    def hook_widget_events(self, *args, **kwargs):
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
    except Exception:
        import traceback
        print traceback.format_exc()
    return test

if __name__ == '__main__':
    win = run()
