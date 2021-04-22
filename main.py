#!/usr/bin/env python

from sys import argv, exit
import logging
from fuse import FUSE

from mailfs import MailFS

if __name__ == '__main__':

    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    logging.basicConfig(level=logging.DEBUG)
    fuse = FUSE(MailFS(), argv[1], foreground=True)
