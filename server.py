from flask import Flask, render_template, jsonify, request, url_for, redirect
from movieFinder import MovieFinder
import subprocess
import os
import dotenv
import time
import lz4.block
import json

app = Flask(__name__)

currentMedia = None
profile = os.path.expanduser("~/.mozilla/firefox/63hi75lx.default-release/")
session_file = os.path.join(profile, "sessionstore-backups", "recovery.jsonlz4")
dotenv.load_dotenv()
tmdbApiKey = os.environ.get('TMDB_API_KEY')
tmdbFinder = MovieFinder(tmdbApiKey)

def focusFirefox():
    subprocess.run(['hyprctl', 'dispatch', 'focusmonitor', 'HDMI-A-1'])
    #subprocess.run(['hyprctl', 'dispatch', 'focuswindow', 'class:^(firefox)$'])

def hideCursor():
    subprocess.run(['hyprctl', 'dispatch', 'movefocus', 'l'])

def urlSplitter(url:str):
    global currentMedia
    url = url.split('?', 1)[0]
    url = url.split('://', 1)[1]
    url = url.split('/',1)[1]
    parts = url.strip('/').split('/')

    result = {
        'format': 'None',
        'id': None,
        'season': None,
        'episode': None
    }

    if len(parts) >= 2:
        result['format'] = parts[0]
        result['id'] = parts[1]
        currentMedia = {'format': result['format'], 'id': result['id']}

    if result['format'] == 'tv':
        result['season'] = parts[2]
        result['episode'] = parts[3]
        currentMedia = {'format': result['format'], 'id': result['format'], 'season':result['season'], 'episode':result['episode']}

    return result

def getCinebyUrl():
    try:
        with open(session_file, "rb") as f:
            data = f.read()


        decompressed = lz4.block.decompress(data[8:])
        session = json.loads(decompressed)

        for window in session["windows"]:
            for tab in window["tabs"]:
                i = tab["index"] - 1  # active entry
                url = tab["entries"][i]["url"]
                if 'cineby.app' in url:
                    return(urlSplitter(url))

        return None
    except:
        return None
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/movies/")
def movies():
    return render_template("movies.html")

@app.route("/search")
def searchTmdb():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    results = tmdbFinder.search(query)
    return jsonify({"results": results})

@app.route("/select/<mediaType>/<int:movieID>")
def selectMovie(movieID, mediaType, season='1', episode='1'):
    focusFirefox()
    current = getCinebyUrl()
    if current:
        press('closeTab')
    if mediaType == 'tv':
        subprocess.run(['firefox', '--new-tab', f'https://www.cineby.app/tv/{movieID}/{season}/{episode}?play=true'])
        currentMedia = {'format': mediaType, 'id': movieID, 'season': season, 'episode': episode}
    else:
        subprocess.run(['firefox', '--new-tab', f'https://www.cineby.app/movie/{movieID}?play=true'])
        currentMedia = {'format': mediaType, 'id': movieID}
    return redirect(url_for("index"))

@app.route("/current")
def current():
    global currentMedia
    if not currentMedia:
        return 'none'

    details = tmdbFinder.getDetails(currentMedia['format'], currentMedia['id'])
    return jsonify({'status':'ok', 'media':currentMedia, 'details':details})

@app.route("/press/<action>")
def press(action):
    if action == 'playpause':
        focusFirefox()
        time.sleep(0.1)
        subprocess.run(['wtype', ' '])
        time.sleep(0.5)
        hideCursor()

    elif action == 'fullscreen':
        focusFirefox()
        print('focused')
        time.sleep(0.1)
        subprocess.run(['wtype', 'f'])
        print('screened')
        time.sleep(0.5)
        hideCursor()

    elif action == 'shutdown':
        subprocess.run(['shutdown', '-h', 'now'])

    elif action == 'nextEpisode':
        current = getCinebyUrl()
        if current == None:
            return 'not open'

        if current['format'] == 'tv':
            currentEp = int(current['episode'])
            current['episode'] = str(currentEp+1)
            focusFirefox()
            selectMovie(current['id'], current['format'], current['season'], current['episode'])
        else:
            return 'not tv'

    elif action == 'closeTab':
        focusFirefox()
        subprocess.run(['wtype', '-M', 'ctrl', 'w', '-m', 'ctrl'])

    return "working"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
