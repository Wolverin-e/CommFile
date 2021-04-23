from __future__ import print_function, absolute_import, division
from collections import defaultdict
from errno import ENOENT
from stat import S_IFREG
from time import time
from fuse import FuseOSError, Operations, LoggingMixIn

from .mailing import send_msg


class MailFS(LoggingMixIn, Operations):

    def __init__(self):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()

        self.files['/'] = dict(
            st_mode=(S_IFREG | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_size=len("%s\n"%0)
        )

    def getattr(self, path, fh=None):
        print(path)
        if path not in self.files:
            raise FuseOSError(ENOENT)

        return self.files[path]

    def read(self, path, size, offset, fh):
        encoded = lambda x: ('%s\n' % x).encode('utf-8')
        if path == "/":
            return encoded(1)

        raise RuntimeError('unexpected path: %r' % path)

    def write(self, path, data, offset, fh):
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])
        return len(data)

    def release(self, path, fh):

        msg = self.data[path].decode("utf-8")

        send_msg(msg)

        self.data.clear()

        return super().release(path, fh)

    # Disable unused operations
    access = None
    flush = None
    getxattr = None
    listxattr = None
    open = None
    opendir = None
    releasedir = None
    statfs = None
