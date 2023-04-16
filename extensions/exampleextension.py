NAME = "Example Extension"
DESCRIPTION = "this is the example extension, it simply outputs things to console and possibly creates some fancy buttons"
VERSION = "0.0.1"
AUTHOR = "Xenontechs"
AUTHOR_WEBSITE = "https://xenontechs.space"
DOCUMENTATION = "https://xenontechs.space/streamhelper#extensions"


# a dict of setting name and default value
# scope will be added on import, so no need for naming like "myExtension.setting"
extensionSettings = {"examplesetting": 123, "extensioniscool": True}


# this will be called after loading and checking the extension, with it a dictionary of the current settings
# in return, it is expected to return a dictionary with updated settings (if needed)
# this makes the above useless? or at least up to the dev
def init(settings={}) -> dict:
    returnSettings = {}
    if not settings == {}:
        print("exampleextension.init: received settings")
        for setting, value in settings.items():
            print(
                "exampleextension.init: received setting "
                + setting
                + " with value "
                + value
            )
            if setting in extensionSettings:
                print("exampleextension.init: setting ok")
                returnSettings[setting] = value
            else:
                print("exampleextension.init: setting unknown, deleting")
                returnSettings[setting] = ""
    else:
        print("exampleextension.init: no settings received")
    for defaultsetting, value in extensionSettings.items():
        if defaultsetting not in settings:
            print(
                "exampleextension.init: setting "
                + str(defaultsetting)
                + "missing, adding with default value "
                + str(value)
            )
            returnSettings[defaultsetting] = value
    return returnSettings


def execute(actionData):
    print("exampleextension.execute: received actionData: " + actionData)
    print("exampleextension.testActionData: pretending to do something ")
    return True


def testActionData(actionData):
    print("exampleextension.testActionData: received actionData: " + actionData)
    print("exampleextension.testActionData: pretending it's fine ")
    return True
