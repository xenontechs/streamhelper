import configparser
import src.status as status

appstatus = status.status()


class deckbutton:
    """any button thrown on the page that should do something
    essentially not more than mapping some strings to pass around"""

    def __init__(
        self, group="none", name="", execute="", state="active", icon=""
    ) -> None:
        """initializes deckbutton object

        :param group: is used in front end to group buttons neatly if they have the same name, defaults to "none"
        :type group: str, optional
        :param name: visible name on the button, defaults to ""
        :type name: str, optional
        :param execute: the macrofunction to execure, defaults to ""
        :type execute: str, optional
        :param state: visible state of the button, defaults to "active"
        :type state: str, optional
        :param icon: icon name superseeds name if exists, neds to be resolved in iconTranslate, defaults to ""
        :type icon: str, optional
        """
        self.group = group
        self.name = name
        self.execute = execute
        self.state = state
        self.icon = icon
        # states:
        # - active - a clickable button that does things
        # - inactive - a button that does nothing
        # - enabled - a feature that's enabled
        # - disabled - a feature that is disabled

    stateTranslate = {
        "active": "btn-primary",
        "enabled": "btn-success",
        "inactive": "btn-outline-inactive",
        "disabled": "btn-outline-danger",
    }

    # if only there was a way to have the will to do this properly
    iconTranslate = {
        "scene": r"static\scene_FILL0_wght400_GRAD0_opsz20.svg",
        "music": r"static\music_note_FILL0_wght400_GRAD0_opsz20.svg",
    }

    def getStateClass(self):
        """resolves self.state into CSS class"""
        return self.stateTranslate[self.state]

    def getIconPath(self):
        """resolves self.icon into icon file path"""
        return self.iconTranslate[self.icon]


class navlink:
    """makes it easy to set navigation items"""

    def __init__(self, name, link, pos="l", style="", target="_self") -> None:
        """initializes navlinks

        :param name: visible name
        :type name: str
        :param link: target link
        :type link: str
        :param pos: position in the navigation pane, defaults to "l"
        :type pos: str, optional
        :param style: CSS class, defaults to ""
        :type style: str, optional
        :param target: window target, defaults to "_self"
        :type target: str, optional

        target is _self or anything else (picked up by a.target in templates)
        this solves the problem of not looking for http in URI, which could be something else
        but it kills opening internal links in new windows if needed
        """
        self.name = name
        self.link = link
        self.pos = pos
        self.style = style
        self.target = target


# this dictionary is nonsense, just array this shit and use buttons[i].name etc.
# that just needs to be clear in the roundabout that thing taked in the update circle
# be a happy and defined object --> be button --> be posted --> be evaluated by macro --> be happy up-to-date object
buttons = {
    "0": deckbutton("sceneswitch", "icon", "", "inactive", "scene"),
    "1": deckbutton("sceneswitch", "start", "Stream Starting", "disabled"),
    "2": deckbutton("sceneswitch", "ingame", "In-Game", "disabled"),
    "3": deckbutton("sceneswitch", "brb", "BRB", "disabled"),
    "4": deckbutton("sceneswitch", "onfire", "onfire", "disabled"),
    "5": deckbutton("sceneswitch", "leaving", "Stream Ending", "disabled"),
    "6": deckbutton("music", "icon", "", "inactive", "music"),
    "7": deckbutton("music", "Disable", "disablemusic", "active"),
    "8": deckbutton("music", "Spotify", "togglespotify", "disabled"),
    "9": deckbutton("music", "Pretzel", "togglepretzel", "disabled"),
    "10": deckbutton("music", "Browser", "togglebrowsermusic", "disabled"),
    "11": deckbutton("visibility", "gamepad", "pad", "disabled"),
    "29-7": deckbutton("testing", "gamepad", "togglevisibility", "active"),
}

# defines links for the navigation pane
navigationData = [
    navlink("Settings", "settings", "l"),
    navlink("About", "about", "l"),
    navlink("Status", "status", "l"),
    navlink("Log", "log", "l"),
    navlink("Deck", "deck", "l"),
    navlink("Scenes", "scenes", "l"),
    navlink("playground", "playground", "l"),
    navlink("Code", "https://github.com/xenontechs", "r", target="_blank"),
    navlink("[xt]", "https://xenontechs.space", "r", target="_blank"),
]


# initialize config here, use it later in other places
config = configparser.ConfigParser()


# list of status items. functions should just be able to add and set them as needed
# maybe a preset would be better than having this open as-is? but then we need to predefine all the things
# this way, it only shows things that the app already touched. maybe it needs to be fed from refreshing the status page?
# that means a global "updateStatusOnAllTheThings()"
# also this kinda also shows which features are enabled, maybe that's confusing
statuslist = {}
