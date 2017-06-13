#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    import paver.tasks
except ImportError:
    from os.path import exists
    if exists("paver-minilib.zip"):
        import sys
        sys.path.insert(0, "paver-minilib.zip")
    import paver.tasks

import sys

paver.tasks.main(['setup_options'] + sys.argv[1:])
