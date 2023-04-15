import os
import importlib.util
import src.datastore as data


module_folder = "extensions"


def load():
    for filename in os.listdir(module_folder):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module_path = os.path.join(module_folder, filename)

            # Check if the module should be loaded
            # load if found with config true
            # skip if found with config false
            # add with false and log if not found
            if not data.config.has_option("modules", module_name):
                data.config["extensions"][module_name] = False
                # LOG AND MESSAGE ABOUT NEW MODULE
            if data.config.has_option(
                "modules", module_name
            ) and data.config.getboolean("modules", module_name):
                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Do something with the module
                # ...
