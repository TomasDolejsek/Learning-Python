"""
07_Day_4 - 01_Flask - 04_Exercise
(c) Tomas Dolejsek 2024-01-27

Using Flask, write a program that will return the result of adding two numbers sent in a GET request
`/count/number1/number2`
"""

from flask import Flask
app = Flask(__name__)


@app.route("/count/<num1>/<num2>", methods=['GET'])
def add_numbers(num1, num2):
    return f"{int(num1) + int(num2)}"


@app.route("/")
def index():
    return f"Použití: /count/number1/number2"


if __name__ == '__main__':
    app.run()
