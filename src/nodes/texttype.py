from enum import Enum


class TextType(Enum):
    NORMAL = 1,
    BOLD = 2,
    ITALIC = 3,
    CODE = 4,
    LINK = 5,
    IMAGE = 6