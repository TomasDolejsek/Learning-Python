import unittest

from tracker import add_student

class TestCase(unittest.TestCase):

    incorrect_input = [
        "Tom Dol email",
        "Tom Dol email@cz",
        "Tom Dol email@cz.",
        "Tom Dol @email.cz",
        "Tom D email@cz.com",
        "Tom D. email1@cz.com",
        "Tom Dol1 email2@cz.com",
        "Tom Dol-Bol-Vol- email3@cz.com",
        "Tom Dol' email4@cz.com",
        "Tom D--sek email5@cz.com",
        "Tom D'-lejs email6@cz.com",
        "Tom- DolBolVol email7@cz.com",
        "T DolBolVol email8@cz.com",
        "Tom' DolBolVol email9@cz.com",
        "'Tom DolBolVol email10@cz.com"
        ]

    correct_input = [
        "Tom DolBolVol email11@cz.com",
        "Tom D'Ejsek email12@cz.com",
        "Tom Dol-Bol-Vol email13@cz.com"
        ]

    def test_add_student(self):
        print("Testing correct inputs:")
        for s in self.correct_input:
            print(s)
            self.assertTrue(add_student(s.split()))
        print("Testing incorrect inputs:")
        for s in self.incorrect_input:            
            print(s)
            self.assertFalse(add_student(s.split()))
            
if __name__ == '__main__':
    unittest.main()