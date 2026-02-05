import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestTextNode(unittest.TestCase):
  def test_markdown_to_blocks(self):
    test_markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
    test_blocks = markdown_to_blocks(test_markdown)
    self.assertEqual(
      test_blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
      ],
    )
  
  def test_markdown_to_blocks_leading_and_trailing_spaces(self):
    test_markdown = """
This is a regular paragraph.

 This is a paragraph with a leading space

This is a paragraph with a trailing space """
    test_blocks = markdown_to_blocks(test_markdown)
    self.assertEqual(
      test_blocks,
      [
        "This is a regular paragraph.",
        "This is a paragraph with a leading space",
        "This is a paragraph with a trailing space",
      ],
    )

  def test_markdown_to_blocks_paragraph_with_linebreaks(self):
    test_markdown = """
This is a regular paragraph.

This is a paragraph that
continues after a linebreak."""
    test_blocks = markdown_to_blocks(test_markdown)
    self.assertEqual(
      test_blocks,
      [
        "This is a regular paragraph.",
        "This is a paragraph that\ncontinues after a linebreak."
      ],
    )
  
  def test_block_to_block_type_paragraph(self):
    mdblock = "This is a regular paragraph"
    self.assertEqual(block_to_block_type(mdblock), BlockType.PARAGRAPH)
  
  def test_block_to_block_type_h1_heading(self):
    mdblock = "# This is an H1 heading"
    self.assertEqual(block_to_block_type(mdblock), BlockType.HEADING)

  def test_block_to_block_type_h6_heading(self):
    mdblock = "###### This is an H1 heading"
    self.assertEqual(block_to_block_type(mdblock), BlockType.HEADING)

  def test_block_to_block_type_malformat_heading_too_deep(self):
    mdblock = "####### This is an H7 heading"
    self.assertEqual(block_to_block_type(mdblock), BlockType.PARAGRAPH)

  def test_block_to_block_type_malformat_heading_no_space(self):
    mdblock = "#This is an H1 heading with no space"
    self.assertEqual(block_to_block_type(mdblock), BlockType.PARAGRAPH)

  def test_block_to_block_type_code(self):
    mdblock = """
```SomeCode
This is a test code block
```
"""
    self.assertEqual(block_to_block_type(mdblock), BlockType.CODE)

  def test_block_to_block_type_code(self):
    mdblock = """
```SomeCode
This is an unclosed code block
"""
    self.assertEqual(block_to_block_type(mdblock), BlockType.PARAGRAPH)

  def test_block_to_block_type_quote_space(self):
    mdblock = "> This is a quote"
    self.assertEqual(block_to_block_type(mdblock), BlockType.QUOTE)

  def test_block_to_block_type_quote_no_space(self):
    mdblock = ">This is a quote without a leading space"
    self.assertEqual(block_to_block_type(mdblock), BlockType.QUOTE)
  
  def test_block_to_block_type_unordered_list(self):
    mdblock = """
- This is an unordered list item
- And this is another one
"""
    self.assertEqual(block_to_block_type(mdblock), BlockType.UL)

  def test_block_to_block_type_unordered_list(self):
    mdblock = """
- This is an unordered list item
-And this is a malformatted one
"""
    self.assertEqual(block_to_block_type(mdblock), BlockType.PARAGRAPH)
  
  def test_block_to_block_type_ordered_list(self):
    mdblock = """
1. This is an ordered list item
2. And this is another one
"""
    self.assertEqual(block_to_block_type(mdblock), BlockType.OL)
  
  def test_block_to_block_type_ordered_list(self):
    mdblock = """
1. This is an ordered list item
3. And this is an out of order one
"""
    self.assertEqual(block_to_block_type(mdblock), BlockType.PARAGRAPH)
  
  def test_block_to_block_type_ordered_list(self):
    mdblock = """
1. This is an ordered list item
2.And this is a malformatted one
"""
    self.assertEqual(block_to_block_type(mdblock), BlockType.PARAGRAPH)

