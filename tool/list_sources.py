#! /usr/bin/env python3
"""Lists the source files

    Copyright (C) 2019-2021 kaoru  https://www.tetengo.org/
"""

import os.path
import pathlib
from typing import List

directories: List[str] = ["library", "product", "sample", "utility"]
extensions: List[str] = ["h", "hpp", "c", "cpp"]


def _list_iter(
    root_path: pathlib.Path, directory: str, extension: str
) -> List[pathlib.Path]:
    path: pathlib.Path = root_path / directory
    return [p for p in path.glob("**/*." + extension)]


def root() -> pathlib.Path:
    """Returns the repository root directory.

    Returns:
        pathlib.Path: The repository root directory.
    """
    return pathlib.Path(__file__).parent.parent.parent


def list() -> List[pathlib.Path]:
    """Lists the source files.

    Returns:
        list[pathlib.Path]: The source files.
    """
    root_path: pathlib.Path = root()
    files: List[pathlib.Path] = []
    for d in directories:
        if os.path.exists(root_path / d):
            for e in extensions:
                for f in _list_iter(root_path, d, e):
                    files.append(f)
    return files
