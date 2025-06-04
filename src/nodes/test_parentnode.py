import unittest
from nodes import *


class TestParentNode(unittest.TestCase):
    def test_to_html_throws_if_no_children(self):
        with self.assertRaises(ValueError) as context:
            parent_node = ParentNode("div", None)
            parent_node.to_html()

    def test_to_html_throws_if_empty_children(self):
        with self.assertRaises(ValueError) as context:
            parent_node = ParentNode("div", [])
            parent_node.to_html()
    
    def test_to_html_with_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_nodes = [
            LeafNode("span", "Frodo", {"href": "frodo_dot_com"}),
            LeafNode("b", "Sam"),
            LeafNode("p", "Merry", {"to my friend": "fool of a took"}),
            LeafNode("i", "Pippin")
        ]
        parent_node = ParentNode("div", child_nodes)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span href=\"frodo_dot_com\">Frodo</span><b>Sam</b><p to my friend=\"fool of a took\">Merry</p><i>Pippin</i></div>"
        )

    def test_to_html_with_multiple_grandchildren(self):
        # parent -> 2x children -> 1x child each
        grandchild_node_1 = LeafNode("b", "grandkid 1")
        grandchild_node_2 = LeafNode("b", "grandkid 2")
        child_node_1 = ParentNode("span", [grandchild_node_1])
        child_node_2 = ParentNode("span", [grandchild_node_2])
        parent_node = ParentNode("p", [child_node_1, child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><span><b>grandkid 1</b></span><span><b>grandkid 2</b></span></p>"
        )