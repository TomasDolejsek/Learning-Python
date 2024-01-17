"""
07_Day_4 - 01_Flask - 02_Exercise
(c) Tomas Dolejsek 2024-01-27

Write and run an application that displays the current time on the screen.
"""

from flask import Flask
from datetime import datetime
app = Flask(__name__)


@app.route("/")
def index():
    return datetime.now().strftime("%H:%M:%S")


if __name__ == '__main__':
    app.run()
