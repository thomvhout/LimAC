import os
import fnmatch


def searchFiles(dir, name):
    files = []
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, name):
            files.append(file)
    return files


def getpwd():
    return __file__[:__file__.rindex('/')+1]
