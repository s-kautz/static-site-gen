import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
  def test_eq_identical(self):
    node1 = TextNode("This is a text node", TextType.BOLD, "https://kautz.design/")
    node2 = TextNode("This is a text node", TextType.BOLD, "https://kautz.design/")
    self.assertEqual(node1, node2)
  
  def test_eq_diff_text(self):
    node1 = TextNode("This is a text node", TextType.TEXT)
    node2 = TextNode("This is another text node", TextType.TEXT)
    self.assertNotEqual(node1, node2)
  
  def test_eq_diff_texttype(self):
    node1 = TextNode("This is a text node", TextType.TEXT, "https://kautz.design/")
    node2 = TextNode("This is a text node", TextType.BOLD, "https://kautz.design/")
    self.assertNotEqual(node1, node2)
  
  def test_eq_diff_url(self):
    node1 = TextNode("This is a text node", TextType.TEXT, "https://kautz.design/")
    node2 = TextNode("This is a text node", TextType.TEXT)
    self.assertNotEqual(node1, node2)
  
  def test_text_to_html(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")
  
  def test_text_to_html_image(self):
    node = TextNode("A sample image", TextType.IMAGE, "./imagepath/image.jpg")
    print(node)
    html_node = text_node_to_html_node(node)
    print(html_node.to_html())
    self.assertEqual(html_node.to_html(), f"<img src=\"./imagepath/image.jpg\" alt=\"A sample image\"></img>")

if __name__ == "__main__":
  unittest.main()