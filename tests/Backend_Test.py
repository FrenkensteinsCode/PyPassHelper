import os
import platform
import re
import sys
import unittest

sys.path.append("../PyPassHelper")
from PyPassHelper_backend import *

class Test_Backend_Methods(unittest.TestCase):

    def setUp(self):
        if platform.system() == "Windows":
            self.separator = "\\"
        else:
            self.separator = "/"
        self.key_location = os.getcwd() + self.separator + "secret.key"
        self.pwfile_location = os.getcwd() + self.separator + "pwfile.txt"
        self.key_location_exists = False
        self.pwfile_location_exists = False
        self.pw_contains_all_chars = False

    def tearDown(self):
        if self.key_location_exists:
            os.remove(self.key_location)
        if self.pwfile_location_exists:
            os.remove(self.pwfile_location)

    def test_key_is_created_correctly(self):
        key_gen(self.key_location)
        self.assertTrue(os.path.isfile(self.key_location))
        self.key_location_exists = True

    def test_pwfile_is_created_correctly(self):
        write_password("Test_Pass","Test_Service", self.pwfile_location)
        self.assertTrue(os.path.isfile(self.pwfile_location))
        self.pwfile_location_exists = True

    def test_create_password(self):
        password = create_password(8)
        if re.search(r'\d', password) and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\W', password):
            self.pw_contains_all_chars = True

        self.assertTrue(self.pw_contains_all_chars)

    def test_shuffle_is_working_as_expected(self):
        pre_shuffle = create_password(8)
        post_shuffle = shuffle(pre_shuffle, 8)
        self.assertFalse(pre_shuffle == post_shuffle)

    def test_create_passphrase(self):
        pass # Idea is to create a passphrase from predefined wordlists and to check it against the expected string...will implement this later

    def test_password_strength_variations(self):
        self.assertEqual("Excellent (Entropy: 80.4)", check_password_strength("123abcDEF!#?")) # Score 75-100
        self.assertEqual("Good (Entropy: 67.0)", check_password_strength("123abcDE!#")) # Score 50-74
        self.assertEqual("Weak (Entropy: 46.9)", check_password_strength("1abDE!#")) # Score 25-49
        self.assertEqual("Very Weak (Entropy: 18.9)", check_password_strength("1aB")) # Score 0-24


if __name__ == "__main__":
    unittest.main()