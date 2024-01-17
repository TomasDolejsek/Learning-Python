"""
07_Day_4 - 01_Flask - 06_Exercise
(c) Tomas Dolejsek 2024-01-27

Using Flask, write th application which on the GET request `/lotto` will draw and display 6 numbers
in the range from 1 to 49 (the numbers cannot be repeated - this is a simulation of a lotto lottery draw).
"""

from random import shuffle
from flask import Flask
app = Flask(__name__)


def lotto_picks():
    numbers = list(range(1, 50))
    shuffle(numbers)
    return numbers[:6]


@app.route("/lotto", methods=['GET'])
def lotto():
    numbers = sorted(lotto_picks())
    return f"Lotto draw: {' - '.join(map(str, numbers))}"


@app.route("/")
def index():
    return f"Použití: /lotto"


if __name__ == '__main__':
    app.run()
