import os
import gzip
import bz2
import psutil


def openfilepaths():
    '''
    `openfilepaths` intends for the `open` to look less like a verb than it would in `open_filepaths`
    '''
    for process in psutil.get_process_list():
        try:
            for openfile in process.get_open_files():
                yield openfile.path
        except psutil.AccessDenied:
            pass


def open_with_autodecompress(filepath):
    '''Create a file object for any filepath,
    1. *gz -> GzipFile(...)
    2. *bz2 -> BZ2File(...)
    3. else -> open(...)
    '''
    if filepath.endswith('gz'):
        # gzip.GzipFile mode defaults to 'rb'
        return gzip.GzipFile(filepath)
    elif filepath.endswith('bz2'):
        # bz2.BZ2File mode defaults to 'r'
        return bz2.BZ2File(filepath)
    else:
        return open(filepath)


def walk(paths):
    '''
    List all files in all given paths, recursing into subdirectories.

    Paths can be files or directories or both.

    Does not yield directories, only files.
    '''
    for path in paths:
        if os.path.isdir(path):
            for child_path in walk(os.path.join(path, child) for child in os.listdir(path)):
                yield child_path
        else:
            yield path
