"""
08_Day_4_-_homework - 02_Exercise
(c) Tomas Dolejsek 2024-01-28

Write a Flask application that asks the user to enter a 10-digit ISBN number (on a GET "/" action), and then
(on the POST "/" action) displays the information:
    * `Correct ISBN` if the code is in valid Polish format (00-001).
    * `Incorrect ISBN` otherwise.

Pass the code as parameter `isbn`.

##### 10-digit ISBN number validation
The check digit (the last one in ISBN number) is the sum of the preceding digits multiplied by their positions,
modulo 11, with 10 being represented as X.

For example, to find the checksum of an ISBN number whose first nine digits are 0-306-40615, calculate:

1x0 + 2x3 + 3x0 + 4x6 + 5x4 + 6x0 + 7x6 + 8x1 + 9x5 = 0 + 6 + 0 + 24 + 20 + 0 + 42 + 8 + 45 = 145 = 13x11 + 2

So the check digit is 2, and the full number is ISBN 0-306-40615-2.
"""

from flask import Flask, request, render_template
app = Flask(__name__)


def validate_isbn(isbn):
    pure_isbn = [x for x in isbn if x != '-']
    if len(pure_isbn) != 10:
        return False
    check = 0
    try:
        for i, number in enumerate(pure_isbn[:-1]):
            check += (i + 1) * int(number)
        return check % 11 == int(pure_isbn[-1])
    except ValueError:
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', display=None)
    if request.method == 'POST':
        isbn = request.form['isbn']
        result = "Correct ISBN" if validate_isbn(isbn) else "Incorrect ISBN"
        return render_template('index.html', display=result)


if __name__ == '__main__':
    app.run()
