import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
  def test_to_html(self):
    node = HTMLNode()
    with self.assertRaises(NotImplementedError):
      node.to_html()
  
  def test_props_to_html(self):
    node = HTMLNode()
    with self.assertRaises(AttributeError):
      node.props_to_html()
    node.props = dict()
    node.props["testcase"] = "This is a test case"
    self.assertEqual(node.props_to_html(), ' testcase="This is a test case"')
  
  def test_repr(self):
    node = HTMLNode(tag="foo", value="bar")
    self.assertEqual(repr(node), f'HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})')

  def test_leaf_to_html(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    test_props = dict()
    test_props["href"] = "https://google.com/"
    node = LeafNode("a", "Hello, world!", props=test_props)
    self.assertEqual(node.to_html(), '<a href="https://google.com/">Hello, world!</a>')
    node = LeafNode("a", "Hello, world!")
    with self.assertRaises(AttributeError):
      node.to_html()
  
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

if __name__ == "__main__":
  unittest.main()