import re
from nodes import *


def text_to_textnodes(text):
    # Assumption: there is no nesting (e.g., no bold within a link)
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([TextNode(text, TextType.NORMAL)], "**", TextType.BOLD),\
                "_", TextType.ITALIC), \
            "`", TextType.CODE)))


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text or node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Delimiter ({delimiter}) count must be even!  Bad node: {node}")
        
        in_main_text = True
        for subtext in node.text.split(delimiter):
            if subtext == "":
                in_main_text = not in_main_text
                continue
            
            subnode_text_type = node.text_type if in_main_text else text_type
            new_nodes.append(TextNode(subtext, subnode_text_type))
            in_main_text = not in_main_text

    return new_nodes


def split_nodes_image(old_nodes):
    return __split_nodes(old_nodes, TextType.IMAGE, lambda text, url: f"![{text}]({url})")


def split_nodes_link(old_nodes):
    return __split_nodes(old_nodes, TextType.LINK, lambda text, url: f"[{text}]({url})")


def __split_nodes(old_nodes, link_type, formatter):
    new_nodes = []
    if link_type not in [TextType.LINK, TextType.IMAGE]:
        raise ValueError(f"Unsupported link type: {link_type}")
    
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        text_link_tuples = extract_markdown_images(node.text) \
            if link_type == TextType.IMAGE \
            else extract_markdown_links(node.text)
        
        if len(text_link_tuples) == 0:
            new_nodes.append(node)
            continue
        
        running_text = node.text
        for text, url in text_link_tuples:
            split_text = running_text.split(formatter(text, url))
            # If the original text did not start with the link
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.NORMAL))
            new_nodes.append(TextNode(text, link_type, url))
            running_text = split_text[1]  # TODO: Make recursive
        
        # Check for trailing, non-link text
        if running_text != "":
            new_nodes.append(TextNode(running_text, TextType.NORMAL))

    return new_nodes


def extract_markdown_images(text):
    # Format: ![alt text](url)
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    # Format: [anchor text](url)
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)