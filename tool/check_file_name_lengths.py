#! /usr/bin/env python3
"""Checks file name lengths

    Copyright (C) 2019-2023 kaoru  https://www.tetengo.org/
"""

import os
import subprocess
import sys

import list_sources

max_length: int = 80


def main(args: list[str]) -> None:
    """The main function.

    Args:
        args: Program arguments
    """
    root_path_string = str(list_sources.root())
    for path in list_sources.list_sources():
        path_string = str(path)[len(root_path_string) :]
        path_main_string, extension_string = os.path.splitext(path)
        if len(path_string) > max_length:
            candidate_path_string: str = _candidate(path_string, extension_string)
            if len(args) > 0 and args[1] == "git_mv":
                _git_mv(root_path_string, path_string, candidate_path_string)
            else:
                _report_too_long(path_string, candidate_path_string)
        elif len(path_string) < max_length and path_main_string.endswith("X"):
            _report_too_short(path_string)


def _candidate(path_string: str, extension_string: str) -> str:
    return (
        os.path.splitext(path_string)[0][: max_length - len(extension_string) - 1]
        + "X"
        + extension_string
    )


def _git_mv(
    root_path_string: str, current_path: str, corrected_path_string: str
) -> None:
    subprocess.run(
        [
            "git",
            "mv",
            root_path_string + current_path,
            root_path_string + corrected_path_string,
        ],
        check=True,
    )


def _report_too_long(current_path: str, corrected_path_string: str) -> None:
    print(
        "Too long path ({} > {}): {}".format(
            len(current_path), max_length, current_path
        )
    )
    print("  Candidate: {}".format(corrected_path_string))


def _report_too_short(current_path: str) -> None:
    print(
        "Too short path ({} < {}): {}".format(
            len(current_path), max_length, current_path
        )
    )


if __name__ == "__main__":
    main(sys.argv[1:])
