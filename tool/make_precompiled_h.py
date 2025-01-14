#! /usr/bin/env python
"""Makes precompiled.h
    
    Copyright (C) 2019-2025 kaoru  https://www.tetengo.org/
"""

import re
from pathlib import Path

import list_sources


def main() -> None:
    """The main function."""
    libc_includes, libcpp_includes, boost_includes = _list_includes()
    precompiled_h: str = _make_precompiled_h(
        libc_includes, libcpp_includes, boost_includes
    )
    _save_to_file(precompiled_h, _precompiled_h_path())


def _list_includes() -> tuple[set[str], set[str], set[str]]:
    libc_includes = set()
    libcpp_includes = set()
    boost_includes = set()
    for path in list_sources.list_sources():
        (
            libc_includes_per_file,
            libcpp_includes_per_file,
            boost_includes_per_file,
        ) = _list_includes_per_file(path)
        libc_includes |= libc_includes_per_file
        libcpp_includes |= libcpp_includes_per_file
        boost_includes |= boost_includes_per_file
    return (libc_includes, libcpp_includes, boost_includes)


def _list_includes_per_file(path: Path) -> tuple[set[str], set[str], set[str]]:
    libc_includes = set()
    libcpp_includes = set()
    boost_includes = set()
    with path.open() as stream:
        for line in stream:
            line = line.rstrip("\r\n")
            libc_match = re.search("^#\s*include\s+<([46a-z]+\.h)>", line)
            if libc_match and not _is_exception_include(line):
                libc_includes.add(libc_match.group(1))
                continue
            libcpp_match = re.search("^#\s*include\s+<([a-z_/]+)>", line)
            if libcpp_match and not _is_exception_include(line):
                libcpp_includes.add(libcpp_match.group(1))
                continue
            boost_match = re.search("^#\s*include\s+<(boost\/[^>]+)>", line)
            if boost_match and not _is_exception_include(line):
                boost_includes.add(boost_match.group(1))
                continue
    return (libc_includes, libcpp_includes, boost_includes)


def _is_exception_include(line: str) -> bool:
    if line == "#include <errno.h>":
        return True
    elif line == "#include <iconv.h>":
        return True
    elif re.match("^#\s*include\s+<boost\/test\/", line):
        return True
    else:
        return False


def _make_precompiled_h(
    libc_includes: set[str], libcpp_includes: set[str], boost_includes: set[str]
) -> str:
    result: str = ""
    result += (
        """
/*! \\file
    \\brief The precompiled header.

    This file is generated by kogyan/tool/make_precompiled_h.py.

    Copyright (C) 2019-2025 kaoru  https://www.tetengo.org/
*/

#if !defined(PRECOMPILED_H)
#define PRECOMPILED_H
""".strip()
        + "\n\n\n"
    )
    result += "// C Standard Library\n"
    for h in sorted(libc_includes):
        result += "#include <" + h + ">\n"
    result += "\n"
    result += "#if defined(__cplusplus)\n\n"
    result += "// C++ Standard Library\n"
    for h in sorted(libcpp_includes):
        result += "#include <" + h + ">\n"
    result += "\n"
    result += "// Boost\n"
    for h in sorted(boost_includes):
        result += "#include <" + h + ">\n"
    result += "\n"
    result += "#endif\n"
    result += (
        "\n\n"
        + """
// Platform Dependent
#if defined(_MSC_VER)
#if defined(__cplusplus)
#define NOMINMAX
#include <Windows.h>
#endif
#else
#include <errno.h>
#include <iconv.h>
#endif


#endif
""".strip()
        + "\n"
    )
    return result


def _precompiled_h_path() -> Path:
    root_path: Path = Path(__file__).parent.parent.parent
    return root_path / "precompiled" / "precompiled.h"


def _save_to_file(content: str, path: Path) -> None:
    with path.open(mode="w", newline="\r\n") as stream:
        stream.write(content)


if __name__ == "__main__":
    main()
