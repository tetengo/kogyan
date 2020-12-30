#! /usr/bin/env python3
# Lists the source files
# Copyright (C) 2019-2021 kaoru  https://www.tetengo.org/

import os.path
from pathlib import Path


directories = ['library', 'product', 'sample', 'utility']
extensions = ['h', 'hpp', 'c', 'cpp']

def list_iter(root_path, directory, extension):
    path = root_path / directory
    return [p for p in path.glob('**/*.' + extension)]

def root():
    return Path(__file__).parent.parent.parent

def list():
    root_path= root()
    files = []
    for d in directories:
        if os.path.exists(root_path / d):
            for e in extensions:
                for f in list_iter(root_path, d, e):
                    files.append(f)
    return files
