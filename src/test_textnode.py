import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", text_type=TextType.BOLD)
    print(f"Node: {node}")
    node2 = TextNode("This is a text node", text_type=TextType.BOLD)
    print(f"Node 2: {node2}")
    print(f"Text comparison: {node.text == node2.text}")
    print(f"Text type comparison: {node.text_type == node2.text_type}")
    print(f"URL comparison: {node.url == node2.url}")
    self.assertEqual(node, node2)

if __name__ == "__main__":
  unittest.main()