"""
07_Day_4 - 01_Flask - 01_Exercise
(c) Tomas Dolejsek 2024-01-27

Write and run your first Flask application that, upon entering `/`, greets the user with the caption: "Hello user!".
Upon entering `/hello/<name>`, it will output the user's name entered in the parameter `<name>`.
"""

from flask import Flask
app = Flask(__name__)


@app.route("/hello/<name>")
@app.route("/")
def index(name='user'):
    return f"Hello {name}!"


if __name__ == '__main__':
    app.run()
