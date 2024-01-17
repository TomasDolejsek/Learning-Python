"""
07_Day_4 - 01_Flask - 07_Exercise
(c) Tomas Dolejsek 2024-01-27

Write and run an application that:
    * displays on the screen a form asking the user to enter their name
    * when it has been submitted, it greets the user with the message: "Hello <Name>!"
"""

from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        template = """
        <form action='/' method='POST'>
            <input type='text' placeholder='Username' name='user_name'>
            <button type='submit'>Submit</button>
        </form>
        """
        return template

    if request.method == 'POST':
        name = request.form['user_name']
        return f'Hello {name}!'


if __name__ == '__main__':
    app.run()
