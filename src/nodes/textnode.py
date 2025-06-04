from nodes import *


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def to_html_node(self):
        match self.text_type:
            case TextType.NORMAL:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {
                    "href": self.url
                })
            case TextType.IMAGE:
                return LeafNode("img", "", {
                    "src": self.url,
                    "alt": self.text
                })
            case _:
                raise Exception(f"invalid text type: {self.text_type}")
    
    def __eq__(self, other_node):
        return self.text == other_node.text \
               and self.text_type == other_node.text_type \
               and self.url == other_node.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"
