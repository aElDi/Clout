import mmap, os, configparser, argparse, hashlib

CACHE = 0

def init():
    global CACHE

    cfg = configparser.ConfigParser()

    if os.path.exists('./config.ini'):
        cfg.read('./config.ini')
        with open(cfg['Cache']['Path'],'rb') as ff:
            CACHE = mmap.mmap(ff.fileno(), 0, access=mmap.ACCESS_READ)

    else:
        with open('./config.ini', 'w') as cfg_file:
            cfg_file.write('[Cache]\r\npath = ./cache.chs')
            cfg_file.close()
    

def filescan(file):
        global CACHE
        filehash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if CACHE.find(filehash.encode()) != -1:
            print('virus detected - ' + file + ' hash: ' + filehash)

def pathscan(directory):
    try:
        for file in os.scandir(directory):
            if file.is_file():
                filescan(file.path)
            elif file.is_dir():
                pathscan(file.path)
    except PermissionError:
        print('[warn] - Perm error 4 ', directory)
        pass

if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument('-f', '--file', help='file to scan', type=str, default='p')
    args.add_argument('-d', '--dir', help='directory to scan', type=str, default='p')

    arguments = args.parse_args()
    init()

    if arguments.file != 'p':
        filescan(arguments.file)
    if arguments.dir != 'p':
        pathscan(arguments.dir)

    print("Work finished. Run 'clout_cli -h' to help")