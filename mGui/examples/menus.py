__author__ = 'bobwhite'

"""
This example shows how to create a mGui window with menus and submenus using the new mGui 2.1 submenu syntax
"""

from mGui import gui


def food_selected(*_, **kwargs):
    print "order " + kwargs['sender'].label


def pizza_selected(*_, **kwargs):
    pizza = kwargs['sender'].parent

    toppings = [i.label for i in pizza.controls if isinstance(i, gui.CheckBoxMenuItem) and  i.checkBox]
    print "order pizza " + (" and ".join(toppings))


def radio_selected(*_, **kwargs):
    print 'delivery:', kwargs['sender'].label
    kwargs['sender'].parent.label = "Delivery: " + kwargs['sender'].label


# the use of tag here acts as a keepalive, so the functions don't get garbage collected
# this is a useful alternative to classes  for simple cases
with gui.Window(menuBar=True, tag=(food_selected, pizza_selected, radio_selected)) as test_window:
    with gui.Menu(label='TestMenu') as food_menu:

        # conventional menu items
        hotdog = gui.MenuItem(label = 'Hot Dog')
        burger = gui.MenuItem(label = 'Burger')
        taco = gui.MenuItem(label = 'Taco')
        for each in (hotdog, burger, taco):
            each.command += food_selected

        # a submenu
        with gui.SubMenu(label='Pizza') as sm:
            pepperoni = gui.CheckBoxMenuItem(label='Pepperoni')
            sausage = gui.CheckBoxMenuItem(label='Sausage')
            pineapples = gui.CheckBoxMenuItem(label='Pineapples')
            for each in (pepperoni, sausage, pineapples):
                each.command += pizza_selected


        gui.MenuDivider()
        # radio collection submenu
        # note that unlike regular radioCollections, radioMenuItemCollections
        # don't keep track of their own selection so we track it in the
        # individual handlers instead.
        with gui.SubMenu(label='Delivery') as sm:
            with gui.RadioMenuItemCollection() as radio:
                eatin = gui.RadioMenuItem('Eat In')
                takeout = gui.RadioMenuItem('Take Out')
                delivery = gui.RadioMenuItem('Delivery')
                for each in (eatin, takeout, delivery):
                    each.command += radio_selected

test_window.show()
