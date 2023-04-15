from __future__ import annotations
import uuid


UUID_NAME = "xenontechs.space/streamhelper#actions"
UUID_NAMESPACE = uuid.NAMESPACE_DNS


class actions:
    def __init__(self) -> None:
        global actionObject
        self.actionObjects = []

        pass

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
        return self.id.hex, self.buttonlocation, self.group, self.label, self.icon, self.state
