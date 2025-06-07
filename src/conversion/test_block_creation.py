import unittest
from conversion import *


class TestBlockCreation(unittest.TestCase):
    def test_paragraph(self):
        block = "This is some text."
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading_one_hash(self):
        block = "# This is a heading."
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_max_hashes(self):
        block = "###### This is a heading with 6 hashes."
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_invalid_heading(self):
        block = "##This is an invalid heading (no space)"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code(self):
        block = "```This is some code```"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_invalid_start(self):
        block = "``This is some invalid code```"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_invalid_end(self):
        block = "```This is some invalid code`"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_one_line(self):
        block = "> Here's a quote"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_multi_line(self):
        block = "> Here is\n> a multiline\n>quote"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_invalid(self):
        block = "> Here is\n> an invalid\n >quote"  # last line starts with " "
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- This is\n- an unordered  \n-  List"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        block = "- This is\nnot a valid  \n-  List"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. This is\n2. an ordered  \n3.  List"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_invalid(self):
        block = "1 This is\n2. an invalid  \n3.  List"
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # MD -> HTML Conversion
    def test_headers(self):
        md = """
# This is a header

## This is a smaller header

###### This is the smallest header
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a header</h1><h2>This is a smaller header</h2><h6>This is the smallest header</h6></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote_one_line(self):
        md = """
>This is a single-line quote block
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a single-line quote block</blockquote></div>"
        )

    def test_blockquote_multiline(self):
        md = """
>This is a 
>multi-line
>block quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a \nmulti-line\nblock quote</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- An item
- Another item
- Some item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>An item</li><li>Another item</li><li>Some item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. An item
2. Another item
3. Some item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>An item</li><li>Another item</li><li>Some item</li></ol></div>"
        )

    def test_unordered_list_with_embedded_content(self):
        md = """
- A **bold** item
- Another item
- Some item with a [link](my.url)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>A <b>bold</b> item</li><li>Another item</li><li>Some item with a <a href=\"my.url\">link</a></li></ul></div>"
        )

    def test_ordered_list_with_embedded_content(self):
        md = """
1. A **bold** item
2. Another item
3. Some item with an ![image](my.url)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>A <b>bold</b> item</li><li>Another item</li><li>Some item with an <img src=\"my.url\" alt=\"image\"></img></li></ol></div>"
        )

    def test_unordered_list_one_item(self):
        md = """- **bold stuff**"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li><b>bold stuff</b></li></ul></div>")