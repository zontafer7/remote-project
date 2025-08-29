from flask import Flask, render_template, jsonify, request
from movieFinder import MovieFinder
import subprocess
import os
import dotenv

app = Flask(__name__)

dotenv.load_dotenv()
tmdbApiKey = os.environ.get('TMDB_API_KEY')
tmdbFinder = MovieFinder(tmdbApiKey)

def focusFirefox():
    subprocess.run(['hyprctl', 'dispatch', 'focuswindow', 'class:^(firefox)$'])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/movies")
def movies():
    return render_template("movies.html")

@app.route("/search")
def searchTmdb():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    results = tmdbFinder.search(query)
    return jsonify({"results": results})

@app.route("/select/<int:movieID>")
def selectMovie(movieID):
    subprocess.run(['firefox', '--new-tab', f'https://www.cineby.app/movie/{movieID}?play=true'])
    return "ok"

@app.route("/press/<action>")
def press(action):
    if action == 'playpause':
        focusFirefox()
        subprocess.run(['wtype', ' '])

    elif action == 'fullscreen':
        focusFirefox()
        subprocess.run(['wtype', 'f'])

    return "working"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
