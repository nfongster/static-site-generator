import unittest
from conversion import *


class TestFileCreation(unittest.TestCase):
    def test_extract_title(self):
        title, content = extract_title("# My title")
        self.assertEqual(title, "My title")
        self.assertEqual(content, "")

    def test_extract_title_invalid(self):
        with self.assertRaises(Exception) as context:
            title, _ = extract_title("Invalid title")

    def test_extract_title_wrong_header(self):
        with self.assertRaises(Exception) as context:
            title, _ = extract_title("### Invalid header type")

    def test_extract_title_multiline(self):
        title, content = extract_title("# This is a\n\nmultiline\nmarkdown\n\nfile!")
        self.assertEqual(title, "This is a")
        self.assertEqual(content, "multiline\nmarkdown\n\nfile!")

    def test_extract_title_multiline_wrong_header(self):
        with self.assertRaises(Exception) as context:
            title, _ = extract_title("## This is a\n\nmultiline\nmarkdown\n\nfile!")
