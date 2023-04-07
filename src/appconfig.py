import logging
import src.datastore as data
import os


configFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")


def createDefaultConfig():
    """create the default configuration file"""
    data.config["obs-settings"] = {}
    data.config["obs-settings"]["websocketAddress"] = "127.0.0.1"
    data.config["obs-settings"]["websocketPort"] = "4444"
    data.config["obs-settings"]["websocketPassword"] = "CHANGEME"
    with open(configFilePath, "w") as configfile:
        data.config.write(configfile)
    print("created config, please go to settings")
    return 0


# goal is to have some way of verifying the config items
# like not having the default value or junk as a boolian
# throw a tantrum if stuff is aloof, this could happen in web view as well
def testconfigfile():
    """test for configuration file, create if needed"""
    if not len(data.config.read(configFilePath)):
        logging.info("No config file found, creating a new one")
        createDefaultConfig()
    else:
        logging.debug("config file found")
