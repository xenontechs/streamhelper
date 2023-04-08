"""obs websocket functions
using https://github.com/aatikturk/obsws-python"""
import obsws_python as obswsp
import src.datastore as data

# pre-initialize global websocket
wsp = {}

# all scene objects will be in here
sceneObjects = []


def getScenes():
    return sceneObjects


def getSceneByName(sceneName):
    for scene in sceneObjects:
        if scene.name == sceneName:
            return scene


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
        self.objectId = sceneObjects.count
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
        self.sceneItemObjects.append(sceneItem(sceneItemId, sourceName, sourceType, sceneItemEnabled, self.sceneItemObjects.count))

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


class sceneItem:
    def __init__(self, sceneItemId, sourceName, sourceType, sceneItemEnabled, objectId):
        self.objectId = objectId
        self.sceneItemId = sceneItemId
        self.sourceName = sourceName
        self.sourceType = sourceType
        self.sceneItemEnabled = sceneItemEnabled


def prepare():
    """sets up the ws class, to be called at the correct time. could probably be an object or something"""
    obsSettings = data.config["obs-settings"]
    # global ws
    global wsp
    # ws = obsws(
    #     obsSettings["websocketAddress"],
    #     obsSettings["websocketPort"],
    #     obsSettings["websocketPassword"]
    # )
    wsp = obswsp.ReqClient(
        host=obsSettings["websocketAddress"],
        port=obsSettings["websocketPort"],
        password=obsSettings["websocketPassword"]
    )


def selectSceneByName(sceneName):
    """selects a scene based on the name

    :param sceneName: the name of the scene
    :type sceneName: str
    :return: error text from OBS websocket
    :rtype: str?
    """
    error = wsp.set_current_program_scene(sceneName)
    return error


def setSceneItemEnabled(sceneName, sceneItemId, sceneItemEnabled):
    pass


def getSceneList():
    """retreive list of scenes

    :return: array of scenes
    :rtype: array
    """
    scenes = wsp.get_scene_list()
    return scenes


def getSceneItemList(sceneName):
    """retreive scene items by scene

    :param sceneName: name of the scene
    :type sceneName: str
    :return: array of scene items
    :rtype: array
    """
    sceneItems = wsp.get_scene_item_list(sceneName)
    return sceneItems


def populateScenes():
    """adds all scenes and sceneItems from OBS websocket
    """
    requestScenes = getSceneList()
    print(requestScenes.scenes)
    for requestScene in requestScenes.scenes:
        tempscene = scene(requestScene["sceneIndex"], requestScene["sceneName"])
        for requestSceneItem in getSceneItemList(requestScene["sceneName"]).scene_items:
            tempscene.addSceneItem(
                requestSceneItem["sceneItemId"],
                requestSceneItem["sourceName"],
                requestSceneItem["sourceType"],
                requestSceneItem["sceneItemEnabled"]
            )


def refreshScenes():
    """updates scene/item data from OBS
    """
    # for all lack of efficiency, unreference objects
    global sceneObjects
    sceneObjects = []
    populateScenes()
