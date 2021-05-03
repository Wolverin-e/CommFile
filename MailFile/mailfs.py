from __future__ import print_function, absolute_import, division
from collections import defaultdict
from errno import ENOENT
import logging
from stat import S_IFDIR, S_IFREG
from time import time
from fuse import FuseOSError, Operations, LoggingMixIn, fuse_get_context
from pathlib import Path

from .mailing import send_msg
from .readmail import receive


logger = logging.getLogger(__name__)


class MailFS(LoggingMixIn, Operations):

    def __init__(self):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        self.flag = False
        self.msg = (receive()).encode('utf-8')
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

        self.files['/recent.unread'] = dict(
            st_mode=(S_IFREG | 0o755),
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
            st_uid=uid,
            st_gid=gid,
            st_pid=pid,
            st_size = len(self.msg)
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
        # # return self.data[path][offset:offset+size]
        # if self.flag == False:
        #     self.msg = receive().replace('\r', '\n')
        #     self.msg = self.msg.encode('utf-8')
        #     self.flag = True
        
        return self.msg[offset:offset+size]

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

        logger.debug(path)

        if(path.suffix == ".unread"):
            self.msg = (receive()).encode('utf-8')
            self.files[path]['st_size'] = len(self.msg)
        else:
            if(path.suffix == ".mail"):
                msg = self.data[path.__str__()].decode("utf-8")
                logging.debug("Suffix mail: %s", self.data)
                send_msg(
                    msg_body=msg,
                    to=path.parent.name,
                    subject=path.stem
                )
            elif(path.suffix == ".attachment"):
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
    statfs = None
