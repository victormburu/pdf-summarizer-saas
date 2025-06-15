import pdb
import unittest
from password import char
pdb.set_trace()
class TestCharFunction(unittest.TestCase):

    def test_length_not_10(self):
        with self.assertRaises(ValueError):
            char("short")
        with self.assertRaises(ValueError):
            char("thisisaverylongstring")

    def test_not_lowercase(self):
        with self.assertRaises(ValueError):
            char("ABCDEFGHIJ")
        with self.assertRaises(ValueError):
            char("Abcdefghij")

    def test_starts_with_vowel(self):
        with self.assertRaises(ValueError):
            char("abcdefghij")
        with self.assertRaises(ValueError):
            char("ijklmnopqr")

    def test_starts_with_consonant(self):
        with self.assertRaises(ValueError):
            char("bcdefghijk")
        with self.assertRaises(ValueError):
            char("lmnopqrstuv")

    def test_valid_input(self):
        self.assertEqual(char("bcdefghijk"), "b")
        self.assertEqual(char("lmnopqrstuv"), "l")

if __name__ == '__main__':
    unittest.main()