import unittest
from nodes import *


class TestLeafNode(unittest.TestCase):
    def test_no_value_throws(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode("p", None)
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b_with_props(self):
        node = LeafNode("b", "This is bold", {"href": "not.a.website"})
        self.assertEqual(node.to_html(), "<b href=\"not.a.website\">This is bold</b>")