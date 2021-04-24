from __future__ import print_function, absolute_import, division
from collections import defaultdict
from errno import ENOENT
import logging
from stat import S_IFDIR, S_IFREG
from time import time
from fuse import FuseOSError, Operations, LoggingMixIn, fuse_get_context
from pathlib import Path

from .mailing import send_msg


logger = logging.getLogger(__name__)


class MailFS(LoggingMixIn, Operations):

    def __init__(self):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()
        uid, gid, pid = fuse_get_context()

        self.files['/'] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_uid=uid,
            st_gid=gid,
            st_pid=pid,
            st_nlink=2
        )

    def getattr(self, path, fh=None):
        super().__getattribute__
        if path not in self.files:
            raise FuseOSError(ENOENT)

        return self.files[path]

    def mkdir(self, path, mode):

        now = time()
        uid, gid, pid = fuse_get_context()

        self.files[path] = dict(
            st_mode=(S_IFDIR | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_uid=uid,
            st_gid=gid,
            st_pid=pid,
            st_nlink=2
        )

        logging.debug(self.files)

    def read(self, path, size, offset, fh):
        encoded = lambda x: ('%s\n' % x).encode('utf-8')  # noqa: E731
        if path == "/":
            return encoded(1)

        raise RuntimeError('unexpected path: %r' % path)

    def readdir(self, path, fh):
        files = ['.', '..']
        for k in self.files:
            if k != '/':
                files.append((Path(k).name, self.getattr(k), 0))

        return files

    def create(self, path, mode, fi=None):

        now = time()
        uid, gid, pid = fuse_get_context()

        self.files[path] = dict(
            st_mode=(mode or S_IFREG | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_uid=uid,
            st_gid=gid,
            st_pid=pid,
            st_size=0
        )

        return 0

    def write(self, path, data, offset, fh):
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])
        return len(data)

    def release(self, path, fh):

        path = Path(path)

        if(path.suffix == ".mail"):
            msg = self.data[path.__str__()].decode("utf-8")
            logging.debug("Suffix mail: %s", self.data)
            send_msg(
                msg_body=msg,
                to=path.parent.name,
                subject=path.stem
            )
        else:
            attachment = self.data[path.__str__()].decode("utf-8")
            send_msg(
                to=path.parent.name,
                subject=path.name,
                attach=attachment,
                filename=path.name
            )

        self.data.clear()

    # Disable unused operations
    getxattr = None
    listxattr = None
    open = None
    statfs = None
