import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_node_with_no_props_set(self):
        node = HTMLNode()

        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_node_with_all_props_set(self):
        tag = "<p>"
        value = "I'm a paragraph!"
        children = [HTMLNode("a tag"), HTMLNode("another tag")]
        props = {
            "propA": "stuff for prop A",
            "propB": "more stuff for prop B"
        }
        node = HTMLNode(tag, value, children, props)

        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_node_with_empty_list_of_childen(self):
        node = HTMLNode(children=[])
        self.assertEqual(node.children, [])

    def test_props_to_html__no_props(self):
        node = HTMLNode()

        actual_html = node.props_to_html()
        expected_html = ""
        
        self.assertEqual(actual_html, expected_html)

    def test_props_to_html__with_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        node = HTMLNode(props=props)

        actual_html = node.props_to_html()
        expected_html = " href=\"https://www.google.com\" target=\"_blank\""

        self.assertEqual(node.props_to_html(), expected_html)

    def test_repr_empty_node(self):
        node = HTMLNode()

        actual_repr = repr(node)
        expected_repr = "HTMLNode(None, None, None, None)"

        self.assertEqual(actual_repr, expected_repr, f"Actual __repr__: {actual_repr}")

    def test_repr_node_with_props(self):
        node = HTMLNode("<p>", "test value", [], {"prop": "property stuff"})

        actual_repr = repr(node)
        expected_repr = "HTMLNode(<p>, test value, [], {\'prop\': \'property stuff\'})"

        self.assertEqual(actual_repr, expected_repr, f"Actual __repr__: {actual_repr}")