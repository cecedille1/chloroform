#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys
import argparse

import logging

logger = logging.getLogger('chloroform')


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
    )
    return parser


class Main(object):
    def __init__(self, parser):
        self.parser = parser

    def setup_logging(self, verbose):
        logger = logging.getLogger()
        formatter = logging.Formatter(u'%(levelname)8s %(name)16s: %(message)s')

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG)

        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        logger.addHandler(sh)

    def __call__(self, args):
        options = self.parser.parse_args(args)
        value = self.run(options)

        if isinstance(value, bool):
            value = int(not value)
        elif value is None:
            value = 0

        sys.exit(value)

    def run(self, options):
        return True


main = Main(get_parser())


if __name__ == '__main__':
    main()
