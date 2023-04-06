import logging
import src.datastore as data
import os


configFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")


def createDefaultConfig():
    """create the default configuration file"""
    data.config["app-server-settings"] = {}
    data.config["app-server-settings"]["port"] = "8647"
    data.config["app-server-settings"]["name"] = "localhost"
    data.config["obs-settings"] = {}
    data.config["obs-settings"]["scenecollectionxml"] = "TODOpath"
    data.config["obs-settings"]["websocketAddress"] = "127.0.0.1"
    data.config["obs-settings"]["websocketPort"] = "4444"
    data.config["obs-settings"]["websocketPassword"] = "socketpuppies"
    data.config["obs-settings"]["legacy"] = "True"
    # config['DEFAULT'] = {'ServerAliveInterval': '45',
    #                     'Compression': 'yes',
    #                     'CompressionLevel': '9'}
    # config['forge.example'] = {}
    # config['forge.example']['User'] = 'hg'
    # config['topsecret.server.example'] = {}
    # topsecret = config['topsecret.server.example']
    # topsecret['Port'] = '50022'     # mutates the parser
    # topsecret['ForwardX11'] = 'no'  # same here
    # config['DEFAULT']['ForwardX11'] = 'yes'
    with open(configFilePath, "w") as configfile:
        data.config.write(configfile)
    print("created config, please go to settings")
    return 0


def testconfigfile():
    """test for configuration file, create if needed"""
    if not len(data.config.read(configFilePath)):
        logging.info("No config file found, creating a new one")
        createDefaultConfig()
    else:
        logging.debug("config file found")
