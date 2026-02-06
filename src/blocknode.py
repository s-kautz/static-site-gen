from enum import Enum
from htmlnode import ParentNode

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UL = "unordered_list"
  OL = "ordered_list"

class BlockNode():
  def __init__(self, block_type=BlockType.PARAGRAPH, text=None, children=None):
    self.block_type = block_type
    self.text = text
    self.children = children
  
  def __eq__(self, other):
    return (
      self.block_type == other.block_type
      and self.text == other.text
      and self.children == other.children
    )
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.block_type.value}, {self.children})"
  
  def children_to_nodes(self):
    for child in self.children:
      return


def block_node_to_html_node(block_node):
  return