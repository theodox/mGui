import os
import json
from mGui import shelf_loader

if __name__ == '__main__':
    example_file = os.path.join(os.path.dirname(__file__), 'shelf_example.json')
    shelf_loader.load_shelf(json.load(open(example_file)))
    