from flask import Blueprint, request, render_template
import configparser
import logging
import src.datastore as data
import src.macros as macro
import src.obs as obs


EVENTLOG_FILENAME = "event.log"
logging.basicConfig(filename=EVENTLOG_FILENAME, level=logging.INFO)

bp = Blueprint("routes", __name__)

# @bp.route('/button1')
# def button1():
#     print("hello, button1 speaking?")
#     return 'this would better be a redirect template'


##################
# basic app stuff
##################


# main page
@bp.route("/")
def index():
    return render_template("index.html", navigationData=data.navigationData)


# about page
@bp.route("/about")
def about():
    return render_template("about.html", navigationData=data.navigationData)


# status page
@bp.route("/status")
def status():
    return render_template(
        "status.html", statuslist=data.statuslist, navigationData=data.navigationData
    )


# log page
@bp.route("/log")
def log():
    logging.info("accessed logfile")
    with open("event.log") as f:
        logcontents = f.readlines()
    return render_template(
        "log.html", navigationData=data.navigationData, logcontents=logcontents
    )


# settings page to edit config.ini
@bp.route("/settings", methods=["GET", "POST"])
def settings():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if request.method == "POST":
        for key, value in request.form.items():
            # print(key + ' - ' + value)
            section, option = key.split(".")
            config.set(section, option, value)
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        logging.info("configuration file changed")
    sections = config.sections()
    return render_template(
        "settings.html",
        config=config,
        sections=sections,
        navigationData=data.navigationData,
    )


# Deck page
@bp.route("/deck", methods=["GET", "POST"])
def deck():
    if request.method == "POST":
        for key, value in request.form.items():
            print(key + " - " + value)
            items = value.split(".")
        macro.raw(items[0], items[1], items[3])
    nonav = request.args.get("nonav")
    return render_template(
        "deck.html",
        nonav=nonav,
        navigationData=data.navigationData,
        buttons=data.buttons,
    )


# scenes page
@bp.route("/scenes")
def scenes():
    return render_template("scenes.html", scenes=obs.getScenes())


# playground page
@bp.route("/playground", methods=["GET", "POST"])
def playground():
    if request.method == "POST":
        for key, value in request.form.items():
            print(key + " - " + value)
            items = value.split(".")
        macro.raw(items[0], items[1], items[3])
    config = configparser.ConfigParser()
    config.read("config.ini")
    nonav = request.args.get("nonav")
    return render_template(
        "playground.html",
        nonav=nonav,
        navigationData=data.navigationData,
        statuslist=data.statuslist,
        config=config,
        buttons=data.buttons,
    )
