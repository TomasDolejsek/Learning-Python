"""
07_Day_4 - 01_Flask - 10_Exercise
(c) Tomas Dolejsek 2024-01-27

Using Flask, write a program that will respond to a request sent to `/` (that is, `http://localhost:5000/`)
depending on the method it was sent through:
    - if the method was POST - the response will be the string "You have sent a POST",
    - if the method was GET - the response will be the string "You have sent a GET".
    - if the method was PUT - the response will be the string "You have sent a PUT".
    - if the method was DELETE - the response will be the string "You have sent a DELETE".
"""

from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def index():
    return f"You have sent a {request.method}"


if __name__ == '__main__':
    app.run()
