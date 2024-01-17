"""
07_Day_4 - 01_Flask - 05_Exercise
(c) Tomas Dolejsek 2024-01-27

Using Flask, write an application, which on the GET request `/draw` will draw and display 3 digits
(digits can be repeated).
"""

from random import randint
from flask import Flask
app = Flask(__name__)


@app.route("/draw", methods=['GET'])
def draw_digits():
    digits = [str(randint(0, 9)) for _ in range(3)]
    return f"{' '.join(digits)}"


@app.route("/")
def index():
    return f"Použití: /draw"


if __name__ == '__main__':
    app.run()
