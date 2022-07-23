#! /usr/bin/env python3
"""Lists the source files

    Copyright (C) 2019-2022 kaoru  https://www.tetengo.org/
"""

import os.path
import pathlib

directories: list[str] = ["library", "product", "sample", "utility"]
extensions: list[str] = ["h", "hpp", "c", "cpp"]


def _list_sources_iter(
    root_path: pathlib.Path, directory: str, extension: str
) -> list[pathlib.Path]:
    path: pathlib.Path = root_path / directory
    return [p for p in path.glob("**/*." + extension)]


def root() -> pathlib.Path:
    """Returns the repository root directory.

    Returns:
        The repository root directory.
    """
    return pathlib.Path(__file__).parent.parent.parent


def list_sources() -> list[pathlib.Path]:
    """Lists the source files.

    Returns:
        The source files.
    """
    root_path: pathlib.Path = root()
    files: list[pathlib.Path] = []
    for d in directories:
        if os.path.exists(root_path / d):
            for e in extensions:
                for f in _list_sources_iter(root_path, d, e):
                    files.append(f)
    return files
