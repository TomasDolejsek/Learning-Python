"""
05_Day_3 - 02_Error_handling - 04_Exercise
(c) Tomas Dolejsek 2024-01-27

Write a function named `phone` that takes the parameter `number`, which denotes a phone number.
The function has to check if the given number is in the list of numbers (invent some).
If so - the function should return the number given in the parameter. If not - it must return an exception
of the type `Exception` with a comment `There is no such number!`.
"""


def phone(number):
    known_numbers = (11111, 22222, 33333)
    try:
        if number not in known_numbers:
            raise Exception
        return number
    except Exception:
        return "There is no such number!"


n1 = 11111
n2 = 12345
print(phone(n1))
print(phone(n2))
