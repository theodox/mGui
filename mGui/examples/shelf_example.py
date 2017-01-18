import os
import yaml
from mGui import shelf_loader

if __name__ == '__main__':
    example_file = os.path.join(os.path.dirname(__file__), 'shelf_example.yaml')
    with open(example_file, 'r') as fyle:
        shelf_loader.load_shelf(''.join(fyle.readlines()))
