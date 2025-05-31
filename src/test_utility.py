import unittest
from utility import *
from textnode import TextType, TextNode


class TestUtility(unittest.TestCase):
    def test_empty_string(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [node]
        self.__validate(new_nodes, expected_nodes)

    def test_no_subtext(self):
        node = TextNode("This is normal text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [node]
        self.__validate(new_nodes, expected_nodes)

    def test_invalid_format(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is `invalid` for`mat!", TextType.NORMAL)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_inline_bold(self):
        node = TextNode("This is text with a **very bold** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("very bold", TextType.BOLD),
            TextNode(" word", TextType.NORMAL)
        ]
        self.__validate(new_nodes, expected_nodes)

    def test_inline_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.NORMAL)
        ]
        self.__validate(new_nodes, expected_nodes)

    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL)
        ]
        self.__validate(new_nodes, expected_nodes)

    def test_multiple_text_types(self):
        node = TextNode("Here _is_ some more **text** but `we split on` code", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Here _is_ some more **text** but ", TextType.NORMAL),
            TextNode("we split on", TextType.CODE),
            TextNode(" code", TextType.NORMAL)
        ]
        self.__validate(new_nodes, expected_nodes)

    def test_multiple_old_nodes(self):
        node1 = TextNode("This is **the first** node", TextType.NORMAL)
        node2 = TextNode("...and here `is` **an** italic node", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("the first", TextType.BOLD),
            TextNode(" node", TextType.NORMAL),
            TextNode("...and here `is` **an** italic node", TextType.ITALIC)
        ]
        self.__validate(new_nodes, expected_nodes)

    def test_subtext_is_main_text(self):
        node = TextNode("_This is an italic node_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [TextNode("This is an italic node", TextType.ITALIC)]
        self.__validate(new_nodes, expected_nodes)

    def __validate(self, new_nodes, expected_nodes):
        for actual_node, expected_node in zip(new_nodes, expected_nodes):
            self.assertEqual(actual_node.text, expected_node.text)
            self.assertEqual(actual_node.text_type, expected_node.text_type)
            self.assertEqual(actual_node.url, expected_node.url)