import re
from functools import reduce
from conversion import *
from nodes import *


def markdown_to_html_node(markdown):
    return ParentNode(
        __block_type_to_tag(BlockType.DIVISION), 
        list(map(__create_block_node, markdown_to_blocks(markdown)))
    )


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(lambda b: b != "", [block.strip() for block in blocks]))


def __create_block_node(block):
    block_type = block_to_blocktype(block)
    return ParentNode(
        __block_type_to_tag(block_type, __get_num_hashes(block)), 
        __create_child_nodes(block, block_type))


def __get_num_hashes(text):
    matched = re.match(r'^#{1,6} ', text)
    return max(len(matched.group(0)) - 1, 0) if matched else 0


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


def __block_type_to_tag(block_type, n=0):
    match block_type:
        case BlockType.DIVISION:
            return "div"
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            if n < 1 or n > 6:
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


def __create_child_nodes(block, block_type):
    match block_type:
        case BlockType.CODE:
            return [TextNode(block.strip("```").lstrip("\n"), TextType.CODE).to_html_node()]

        case BlockType.UNORDERED_LIST:
            text_items = [item for item in block.replace("\n", "").split("- ")[1:]]
            return __create_child_nodes_for_list_items(text_items)
    
        case BlockType.ORDERED_LIST:
            text_items = [item for item in [re.sub(r'^\d+\.\s*', '', line) for line in block.split("\n")]]
            return __create_child_nodes_for_list_items(text_items)

        case BlockType.HEADING:
            return [node.to_html_node() for node in text_to_textnodes(block.lstrip("# "))]

        case BlockType.QUOTE:
            return [node.to_html_node() for node in text_to_textnodes(block.lstrip("> ").replace("\n> ", "\n"))]

        case _:
            return [node.to_html_node() for node in text_to_textnodes(block)]


def __create_child_nodes_for_list_items(text_items):
    child_nodes_per_item = [__create_child_nodes(text, TextType.NORMAL) for text in text_items]
    return [ParentNode("li", children) for children in child_nodes_per_item]