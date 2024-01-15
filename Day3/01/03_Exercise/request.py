"""
05_Day_3 - 01_Virtualenv - 03_Exercise
(c) Tomas Dolejsek 2024-01-27

Using the **requests** library, write a simple program that will connect to any page
and download the HTML code of the home page.
"""

import requests


r = requests.get('http://www.coderslab.cz')
print(r.text)
