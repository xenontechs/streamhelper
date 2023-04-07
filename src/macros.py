"""easy to define way to create a bunch of things happening on command
first as functions, later possibly read by file or something"""
import src.obs as obs
import src.datastore as data


def raw(id, type, action):
    """eats basic button data. may be easier to call this one and organizing here than defining other functions all over the place
    :param id: Button ID
    :param type: Action Type (used to resolve category)
    :param action: specific action

    :return: 0 if successful, 1 if something messed up
    """
    print("id:" + id + " type:" + type + " action:" + action)
    error = ""
    match type:
        # a wild sceneswitch button, call OBS websocket, if good, flip all buttons accordingly
        case "sceneswitch":
            error = obs.selectSceneByName(action)
            if error.datain["status"] == "ok":
                for key, value in data.buttons.items():
                    if value.group == "sceneswitch" and value.execute != "":
                        value.state = "disabled"
                data.buttons[id].state = "enabled"
                return 0
            else:
                print("argh!")
                return 1
