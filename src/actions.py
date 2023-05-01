from __future__ import annotations
import uuid
import src.extensions as extensions


"""
ok the hell is this? it's a class that collects actions
the hell is an action? anything that we can call to do things:
- make OBS do things
- make streamerbot do things
- make a macro do many things

anything? so also, like, clicking a link in the menu? well absolutely!
so we kinda have to figure out how to easily path our way through a bunch of decisions
the difference between switching a scene in OBS and calling an action in streamerbot is: a lot
so what do we need:
"I want to press a button and streamerbot does an action"
- a button, clickable, with name/icon
- a "path" - streamerbot > actions > action-ID
- a check for success

"I want to switch scenes in OBS"
- a button, clickable, with name/icon
- a path - obs > sceneswitch > scene-ID
- a check for success
- an update to button state to display active scene
- an update to other button states to display inactive scene

"I want to toggle a source in OBS"
- a button, clickable, with name/icon
- a path - obs > sourcetoggle > scene-id > source-ID
- a check for success
- an update to button state to display active scene
- an update to other button states to display inactive scene

path could be done with raw asn-style data
- obs.sourcetoggle.scene-id.source-id
- streamerbot.actions.actionid
and then match case through all the things

or strictly defined, but with a more open "data" field
- target="obs", actiontype="togglevisibility", data="17-5"

both don't really include a proper way of doing the "return&re-action" part
for that, it may be better to define a class for each target
- class obstarget:
- def buttonstoggleactivescene()
that would essentially give it a more modular approach
- che class can define the button behavior (for single-action vs toggle)
also gives each module the possibility to check if it understands the assignment

that leaves us with:
- module name
- module action string
- readable name
- button stuff
    - icon
    - title

"""

UUID_NAME = "xenontechs.space/streamhelper#actions"
UUID_NAMESPACE = uuid.NAMESPACE_DNS
stateclasses = {
    "": "btn-primary",
    "active": "btn-primary",
    "enabled": "btn-success",
    "inactive": "btn-outline-inactive",
    "disabled": "btn-outline-danger",
}


class actions:
    def __init__(self) -> None:
        # global actionObject
        self.actionObjects = []

    def addAction(
        self,
        actionName="",
        actionProvider="",
        actionData="",
        group="",
        state="",
        label="",
        icon="",
        buttonlocation="",
    ):
        """add a new action

        :param actionName: a name to recognize, defaults to ""
        :type actionName: str, optional
        :param actionProvider: who to send the data to, defaults to ""
        :type actionProvider: str, optional
        :param actionData: additional data it needs to know, defaults to ""
        :type actionData: str, optional
        :param group: which group it belongs to (important in frontend), defaults to ""
        :type group: str, optional
        :param state: the current display state, defaults to ""
        :type state: str, optional
        :param label: the label of the button, defaults to ""
        :type label: str, optional
        :param icon: the icon to use instead of the label, defaults to ""
        :type icon: str, optional
        :param buttonlocation: the place of the button, defaults to ""
        :type buttonlocation: str, optional
        """
        newAction = action(
            uuid.uuid4(),
            actionName,
            actionProvider,
            actionData,
            group,
            state,
            label,
            icon,
            buttonlocation,
        )
        # HACK: should return which thing is causing the problem
        if newAction.test():
            self.actionObjects.append(newAction)
        else:
            print(
                f"actions: error creating action. provider:{newAction.actionProvider}, actionData:{newAction.actionData}"
            )
        pass

    def getActionById(self, id) -> action:
        print(f"{self.__module__} getActionById(): {id}")
        for action in self.actionObjects:
            print(action.id)
            match str(id):
                case str(action.id):
                    print(f"= action: {action.id}")
                    return action
                case str(action.id.hex):
                    print(f"= action: {action.id.hex}")
                    return action
                case str(action.id.int):
                    print(f"= action: {action.id.int}")
                    return action
                case str(action.id.urn):
                    print(f"= action: {action.id.urn}")
                    return action
        # log error, UUID crappy, this should not be possible, halt all the things

    def getFriendlyList(self) -> list:
        """get a friendly list of actions"""
        returnList = []
        for item in self.actionObjects:
            returnList.append(str(item.actionProvider + ">" + str(item.action)))
        return returnList


class action:
    def __init__(
        self,
        id,
        action,
        actionProvider,
        actionData,
        group,
        state,
        label,
        icon,
        buttonlocation,
    ) -> None:
        self.id = id
        self.action = action
        self.actionProvider = actionProvider
        self.actionData = actionData
        self.group = group
        self.state = state
        self.label = label
        self.icon = icon
        self.buttonlocation = buttonlocation
        pass

    def getState(self):
        # TODO: extensions.sys.modules[self.actionProvider].getState()
        pass

    def getStateClass(self) -> str:
        return stateclasses[self.state]

    def getButton(self) -> list:
        """returns all required elements for buttonplacement

        :return: _description_
        :rtype: list
        """
        return (
            self.id.hex,
            self.buttonlocation,
            self.group,
            self.label,
            self.icon,
            self.state,
        )

    def call(self) -> bool:
        """calls this objects defined action

        :return: true if good, false if bad
        :rtype: bool
        """
        # check if actionProvider is native, default to extension
        # this should possibly be iterating a lis of native providers
        # but also there should not be any native providers (apart from macros?) once this is finished
        match self.actionProvider:
            case "obs":
                # TODO: add OBS call
                pass
            case "macro":
                # TODO: add macro call
                pass
            case _:
                return extensions.sys.modules[self.actionProvider].execute(
                    self.actionData
                )

    def test(self) -> bool:
        """tests for existing provider and if it accpts the given data

        :return: true if good, false if bad
        :rtype: bool
        """
        match self.actionProvider:
            case "src.obs":
                return True
            case "src.macro":
                return True
            case _:
                # print(f"actions.action.test(): testing for module {str(self.actionProvider)}")
                # print(f"actions.action.test(): testing in {extensions.sys.modules.keys()}")
                if str(self.actionProvider) in extensions.sys.modules.keys():
                    # print(f"actions.action.test(): module found")
                    # print(f"actions.action.test(): testing action data")
                    if extensions.sys.modules[self.actionProvider].testActionData(
                        self.actionData
                    ):
                        print(
                            f"actions.action.test(): action data fine: {self.actionProvider}: {self.actionData}"
                        )
                        return True
                    else:
                        # print(f"actions.action.test(): action data not fine")
                        return False
                else:
                    print(
                        f"actions.action.test(): module not found: {self.actionProvider}"
                    )
                    return False
