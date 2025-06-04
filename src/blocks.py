from enum import Enum
import re
from functools import reduce
from utility import *
from nodes import *


class BlockType(Enum):
    PARAGRAPH = 1,
    HEADING = 2,
    CODE = 3,
    QUOTE = 4,
    UNORDERED_LIST = 5,
    ORDERED_LIST = 6


def block_to_blocktype(block):
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    if re.match(r'^`{3}', block) and re.search(r'`{3}$', block):
        return BlockType.CODE

    agg = lambda x, y: x and y
    if reduce(agg, [re.match(r'^>', line) for line in block.split('\n')], True):
        return BlockType.QUOTE

    if reduce(agg, [re.match(r'^- ', line) for line in block.split('\n')], True):
        return BlockType.UNORDERED_LIST

    if reduce(agg, [re.match(rf'{i+1}. ', line) for i, line in enumerate(block.split('\n'))], True):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    block_nodes = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_blocktype(block)
        block_node = ParentNode(block_type_to_tag(block_type, get_num_hashes(block)), None)
        if block_type == BlockType.CODE:
            block_node.children = [TextNode(block.strip("```").lstrip("\n"), TextType.CODE).to_html_node()]
        else:
            block_node.children = text_to_children(block.lstrip("# "))  # TODO: This is suspect...
        block_nodes.append(block_node)
    return ParentNode("div", block_nodes)


def block_type_to_tag(block_type, n=0):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            if n < 1:
                raise ValueError(f"The block type was HEADING, but the hash count was invalid: {n}")
            return f"h{n}"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case _:
            raise ValueError(f"Unsupported block type: {block_type}")


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [node.to_html_node() for node in nodes]


def get_num_hashes(text):
    matched = re.match(r'^#{1,6} ', text)
    if not matched:
        return 0
    count = len(matched.group(0)) - 1
    return max(count, 0)