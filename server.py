# hello.py
from flask import Flask, render_template
import subprocess


app = Flask(__name__)

def playPause():                                                             
    subprocess.run(["wtype", " "])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/press/playpause")
def pressPlayPause():
    playPause()
    return "playpause pressed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
