import os
import subprocess

from . import utils

isRunning = False

serverPath = os.getcwd() + "/" + "./content/server/"
serverExec = serverPath + "acServer"

process = None

# 1. 1 Layout => UI/...png
# 2. More layout => UI/LAYOUT/...png


def getTracks():
    #models = [[i*j for j in range(maxModels)] for i in range(maxTracks)]
    models = []

    count = 0
    trackPath = serverPath + "content/tracks/"
    for dir in os.listdir(trackPath):
        # Track with no subdir in [Track]/ui/ has no layouts
        uiImgs = utils.searchFiles(trackPath + dir + "/ui", "*.png")
        if (len(uiImgs) > 0):
            # Track has one layout
            models.append([dir])
        else:
            # Track has multiple layouts
            # TODO fix non-dirs being included. => e.g.: monza66/ui/people_stand.dds
            subdir = os.listdir(trackPath + dir + "/ui")
            nested_list = []
            nested_list.append(dir)
            for layout in subdir:
                nested_list.append(layout)
            models.append(nested_list)
        count += 1

    print("Found {} tracks/layouts:".format(len(models)))
    for layout in models:
        print(layout)
    return models
