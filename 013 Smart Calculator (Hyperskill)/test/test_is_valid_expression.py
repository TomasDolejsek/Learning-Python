import unittest

from calculator import is_valid_expression

class MyTestCase(unittest.TestCase):
    empty_input = ''

    incorrect_input = [
        "-2 +3 2",
        "--6 + 3",
        "6 -6 -",
        "6 + 6 -",
        "6 +",
        "+3 -- 6 8",
        "2-",
        "3+-",
        "2 -5+"
    ]
    correct_input = [
        "2 + 3 --- -6",
        "-3 ++ 6 + 8 -- -9",
        "-2",
        "859",
        "-3    + 8    -- 6"
    ]

    #def __init__(self):
     #   Print("Test of is_valid_expression started:\n")

    def test_is_empty(self):
        self.assertFalse(is_valid_expression(self.empty_input))
        print("\ntest_is_empty() finished.")

    def test_is_correct(self):
        for s in self.correct_input:
            print(f"'{s}' expression as correct tested.")
            self.assertTrue(is_valid_expression(s))
        print("\ntest_is_correct() finished.")

    def test_is_incorrect(self):
        for s in self.incorrect_input:
            print(f"'{s}' expression as incorrect tested.")
            self.assertFalse(is_valid_expression(s))
        print("\ntest_is_incorrect() finished.")

if __name__ == '__main__':
    unittest.main()
