import os.path

from . import __scanner__
import numpy as np

import hashlib

class CLT_Md5Scanner(__scanner__.Scanner):

    CACHE_FILE = "./cache.ch2"
    cache = None

    name = "MD5 Scanner"
    author = "a3lDi"
    desc = "MD5 Scanner for cache.ch2 file, with count of hashes: "
    required = [CACHE_FILE]

    def init(self):
        try:
            if not (self.check_reqs()):
                return {"code": self.CODES.NO_REQ}
            l = os.path.getsize(self.CACHE_FILE) // 16
            self.cache = np.fromfile(self.CACHE_FILE, dtype=np.int8).reshape(l,16)
            self.desc += str(l)
            return {"code": self.CODES.GOOD}
        except Exception:
            return {'code': self.CODES.INTERNAL_ERROR}


    def scan_file(self, filepath):
        h = hashlib.md5(open(filepath, 'rb').read())
        print(h)
        pass
