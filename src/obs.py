"""obs websocket functions
using https://github.com/Elektordi/obs-websocket-py"""
from obswebsocket import obsws, requests
import src.datastore as data

ws = {}


def prepare():
    """sets up the ws class, to be called at the correct time. could probably be an object or something"""
    obsSettings = data.config["obs-settings"]
    global ws
    ws = obsws(
        obsSettings["websocketAddress"],
        obsSettings["websocketPort"],
        obsSettings["websocketPassword"],
        legacy=True,
    )


def selectSceneByName(sceneName):
    """selects a scene based on the name

    :param sceneName: the name of the scene
    :type sceneName: str
    :return: error text from OBS websocket
    :rtype: str?
    """
    ws.connect()
    # print(ws.call(requests.SetCurrentProgramScene(sceneName=sceneName)))
    error = ws.call(requests.SetCurrentScene(**{"scene-name": sceneName}))
    ws.disconnect()
    return error


def setSceneItemEnabled(sceneName, sceneItemId, sceneItemEnabled):
    ws.connect()
    ws.call(
        requests.SetSceneItemEnabled(
            sceneName=sceneName,
            sceneItemId=sceneItemId,
            sceneItemEnabled=sceneItemEnabled,
        )
    )
    ws.disconnect()
