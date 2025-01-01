#! /usr/bin/env python
"""Lists the source files

    Copyright (C) 2019-2025 kaoru  https://www.tetengo.org/
"""

import os.path
from pathlib import Path

directories: list[str] = ["library", "product", "sample", "utility"]
extensions: list[str] = ["h", "hpp", "c", "cpp"]


def _list_sources_iter(root_path: Path, directory: str, extension: str) -> list[Path]:
    path: Path = root_path / directory
    return [p for p in path.glob("**/*." + extension)]


def root() -> Path:
    """Returns the repository root directory.

    Returns:
        The repository root directory.
    """
    return Path(__file__).parent.parent.parent


def list_sources() -> list[Path]:
    """Lists the source files.

    Returns:
        The source files.
    """
    root_path: Path = root()
    files: list[Path] = []
    for d in directories:
        if os.path.exists(root_path / d):
            for e in extensions:
                for f in _list_sources_iter(root_path, d, e):
                    files.append(f)
    return files
