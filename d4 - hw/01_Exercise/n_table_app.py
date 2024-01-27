"""
08_Day_4_-_homework - 01_Exercise
(c) Tomas Dolejsek 2024-01-28

Write a Flask application that asks the user to enter the natural number n (on a GET "/" action),
and then (on the POST "/" action) displays a table containing in consecutive rows:
    * 2 to the power of n
    * n to the power of n
    * n factorial
Pass the number as parameter n.
"""

from math import factorial
from collections import namedtuple
from flask import Flask, request, render_template
app = Flask('__name__')
Results = namedtuple('Results', ['two_power', 'n_power', 'fact'])


def calculate(n):
    try:
        n = int(n)
        return Results(two_power=2 ** n, n_power=n ** n, fact=factorial(n))
    except ValueError:
        return "Invalid input!"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', results=None)
    if request.method == 'POST':
        n = request.form['number']
        return render_template('index.html', results=calculate(n), number=n)


if __name__ == "__main__":
    app.run()
