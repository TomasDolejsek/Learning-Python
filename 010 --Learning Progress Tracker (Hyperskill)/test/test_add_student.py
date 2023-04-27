import unittest

from tracker import add_student

class TestCase(unittest.TestCase):

    incorrect_input = [
        "John Doe email",
        "John Doe email@lol",
        "John Doe email@lol.",
        "John Doe @email.com",
        "John D email@lol.com",
        "John D. email@lol.com",
        "John Dunkan1 email@lol.com",
        "John Doo-Bee-Doo- email@lol.com",
        "John Door' email@lol.com",
        "John D--ies email@lol.com",
        "John D'-lork email@lol.com",
        "John- DooBeeDoo email@lol.com",
        "J DooBeeDoo email@lol.com",
        "John' DooBeeDoo email@lol.com",
        "'John DooBeeDoo email@lol.com"
        ]

    correct_input = [
        "John DooBeeDoo email@lol.com",
        "John D'Ark email@lol.com",
        "John Doo-Bee-Doo email@lol.com"
        ]

    def test_add_student(self):
        for s in self.correct_input:
            print(s)
            self.assertTrue(add_student(s.split()))
        for s in self.incorrect_input:            
            print(s)
            self.assertFalse(add_student(s.split()))
            
if __name__ == '__main__':
    unittest.main()