import os
import json
import urllib2

from mGui import shelf_loader, core, gui, forms

url = 'https://raw.githubusercontent.com/theodox/mGui/master/mGui/examples/shelf_example.json'

example_file = os.path.join(os.path.dirname(__file__), 'shelf_example.json')
shelf_dict = json.load(open(example_file))

def add_to_main_shelf_layout():
    shelf_loader.load_shelf(shelf_dict)


def create_floating_shelf():
    if core.MAYA_VERSION >= '2017':
        with gui.WorkspaceControl() as win:
            with forms.FillForm() as f:
                with gui.ShelfTabLayout() as shelf:
                   shelf_loader.load_shelf(shelf_dict, shelf)

def load_shelf_from_url():
    shelf_dict = json.load(urllib2.urlopen(url))
    shelf_loader.load_shelf(shelf_dict)


if __name__ == '__main__':

    # add_to_main_shelf_layout()
    # create_floating_shelf()
    load_shelf_from_url()
