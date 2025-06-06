import re
from functools import reduce
from conversion import *
from nodes import *


def markdown_to_html_node(markdown):
    block_nodes = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_blocktype(block)
        block_node = ParentNode(__block_type_to_tag(block_type, __get_num_hashes(block)), None)
        # TODO: Refactor this switch statement into a helper method
        if block_type == BlockType.CODE:
            block_node.children = [TextNode(block.strip("```").lstrip("\n"), TextType.CODE).to_html_node()]
        elif block_type == BlockType.UNORDERED_LIST:
            block_node.children = []
            for item in block.replace("\n", "").split("- ")[1:]:
                node = TextNode(item, TextType.NORMAL).to_html_node()
                node.tag = "li"
                block_node.children.append(node)
        elif block_type == BlockType.ORDERED_LIST:
            block_node.children = []
            for item in [re.sub(r'^\d+\.\s*', '', line) for line in block.split("\n")]:
                node = TextNode(item, TextType.NORMAL).to_html_node()
                node.tag = "li"
                block_node.children.append(node)
        else:
            block_node.children = __text_to_children(__remove_markdown(block, block_type))
        block_nodes.append(block_node)
    return ParentNode("div", block_nodes)


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(lambda b: b != "", [block.strip() for block in blocks]))


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


def __get_num_hashes(text):
    matched = re.match(r'^#{1,6} ', text)
    if not matched:
        return 0
    count = len(matched.group(0)) - 1
    return max(count, 0)


def __remove_markdown(text, block_type):
    match block_type:
        case BlockType.HEADING:
            text = text.lstrip("# ")
        case BlockType.QUOTE:
            text = text.lstrip(">").replace("\n>", "\n")
        case BlockType.UNORDERED_LIST:
            # replace "- " with ""
            text = text.lstrip("- ").replace("\n- ", "\n")
        case BlockType.ORDERED_LIST:
            # replace `#. ` with ""
            pass
    return text

def __text_to_children(text):
    nodes = text_to_textnodes(text)
    return [node.to_html_node() for node in nodes]