"""
06_Day_3_-_homework - 03_Exercise
(c) Tomas Dolejsek 2024-01-27

Write a function `validate_isbn` that takes a 13-digit ISBN number as a text string,
then checks its correctness and returns:

* `True` if the ISBN is correct,
* `False` if the ISBN is incorrect.

##### 13-digit ISBN number validation rules

This kind of ISBN number consists of 13 digits, the last of which is a check digit. The check digit of the 13-digit
version of an ISBN is calculated as follows:

The individual digits of the ISBN are given corresponding weights. The first digit is given a weight of 1,
the second 3, the third 1 and so on (the odd digits are given 1, the even digits 3).
Each digit is multiplied by its weight and then all the products are added together.
The resulting sum is divided by 10, and the remainder is subtracted from 10.
If the remainder is 0, then the control digit is also 0.
"""


def validate_isbn(isbn):
    pure_isbn = [x for x in isbn if x !='-']
    if len(pure_isbn) != 13:
        return False
    suma = 0
    odd = True
    try:
        for n in pure_isbn[:-1]:
            suma += int(n) if odd else int(n) * 3
            odd = not odd   
        cn = (10 - suma % 10) % 10
        return cn == int(pure_isbn[-1])
    except ValueError:
        return False


if __name__ == '__main__':
    print(validate_isbn('978-80-7080-637-1'))
    print(validate_isbn('978-0-545-01022-1'))
