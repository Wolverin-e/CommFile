from sys import argv, exit
import logging
from fuse import FUSE

from .mailfs import MailFS

def main():

    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    logging.basicConfig(level=logging.DEBUG)
    FUSE(MailFS(), argv[1], foreground=True)
