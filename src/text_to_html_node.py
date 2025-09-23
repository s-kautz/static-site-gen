from textnode import TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
  if not text_node.text_type in TextType:
    raise ValueError("TextNode object with unhandled TextType")
  if text_node.text_type == TextType.TEXT:
    return LeafNode(tag=None, value=text_node.text)
  if text_node.text_type == TextType.BOLD:
    return LeafNode(tag="b", value=text_node.text)
  if text_node.text_type == TextType.ITALIC:
    return LeafNode(tag="i", value=text_node.text)
  if text_node.text_type == TextType.CODE:
    return LeafNode(tag="code", value=text_node.text)
  if text_node.text_type == TextType.LINK:
    return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
  if text_node.text_type == TextType.IMAGE:
    return LeafNode(tag="img", value=text_node.text, props={"src": text_node.url, "alt": text_node.text})