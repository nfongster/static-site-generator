import unittest
from utility import *
from textnode import TextType, TextNode


class TestUtility(unittest.TestCase):
    # Split Nodes Delimiter
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

    # Extract Markdown Images
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_images_nested_brackets(self):
        text = "More text ![stuff[nest]](https://www.google.com)"
        expected = []
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_nested_brackets(self):
        text = "More text [stuff[nest]](https://www.google.com)"
        expected = []
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_links_ignore_images(self):
        text = "Here is an image: ![myimage](https://www.google.com) and link: [mylink](google.com)"
        expected = [("mylink", "google.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    # Split Nodes Image
    def test_split_image_no_images(self):
        node = TextNode("no links here!", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("no links here!", TextType.NORMAL)
        ], new_nodes)

    def test_split_image_link_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ], new_nodes)

    def test_split_image_link_first(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) is a link", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        print(new_nodes)
        self.assertListEqual([
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" is a link", TextType.NORMAL)
        ], new_nodes)

    def test_split_image_link_second(self):
        node = TextNode("Here is link: ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        print(new_nodes)
        self.assertListEqual([
            TextNode("Here is link: ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ], new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_two_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        node2 = TextNode(
            "This ![link](https://i.imgur.com/zjjcJKZ.png) is just a copy",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This ", TextType.NORMAL),
                TextNode("link", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is just a copy", TextType.NORMAL)
            ],
            new_nodes,
        )

    # Split Nodes Link