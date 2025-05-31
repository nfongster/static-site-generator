from functools import reduce
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node must have a tag!")

        if not self.children:
            raise ValueError("parent node must have children!")
        
        children_html = reduce(lambda x, y: x + y, [child.to_html() for child in self.children], "")
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"