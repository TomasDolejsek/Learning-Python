"""
07_Day_4 - 01_Flask - 08_Exercise
(c) Tomas Dolejsek 2024-01-27

Write and run a simple calculator that:
    * displays a form with two fields for entering numbers and a list of selectable operations (+, -, *, /)
    * after pressing the "send" button calculates the result and displays it on the screen.
"""

from flask import Flask, request, render_template
app = Flask(__name__)


def calculate(n1, n2, op):
    try:
        n1, n2 = float(n1), float(n2)
        if op == '+':
            return n1 + n2
        if op == '-':
            return n1 - n2
        if op == '*':
            return n1 * n2
        if op == '/':
            return n1 / n2
    except ZeroDivisionError:
        return "Division by zero!"
    except ValueError:
        return "Invalid input!"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', display=None)
    if request.method == 'POST':
        number1 = request.form['n1']
        number2 = request.form['n2']
        op = request.form['operation']
        output = [number1, number2, op, calculate(number1, number2, op)]
        return render_template('index.html', display=output)


if __name__ == '__main__':
    app.run()
