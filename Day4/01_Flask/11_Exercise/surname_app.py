"""
07_Day_4 - 01_Flask - 11_Exercise
(c) Tomas Dolejsek 2024-01-27

Using Flask, write and run a program that:

* upon entering using the GET method will display an empty form with the following fields:
    * name,
    * surname,
    * "Send" button.
* the above form should send data using the POST method.
* when accessed using the POST method, it will display the message "Hello _name surname_".
"""

from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        name = request.form['first_name']
        surname = request.form['surname']
        return f"Hello {name} {surname}"


if __name__ == "__main__":
    app.run()
