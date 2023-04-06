- do you have too many scenes in OBS? 
- is managing sources and visibility a chore? 
- do you think "oh hell no" if someone mentions using a new communication app because it means you have to integrate it into all those scenes?
- is streamer.bot just not enough?

well you've come to the right place, because we're not really fixing any of these issues, but we smack some python on top as duct tape!

# about
this is a tool to automate things in OBS, to be called from within OBS, that can interface with things outside of OBS. it is based on python, uses flask to present you with a Browser Dock (OBS) and calls preprogrammed changes via OBS Websocket. Further triggers can be configured in use with streamer.bot and because it's fun, it solves all other annoying problems as well

current version: early prototype

# (possible) features
- local server (all yours, no cloud)
- dock for OBS with buttons to press that do things
- easy™ way to configure what the buttons do
- pre-stream checklist, as automated as possible (AKA "why is my feature not working? ah, forgot to open streamerbot")
- autodetect running game and apply that to game/app capture

# how to use
1. clone repo
2. Run `python -m venv venv` to create a virtual environment and activate the venv (see https://docs.python.org/3/library/venv.html)
3. Install the required packages with either
  * `pip install -r contrib/requirements.txt` for development OR 
  * `pip install -r contrib/requirements.lock` for stable requirements
5. run `python app.py`
6. open http://127.0.0.1:5000/ in your browser
7. click things until you hit "settings", fill them to the best of your ability
8. go to OBS, add a Browser Deck with the URL http://127.0.0.1:5000/deck?nonav=heckyeah
9.  you should now have buttons in OBS that probably don't do things
10. go to src/datastore.py and configure the buttons properly
11. good luck

# how to contribute
feel free to commit to the dev branch, but be careful, I will hold submissions to the highest standards that I know of. at the moment these standards are very low, but I do not give any guarantees for the future. 