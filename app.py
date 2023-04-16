from flask import Flask
import src.appconfig as appconfig
from src.routes import bp
import logging
import src.datastore as data
import src.obs as obs
import src.extensions as extensions

LOG_FILENAME = "app.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


app = Flask(__name__)
app.register_blueprint(bp)
app.config.from_pyfile("src/flaskConfig.py")


@app.before_first_request
def before_first_request():
    appconfig.testconfigfile()
    obs.prepare()
    obs.populateScenes()
    data.config["extensions"]["exampleextension"] = "True"
    extensions.load()
    extensions.init()
    appconfig.saveConfigToFile()
    data.appstatus.update()
    print("Starting server on http://localhost:5000")


if __name__ == "__main__":
    """main function"""
    app.run()
