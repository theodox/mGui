__author__ = 'bobwhite'

"""
This example shows how to create a mGui window with menus and submenus using the new mGui 2.1 submenu syntax
"""

from mGui import gui


def food_selected(*_, **kwargs):
    print "order " + kwargs['sender'].label


def pizza_selected(*_, **kwargs):
    pizza = kwargs['sender'].parent
    toppings = [i.label for i in pizza.controls if i.checkBox]
    print "order pizza " + (" and ".join(toppings))


def checkbox_selected(*_, **kwargs):
    print "checkbox is ", kwargs['sender'].checkBox


def radio_selected(*_, **kwargs):
    print 'delivery:', kwargs['sender'].label
    kwargs['sender'].parent.label = "Delivery: " + kwargs['sender'].label


# the use of tag here acts as a keepalive, so the functions don't get garbage collected
# this is a useful alternative to classes  for simple cases
with gui.Window(menuBar=True, tag=(food_selected, pizza_selected, checkbox_selected, radio_selected)) as test_window:
    with gui.Menu(label='TestMenu') as food_menu:
        # conventional menu items
        for v in ('Hot Dog', 'Hamburger'):
            item = gui.MenuItem(label=v)
            item.command += food_selected

        # a submenu
        with gui.SubMenu(label='Pizza') as sm:
            for v in ('Pepperoni', 'Sausage', 'Pineapples'):
                item = gui.CheckBoxMenuItem(label=v)
                item.command += pizza_selected

        gui.MenuDivider()
        # radio collection submenu
        # note that unlike regular radioCollections, radioMenuItemCollections
        # don't keep track of their own selection so we track it in the
        # individual handlers instead.
        with gui.SubMenu(label='Delivery') as sm:
            with gui.RadioMenuItemCollection() as fred:
                for v in ('Eat In', 'Take Out', 'Delivery'):
                    item = gui.RadioMenuItem(label=v)
                    item.command += radio_selected

test_window.show()
