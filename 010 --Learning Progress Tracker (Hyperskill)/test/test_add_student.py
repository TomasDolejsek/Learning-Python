import unittest

from tracker import add_student

class TestCase(unittest.TestCase):

    incorrect_input = [
        "Tom Dol email",
        "Tom Dol email@cz",
        "Tom Dol email@cz.",
        "Tom Dol @email.cz",
        "Tom D email@cz.com",
        "Tom D. email@cz.com",
        "Tom Dol1 email@cz.com",
        "Tom Dol-Bol-Vol- email@cz.com",
        "Tom Dol' email@cz.com",
        "Tom D--sek email@cz.com",
        "Tom D'-lejs email@cz.com",
        "Tom- DolBolVol email@cz.com",
        "T DolBolVol email@cz.com",
        "Tom' DolBolVol email@cz.com",
        "'Tom DolBolVol email@cz.com"
        ]

    correct_input = [
        "Tom DolBolVol email@cz.com",
        "Tom D'Ejsek email@cz.com",
        "Tom Dol-Bol-Vol email@cz.com"
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