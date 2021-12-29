# Automake Settings
# Copyright (C) 2019-2022 kaoru  https://www.tetengo.org/

SUBDIRS = \
    tool \
    vsprops

EXTRA_DIST = \
    .clang-format \
    COPYING \
    README.md


mypy:
	${MAKE} -C tool mypy

format:
	${MAKE} -C tool format
