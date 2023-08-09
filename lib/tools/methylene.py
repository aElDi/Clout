import numpy as np
import os.path

class Methylene_ReWriter:

    data = None

    def read(self, filename):
        s = open(filename).readlines()
        l = len(s)
        arr = bytearray()
        for i in s:
            arr += bytearray.fromhex(i)
        self.data = np.frombuffer(arr, dtype=np.int8)
        print(self.data)

    def write(self, filename):
        with open(filename, 'wb') as s:
            self.data.tofile(s)
class Methylene_Reader:

    data = None

    def read(self, filename):
        with open(filename, 'rb') as f:
            self.data = np.fromfile(f, dtype=np.int8).reshape(32, os.path.getsize(filename)//32)
        print(self.data)

if __name__ == '__main__':
    p = Methylene_ReWriter()

    r = Methylene_Reader()

    r.read('cache.ch2')
