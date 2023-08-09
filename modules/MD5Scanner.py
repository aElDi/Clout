from modules.scanner import Scanner
import mmap
import hashlib
import os

class MemoryMappedFileCache:
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("Cache file not found.")
        self._file = open(path)
        self._data = mmap.mmap(self._file.fileno(),
                               length=0, access=mmap.ACCESS_READ)

    def close(self):
        self._data.close()
        self._file.close()


class MD5Scanner(Scanner):

    name = 'MD5 scanner'
    desc = 'Scans files for known viruses in the hash database'

    CACHE_FILE = "./cache.chs"
    CHUNK_SIZE = 4096
    cache = MemoryMappedFileCache(CACHE_FILE)

    def compute_md5(self, filepath):
        with open(filepath, "rb") as f:
            md5 = hashlib.md5()
            while True:
                chunk = f.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                md5.update(chunk)
        return md5.hexdigest()

    def scan_file(self, file_path):
        try:
            hash_value = self.compute_md5(file_path)
            if self.cache._data.find(hash_value.encode('ascii')):
                return [True, hash_value]
            # if self.cache.__contains__(hash_value):
                # return [True, hash_value]
            return [False]
        except:
            return [False]
