"""
07_Day_4 - 01_Flask - 03_Exercise
(c) Tomas Dolejsek 2024-01-27

Write and run an application that displays the current date on the screen.
"""

from flask import Flask
from datetime import date
app = Flask(__name__)


@app.route("/")
def index():
    return f"{date.today()}"


if __name__ == '__main__':
    app.run()
