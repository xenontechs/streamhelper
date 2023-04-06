"""obs websocket functions
using https://github.com/Elektordi/obs-websocket-py"""
from obswebsocket import obsws, requests
import src.datastore as data

ws = {}


def prepare():
    obsSettings = data.config['obs-settings']
    global ws
    ws = obsws(obsSettings['websocketAddress'], obsSettings['websocketPort'], obsSettings['websocketPassword'], legacy=True)


def selectSceneByName(sceneName):
    ws.connect()
    # print(ws.call(requests.SetCurrentProgramScene(sceneName=sceneName)))
    error = ws.call(requests.SetCurrentScene(**{'scene-name': sceneName}))
    ws.disconnect()
    return error


def setSceneItemEnabled(sceneName, sceneItemId, sceneItemEnabled):
    ws.connect()
    ws.call(requests.SetSceneItemEnabled(sceneName=sceneName, sceneItemId=sceneItemId, sceneItemEnabled=sceneItemEnabled))
    ws.disconnect()
