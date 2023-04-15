from __future__ import annotations
import uuid


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

that leads us with:
- module name
- module action string
- readable name
- button stuff
    - icon
    - title

"""

UUID_NAME = "xenontechs.space/streamhelper#actions"
UUID_NAMESPACE = uuid.NAMESPACE_DNS


class actions:
    def __init__(self) -> None:
        global actionObject
        self.actionObjects = []

    def addAction(
        self,
        actionName="",
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
        self.actionObjects.append(
            action(
                uuid.uuid5(UUID_NAMESPACE, UUID_NAME),
                actionName,
                actionData,
                group,
                state,
                label,
                icon,
                buttonlocation,
            )
        )
        pass

    def getActionById(self, id):
        for action in self.actionObjects:
            match id:
                case action.id:
                    return action
                case action.id.hex:
                    return action
                case action.id.int:
                    return action
                case action.id.urn:
                    return action
        # log error, UUID crappy, this should not be possible, halt all the things


# this will probably be extensions
class action:
    def __init__(
        self, id, action, actionData, group, state, label, icon, buttonlocation
    ) -> None:
        self.id = id
        self.action = action
        self.actionData = actionData
        self.group = group
        self.state = state
        self.label = label
        self.icon = icon
        self.buttonlocation = buttonlocation
        pass

    def getState(self):
        pass

    def getButton(self):
        return (
            self.id.hex,
            self.buttonlocation,
            self.group,
            self.label,
            self.icon,
            self.state,
        )
