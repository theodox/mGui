import maya.cmds as cmds
import mGui.gui as gui
import mGui.observable as observable
import mGui.stylesheets as stylesheets
import mGui.lists as lists
import mGui.forms as forms
import mGui.styles as st

import mGui.bindings as bindings
reload(bindings)
reload(lists)

class TestWidget(lists.ItemTemplate):
    def widget(self, item):
        with forms.HorizontalExpandForm('tmp_%i' % id(item), parent=self.Parent, width=250, backgroundColor=(.7, .2, .2)) as root:
                gui.IconTextButton('delete', style='iconAndTextHorizontal', image='delete', tag=item)
                with forms.VerticalForm('names'):
                    fred = gui.NameField(0, object=item, width=250)
                with forms.VerticalForm('xform'):
                    gui.AttrFieldGrp('t', label='translate', attribute=item + ".t")

        return {'widget':root, 'delete':root.delete.command}


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
                        gui.Text('shown') + "label" << self.Collection + "ViewCount"
                        gui.Text(None, '/')
                        gui.Text('total') + "label" << self.Collection + "Count"

                self.Collection >> lists.VerticalList('itemList', itemTemplate=TestWidget).Collection

        self.Window.main.itemList.NewWidget += self.request_delete
        flt.filtertext.enterCommand += self.update_filter

    def update_filter(self, *args, **kwargs):
        sender = kwargs['sender']
        try:
            l_string = "lambda x : x %s"
            filter_exp = eval((l_string % sender.text))

            self.Collection.update_filter(filter_exp)
        except:
            self.Collection.update_filter(None)


    def request_delete(*args, **kwargs):
        print args
        print kwargs

    def show(self):
        self.Window.show()

test = BoundCollectionWindow([])
test.show()
test.Collection.add('pCylinder1')
