import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):

    '''
    Delim split test cases
    '''
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
        new_nodes
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and _italic_", TextType.TEXT),
            ],
            new_nodes
        )
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_incomplete(self):
        node = TextNode("This is text **with and unclosed delimiter.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_complete_and_incomplete(self):
        node = TextNode("This is text with **one closed** and **one unclosed delimiter.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    '''
    Image extraction test cases
    '''
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("another image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_with_link(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [regular link](https://google.com/)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_malformed_image(self):
        text = "This is text with an incomplete ![image link](https://i.imgur.com/zjjcJKZ.png in the middle"
        with self.assertRaises(ValueError):
            extract_markdown_images(text)

    '''
    Link extraction test cases
    '''
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://imgur.com/), isn't that wild?"
        )
        self.assertListEqual([("link", "https://imgur.com/")], matches)

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        self.assertListEqual(split_nodes_image([node]), [TextNode("This is text with an ", TextType.TEXT), (TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))])

    def test_split_nodes_multiple_images_trailing_text(self):
        node = TextNode("This is text with two images: this ![image](https://i.imgur.com/zjjcJKZ.png), and ![this image](https://i.imgur.com/zjjcJKZ.png) as well.", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with two images: this ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", and ", TextType.TEXT),
                TextNode("this image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" as well.", TextType.TEXT)
            ]
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](https://i.imgur.com/)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/")
            ]
        )

    def test_split_nodes_multiple_links_trailing_text(self):
        node = TextNode("This is text with two links: this [link](https://imgur.com/), and [this link](https://google.com/) as well.", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with two links: this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://imgur.com/"),
                TextNode(", and ", TextType.TEXT),
                TextNode("this link", TextType.LINK, "https://google.com/"),
                TextNode(" as well.", TextType.TEXT)
            ]
        )

    def test_text_to_textnodes(self):
        matches = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(matches, 
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        )
