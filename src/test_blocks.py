import unittest
from blocks import *


class TestUtility(unittest.TestCase):
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