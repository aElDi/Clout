import hashlib
import os
import configparser
import requests
import mmap

def filescan(file, mm_cache):
        filehash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if mm_cache.find(filehash.encode()) != -1:
            print('virus detected - ' + file + ' hash: ' + filehash)

def pathscan(directory, mm_cache):
    try:
        for file in os.scandir(directory):
            if file.is_file():
                filescan(file.path, mm_cache=mm_cache)
            elif file.is_dir():
                pathscan(file.path, mm_cache)
    except PermissionError:
        print('[warn] - Perm error 4 ', directory)
        pass


TOKEN = "b11f1ec7b09664a23316d3cd9bb46447fde1dbea269a397e992f8ea3389cef23"

banner = '''
  ,ad8888ba,   88                                     
 d8"'    `"8b  88                              ,d     
d8'            88                              88     
88             88   ,adPPYba,   88       88  MM88MMM  
88             88  a8"     "8a  88       88    88     
Y8,            88  8b       d8  88       88    88     
 Y8a.    .a8P  88  "8a,   ,a8"  "8a,   ,a88    88,    
  `"Y8888Y"'   88   `"YbbdP"'    `"YbbdP'Y8    "Y888 

\t\t\tby aElDi
\t\t\t\tv. 1.0
'''

usage = '''
\t[?] Select mode:

[1]-File mode
[2]-Directory mode
[3]-Disk mode

'''
print('Loading config...')

cfg = configparser.ConfigParser()

if os.path.exists('config.ini'):
    cfg.read('config.ini')

os.system('cls')

print(banner)
print(usage)

i_mode = input('You select: ')

with open(cfg['Cache']['Path'],'rb') as f_cache, mmap.mmap(f_cache.fileno(), 0, access=mmap.ACCESS_READ) as mm_cache:
    match i_mode:
        case '1':
            os.system('cls')
            filepath = input("\nEnter file path (drag&drop enabled): ")
            filescan(filepath, mm_cache=mm_cache)
        case '2':
            os.system('cls')
            dir = input("\nEnter directory path (drag&drop enabled): ")
            if os.path.exists(dir):
                pathscan(dir, mm_cache=mm_cache)
            else:
                print('\nThis path does not exist or not allow to read!')
        case '3':
            os.system('cls')
            disk = input('Enter disk letter: ') + ':\\'
            if os.path.exists(disk):
                pathscan(disk, mm_cache=mm_cache)
            else:
                print('\nThis path does not exist or not allow to read!')


