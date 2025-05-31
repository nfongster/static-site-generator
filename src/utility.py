import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text or node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Delimiter count must be even!  Bad node: {node}")
        
        in_main_text = True
        for subtext in node.text.split(delimiter):
            if subtext == "":
                in_main_text = not in_main_text
                continue
            
            subnode_text_type = node.text_type if in_main_text else text_type
            new_nodes.append(TextNode(subtext, subnode_text_type))
            in_main_text = not in_main_text

    return new_nodes


def extract_markdown_images(text):
    # Format: ![alt text](url)
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    # Format: [anchor text](url)
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)