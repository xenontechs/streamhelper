"""easy to define way to create a bunch of things happening on command
first as functions, later possibly read by file or something"""
import src.obs as obs
import src.datastore as data


def raw(id, type, action):
    print("id:" + id + " type:" + type + " action:" + action)
    error = ""
    match type:
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
