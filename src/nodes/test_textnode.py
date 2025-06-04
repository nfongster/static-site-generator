import unittest
from nodes import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("Test Node A", TextType.BOLD)
        node2 = TextNode("Test Node B", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_text_style(self):
        node = TextNode("Test Node", TextType.BOLD)
        node2 = TextNode("Test Node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Test Node", TextType.ITALIC, "fake_url")
        node2 = TextNode("Test Node", TextType.ITALIC, "fake_url")
        self.assertEqual(node, node2)

    # Test conversion to HTML (leaf) node

    def test_invalid_text_type_throws(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is an invalid node", -1)
            html_node = node.to_html_node()

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("cout << \"sad boi\" << endl", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "cout << \"sad boi\" << endl")

    def test_link(self):
        node = TextNode("dis is a link", TextType.LINK, "website.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "dis is a link")
        self.assertEqual(html_node.props, {"href": "website.com"})

    def test_image(self):
        node = TextNode("dis is a pic", TextType.IMAGE, "imgsrc/")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "imgsrc/", "alt": "dis is a pic"})


if __name__ == "__main__":
    unittest.main()