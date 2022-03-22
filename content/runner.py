import os
import subprocess
import fnmatch

isRunning = False

serverPath = os.getcwd() + "/" + "./server/"
serverExec = serverPath + "acServer"


def searchFiles(dir, name):
    files = []
    for file in os.listdir(dir):
        if fnmatch.fnmatch(file, name):
            files.append(file)
    return files


class acServer:
    process = None
    isRunning = False

    def __init__(self, start):
        if start:
            self.isRunning = True
            self.start()

    def start(self):
        if self.isRunning:
            return "Server already running!"
        else:
            print("Starting Server!")
            self.isRunning = True
            self.process = subprocess.Popen(serverExec, cwd=serverPath)
        return "Starting Server!"

    def die(self):
        if self.isRunning:
            print("Stopping server!")
            self.isRunning = False
            subprocess.Popen.terminate(self.process)
            return "Stopping server!"
        else:
            return "Server already stopped!"
        return

    def changeTrack(self, request: str):
        args = request.split(';')
        # No select item has been chosen
        if args[1] != "None":
            track = args[1]
            layoutName = ""
            models = []
            models = searchFiles(
                f"{serverPath}/content/tracks/{track}", "models_*.ini")
            print(f"    b4: {models}")
            models.sort()
            print(models)
            if len(models) == 0:
                # Track without layout
                layoutName = ""
            else:
                # Track with layout
                layoutIndex = 0
                if args[2] == "None" or args[2] == "default":
                    layoutIndex = 0
                elif int(args[2]) > len(models):
                    layoutIndex = 0
                else:
                    layoutIndex = int(args[2])-1
                layoutName = models[layoutIndex]
                layoutName = layoutName.split("_", 1)[1]
                layoutName = layoutName.split(".")[0]
            trackString = f"TRACK={track}"
            layoutString = f"CONFIG_TRACK={layoutName}"
            print(track)
            print(layoutName)
            self.writeConfig(trackString, layoutString)
        return

    def writeConfig(self, trackString, layoutString):
        trackIndex = 5
        layoutIndex = 4
        # Read all
        with open(f"{serverPath}/cfg/server_cfg.ini", 'r') as f:
            get_all = f.readlines()
        print(get_all)
        with open(f"{serverPath}/cfg/server_cfg.ini", 'w') as f:
            for i, line in enumerate(get_all, 1):
                if i == layoutIndex:
                    f.writelines(layoutString+"\n")
                elif i == trackIndex:
                    f.writelines(trackString+"\n")
                else:
                    f.writelines(line)

#   TODO run telnet on AC server: `telnet 127.0.0.1 8081`


def verifyRunning():
    #    process = subprocess.Popen(serverExec, cwd=serverPath)
    return
