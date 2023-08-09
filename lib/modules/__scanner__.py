import os.path
import enum

class Scanner:
    name = ""
    author = ""
    desc = ""

    required = []

    class CODES(enum.IntEnum):
        GOOD = 0
        FOUND = 1
        NO_REQ = 3
        NO_FILE = 4
        INTERNAL_ERROR = 5
        CODE10 = 10

    def check_reqs(self):
        for i in self.required:
            if not (os.path.isfile(i)):
                return 0
        return 1

    def init(self):
        if not (self.check_reqs()):
            return {"code": self.CODES.NO_REQ}
        return {"code": self.CODES.GOOD}

    def scan_file(self, filepath):
        pass