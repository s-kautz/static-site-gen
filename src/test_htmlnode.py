import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
  def test_to_html(self):
    node = HTMLNode()
    with self.assertRaises(NotImplementedError):
      node.to_html()
  
  def test_props_to_html(self):
    node = HTMLNode()
    with self.assertRaises(ValueError):
      node.props_to_html()
    node.props = dict()
    node.props["testcase"] = "This is a test case"
    self.assertEqual(node.props_to_html(), ' testcase="This is a test case"')
  
  def test_repr(self):
    node = HTMLNode(tag="foo", value="bar")
    self.assertEqual(repr(node), f'HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})')

if __name__ == "__main__":
  unittest.main()