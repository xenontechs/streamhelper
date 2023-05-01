"""obs websocket functions
using https://github.com/aatikturk/obsws-python"""
from __future__ import annotations
import obsws_python as obswsp
import src.datastore as data
import weakref

# pre-initialize global websocket
wsp = {}

# all scene objects will be in here
sceneObjects = []


def getScenes():
    """get a list of all scenes

    :return: all scene objects
    :rtype: list
    """
    return sceneObjects


class scene:
    def __init__(self, sceneId, sceneName) -> None:
        """initialize scene object

        :param sceneId: ID of the scene in OBS
        :type sceneId: int
        :param sceneName: name of the scene in OBS
        :type sceneName: str
        """
        global sceneObjects

        # for keeping all the sceneItems
        self.sceneItemObjects = []

        self.id = sceneId
        self.name = sceneName
        self.objectId = sceneObjects.__len__()
        sceneObjects.append(self)

    def getSceneItems(self):
        """gets you all the scene items as a list of objects

        :return: list of scene items
        :rtype: list
        """
        return self.sceneItemObjects

    def addSceneItem(self, sceneItemId, sourceName, sourceType, sceneItemEnabled):
        """adds a new sceneItem to the scene. all data should come directly from OBS websocket

        :param sceneItemId: Scene ID
        :type sceneItemId: int
        :param sourceName: name of the item
        :type sourceName: str
        :param sourceType: type of the item
        :type sourceType: str
        :param sceneItemEnabled: if it is visible or not
        :type sceneItemEnabled: bool
        """
        self.sceneItemObjects.append(
            sceneItem(
                self,
                sceneItemId,
                sourceName,
                sourceType,
                sceneItemEnabled,
                self.sceneItemObjects.__len__(),
            )
        )

    def getSceneItemIdByName(self, sceneName):
        """for looking up IDs based on name

        :param sceneName: name of the scene
        :type sceneName: str
        :return: scene ID
        :rtype: int
        """
        for sceneItem in self.sceneItemObjects:
            if sceneItem.name == sceneName:
                return sceneItem.sceneItemId

    def getSceneItemByName(self, sceneItemName) -> sceneItem:
        for sceneItem in self.getSceneItems():
            if sceneItem.sourceName == sceneItemName:
                return sceneItem

    def getSceneItemByReference(self, sceneItemReference) -> sceneItem:
        for scene in self.getSceneItems():
            if scene.objectId == sceneItemReference:
                return scene

    def getSceneItemById(self, sceneItemId) -> sceneItem:
        for scene in self.getSceneItems():
            if int(scene.sceneItemId) == int(sceneItemId):
                return scene


class sceneItem:
    def __init__(
        self, parent, sceneItemId, sourceName, sourceType, sceneItemEnabled, objectId
    ):
        # add parent object reference for internal getByName functions
        # self.parent = weakref.ref(parent)
        # apparently this is bad for garbage collection, but I'll make up for it by drinking from Mehrweg bottles:
        self.parent = parent
        self.objectId = objectId
        self.sceneItemId = sceneItemId
        self.sourceName = sourceName
        self.sourceType = sourceType
        self.sceneItemEnabled = sceneItemEnabled

    def enable(self):
        setSceneItemEnabledOnWebsocket(self.parent.name, self.sceneItemId, True)
        self.sceneItemEnabled = True

    def disable(self):
        setSceneItemEnabledOnWebsocket(self.parent.name, self.sceneItemId, False)
        self.sceneItemEnabled = False

    def toggle(self):
        setSceneItemEnabledOnWebsocket(
            self.parent.name, self.sceneItemId, not self.sceneItemEnabled
        )
        self.sceneItemEnabled = not self.sceneItemEnabled


def getSceneByName(sceneName) -> scene:
    for scene in sceneObjects:
        if scene.name == sceneName:
            return scene


def prepare():
    """sets up the ws class, to be called at the correct time. could probably be an object or something"""
    obsSettings = data.config["obs-settings"]
    global wsp
    wsp = obswsp.ReqClient(
        host=obsSettings["websocketAddress"],
        port=obsSettings["websocketPort"],
        password=obsSettings["websocketPassword"],
    )


def selectSceneByNameOnWebsocket(sceneName):
    """selects a scene based on the name

    :param sceneName: the name of the scene
    :type sceneName: str
    :return: error text from OBS websocket
    :rtype: str?
    """
    error = wsp.set_current_program_scene(sceneName)
    return error


def setSceneItemEnabledOnWebsocket(sceneName, sceneItemId, sceneItemEnabled):
    wsp.set_scene_item_enabled(sceneName, sceneItemId, sceneItemEnabled)


def getSceneListFromWebsocket():
    """retreive list of scenes

    :return: array of scenes
    :rtype: array
    """
    scenes = wsp.get_scene_list()
    return scenes


def getSceneItemListFromWebsocket(sceneName):
    """retreive scene items by scene

    :param sceneName: name of the scene
    :type sceneName: str
    :return: array of scene items
    :rtype: array
    """
    sceneItems = wsp.get_scene_item_list(sceneName)
    return sceneItems


def populateScenes():
    """adds all scenes and sceneItems from OBS websocket"""
    requestScenes = getSceneListFromWebsocket()
    for requestScene in requestScenes.scenes:
        tempscene = scene(requestScene["sceneIndex"], requestScene["sceneName"])
        for requestSceneItem in getSceneItemListFromWebsocket(
            requestScene["sceneName"]
        ).scene_items:
            tempscene.addSceneItem(
                requestSceneItem["sceneItemId"],
                requestSceneItem["sourceName"],
                requestSceneItem["sourceType"],
                requestSceneItem["sceneItemEnabled"],
            )


def refreshScenes():
    """updates scene/item data from OBS"""
    # for all lack of efficiency, unreference objects
    global sceneObjects
    sceneObjects = []
    populateScenes()


def getSceneItemIdByName(sceneItemName):
    """gives next best sceneItem ID across all scenes. doesn't really work when there's duplicates

    :param sceneItemName: name of the sceneItem
    :type sceneItemName: str
    :return: sceneItemId
    :rtype: int
    """
    for scene in getScenes():
        if scene.getSceneItemIdByName(sceneItemName):
            return scene.getSceneItemIdByName(sceneItemName)


def getSceneItemByName(sceneItemName) -> sceneItem:
    """gets nects best sceneItem object across all scenes. problematic if names not unique

    :param sceneItemName: name of the sceneItem
    :type sceneItemName: str
    :return: sceneItem object
    :rtype: sceneItem
    """
    for scene in getScenes():
        if scene.getSceneItemByName(sceneItemName):
            return scene.getSceneItemByName(sceneItemName)


def getSceneByReference(sceneReference) -> scene:
    for scene in getScenes():
        if scene.objectId == sceneReference:
            return scene


def getSceneById(sceneId) -> scene:
    for scene in getScenes():
        if int(scene.id) == int(sceneId):
            return scene


class general:
    def __init__(self) -> None:
        pass

    def getVersion():
        version = wsp.get_version()
        return version

    def getStats():
        stats = wsp.get_stats()
        return stats

    def TriggerHotkeyByName(hotkeyName):
        wsp.trigger_hot_key_by_name(hotkeyName)


gen = general


def execute(raw) -> dict:
    """manages OBS things from raw strings"""
    if len(raw.split("-")) == 2:
        match raw.split("-")[0]:
            case "sceneswitch":
                selectSceneByNameOnWebsocket(raw.split("-")[1])
