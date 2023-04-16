import os
import sys
import importlib.util
import src.datastore as data
import src.appconfig as appconfig

extensions_folder = "extensions"
extensions = {}


def load():
    for filename in os.listdir(extensions_folder):
        if filename.endswith(".py"):
            extension_name = filename[:-3]
            extension_path = os.path.join(extensions_folder, filename)
            # print("# extensions.load: found " + str(extension_path))
            # print("# extensions.load: found in config? " + str(data.config.has_option("extensions", str(extension_name))))
            # print("# extensions.load: enabled in config? " + str(data.config.getboolean("extensions", extension_name)))

            # Check if the extension should be loaded
            # load if found with config true
            # skip if found with config false
            # add with false and log if not found
            if not data.config.has_option("extensions", extension_name):
                data.config["extensions"][str(extension_name)] = "False"
                print(
                    "# extensions.load: new extension found, enable in settings: "
                    + extension_name
                )
                # LOG AND MESSAGE ABOUT NEW extension
            if data.config.has_option(
                "extensions", str(extension_name)
            ) and data.config.getboolean("extensions", extension_name):
                print("# extensions.load: loading extension: " + extension_name)
                # Load the module
                # add try/catch maybe, in case the extension sucks?
                spec = importlib.util.spec_from_file_location(
                    extension_name, extension_path
                )
                extension = importlib.util.module_from_spec(spec)
                sys.modules[extension_name] = extension
                spec.loader.exec_module(extension)
                extensions[extension_name] = extension
                # check for required data
                errors, warnings = checkExtension(extension)
                # # load if good
                # if len(errors) < 1:
                #     if len(warnings) < 1:
                #         # log and show warnings
                #         pass
                # else:
                #     # if it was enabled before, disable now
                #     if extension_name in data.config["extensions"]:
                #         data.config["extensions"][str(extension_name)] = "False"
                #     # LOG AND ERROR, EXTENSION LOADING FAILED
                #     pass


def init():
    for extension in extensions.values():
        settings = {}
        extendedSettings = {}
        print("# extensions.init: initialize extension: " + extension.__name__)

        # this chaos will run over existing settings in the config, remove the extension name prefix,
        # then store it in a ditionary, while removing it from the config, then pass it on to the extensions init function
        # this should return an updated dictionary that we attach the prefix to and throw it into our config again
        # upside: extensions can do updates and checkups to settings, as well as store them for itself!
        # we need to push them to the extension anyways at some point....
        # downside: all the things, complexity, extensions HAVE to control settings actively
        # alternative: just read from extension.settings[]?
        for setting, value in data.config.items("extensionsettings"):
            print("this my setting? " + setting + " = " + str(value))
            print(setting.split(".")[0])
            print(setting.split(".")[0])
            print(extension.__name__)
            if str(setting.split(".")[0]) == str(extension.__name__):
                print(
                    "yep!... because "
                    + setting.split(".")[0]
                    + " == "
                    + extension.__name__
                )
                settings[setting.split(".")[1]] = value
                if data.config.remove_option("extensionsettings", setting):
                    print("removed " + setting)
                print(data.config.items("extensionsettings"))
        settings = extension.init(settings)
        for setting, value in settings.items():
            extendedSettings[extension.__name__ + "." + setting] = value
        print(extendedSettings)
        appconfig.saveConfigToFile()
        data.config.read_dict({"extensionsettings": extendedSettings})


def checkExtension(extension):
    # critical criteria, needs to be set, otherwise the extension should be rejected
    extensionImportErrors = []
    extensionImportErrors.append("missing NAME") if not hasattr(
        extension, "NAME"
    ) else False
    extensionImportErrors.append("missing AUTHOR") if not hasattr(
        extension, "AUTHOR"
    ) else False
    extensionImportErrors.append("missing init()") if not hasattr(
        extension, "init"
    ) else False
    extensionImportErrors.append("missing execute()") if not hasattr(
        extension, "execute"
    ) else False
    # warnings
    extensionImportWarnings = []
    extensionImportWarnings.append("missing DESCRIPTION") if not hasattr(
        extension, "DESCRIPTION"
    ) else False
    extensionImportWarnings.append("missing VERSION") if not hasattr(
        extension, "VERSION"
    ) else False
    extensionImportWarnings.append("missing AUTHOR_WEBSITE") if not hasattr(
        extension, "AUTHOR_WEBSITE"
    ) else False
    extensionImportWarnings.append("missing DOCUMENTATION") if not hasattr(
        extension, "DOCUMENTATION"
    ) else False
    extensionImportWarnings.append("missing testActionData()") if not hasattr(
        extension, "testActionData"
    ) else False
    print("# extensions.checkExtension: Errors: " + str(extensionImportErrors))
    print("# extensions.checkExtension: Warnings: " + str(extensionImportWarnings))

    return extensionImportErrors, extensionImportWarnings


def reload():
    global extensions
    extensions = {}
    load()
    init()
