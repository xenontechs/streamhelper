"""all the things related to automatically populating the source application based on running processes"""
import wmi
import os
import src.datastore as data

# TODO: get path from config file
gameFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "games.txt")


def setGameSource():
    """set the game/audio source of OBS sources
    based on running apps and an allow-list"""
    errortext = ""
    # get process list
    # get game list
    # get sources list
    # match lists
    return errortext


def getProcessList():
    """get a list of processes"""
    x = wmi.WMI()
    y = []
    for process in x.Win32_Process():
        y.append(process.Name)
    return y


def getGameList():
    """get all games from file"""
    y = []
    with open(gameFilePath, "r") as f:
        for line in f:
            y.append(line.strip())
    return y


def getExclusionsFromConfig():
    """get all exclusions from config file"""
    y = []
    # TODO: define how the list should look in .ini, then do this thing here
    return y
