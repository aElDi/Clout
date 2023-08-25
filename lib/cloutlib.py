import importlib
import os
import logging
import enum

modules = []

class CODES(enum.IntEnum):
    GOOD = 0
    FOUND = 1
    NO_REQ = 3
    NO_FILE = 4
    INTERNAL_ERROR = 5


def load_modules(d):
    logging.info('Scanning modules...')
    for ent in os.scandir(d):
        if ent.name.endswith('.py') and ent.name != '__scanner__.py':
            name = ent.name.split('.')[0]
            lib = importlib.import_module('modules.' + name)
            clt_std = [i for i in dir(lib) if i[:4] == 'CLT_']
            for cls in clt_std:
                modules.append(getattr(lib, cls)())
    logging.info(f'Loaded {len(modules)} module(s)')


def init_modules():
    logging.info("Initialization modules...")
    for m in modules:
        logging.info(f"Initialization module {m.name}...")
        res = m.init()
        if res['code'] == CODES.NO_REQ:
            logging.error(f"FAILED! No requirements for module {m.name}")
            return 1
        elif res['code'] == CODES.INTERNAL_ERROR:
            logging.error(f"FAILED! Internal error for module {m.name}")
            return 1
        elif res['code'] == CODES.GOOD:
            logging.info(f"Inited module {m.name}")
    return 0


def scan_file(filepath):
    for m in modules:
        m.scan_file(filepath)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, filename="log.log")
    load_modules('./modules')
    if init_modules():
        print('NO')

    pass
