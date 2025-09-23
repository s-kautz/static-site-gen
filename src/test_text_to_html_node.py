import unittest
from text_to_html_node import *
from textnode import TextNode


class TestMain(unittest.TestCase):
  def test_text(self):
      node = TextNode("This is a text node", TextType.TEXT)
      html_node = text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "This is a text node")