# hello.py
from flask import Flask, render_template
import subprocess


app = Flask(__name__)

def focusFirefox():
    subprocess.run(['hyprctl', 'dispatch', 'focuswindow', 'class:^(firefox)$'])


@app.route("/")
def index():
    return render_template("index.html")

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
