import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", text_type=TextType.BOLD)
    node2 = TextNode("This is a text node", text_type=TextType.BOLD)
    self.assertEqual(node, node2)
  
  def test_text_to_html(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
  unittest.main()