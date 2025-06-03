from enum import Enum
import re
from functools import reduce


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