import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT or delimiter not in old_node.text:
      new_nodes.append(old_node)
      continue
    text = old_node.text
    if text.count(delimiter) % 2 != 0:
      raise ValueError("ERROR: Delimiter in string not closed")
    apply_text_type = True
    substrings = text.split(delimiter)
    for substring in substrings:
      apply_text_type = not apply_text_type
      if substring == "":
        continue
      if apply_text_type:
        new_nodes.append(TextNode(text=substring, text_type=text_type))
      else:
        new_nodes.append(TextNode(text=substring, text_type=TextType.TEXT))
  return new_nodes

'''
To-Do:
- refactor according to course:
define pattern
gather matches
return matches (empty list if no matches)
'''
def extract_markdown_images(text):
  images = re.findall(r"!\[.*?\]\(.*?\)", text)
  tuples = []
  if not images:
    raise ValueError("ERROR: No image in string")
  for image in images:
    alt_text = re.findall(r"\[.*?\]", image)[0].strip("[]")
    url = re.findall(r"\(.*?\)", image)[0].strip("()")
    tuples.append((alt_text, url))
  return tuples

def extract_markdown_links(text):
  links = re.findall(r"\[.*?\]\(.*?\)", text)
  tuples = []
  if not links:
    raise ValueError("ERROR: No link in string")
  for link in links:
    anchor_text = re.findall(r"\[.*?\]", link)[0].strip("[]")
    url = re.findall(r"\(.*?\)", link)[0].strip("()")
    tuples.append((anchor_text, url))
  return tuples

'''
To-Do:
- Use extract_markdown_images once, iterate matches, and split(f"![{alt}]({url})", 1) to increase efficiency.
'''
def split_nodes_image(old_nodes):
  if not old_nodes:
    return []
  new_nodes = []
  for node in old_nodes:
    if re.search(r"!\[.*?\]\(.*?\)", node.text) and node.text_type == TextType.TEXT:
      link_tuple = extract_markdown_images(node.text)[0]
      parts = node.text.split(f"![{link_tuple[0]}]({link_tuple[1]})")
      if len(parts) != 2:
        raise ValueError("ERROR: Invalid markdown, image section not closed")
      if parts[0] != "":
        new_nodes.append(TextNode(parts[0], TextType.TEXT))
      new_nodes.append(TextNode(link_tuple[0], TextType.IMAGE, link_tuple[1]))
      if parts[1] != "":
        for new_node in split_nodes_image([TextNode(parts[1], TextType.TEXT)]):
          new_nodes.append(new_node)
    else:
      new_nodes.append(node)
  return new_nodes

def split_nodes_link(old_nodes):
  if not old_nodes:
    return []
  new_nodes = []
  for node in old_nodes:
    if re.search(r"\[.*?\]\(.*?\)", node.text) and node.text_type == TextType.TEXT:
      link_tuple = extract_markdown_links(node.text)[0]
      parts = node.text.split(f"[{link_tuple[0]}]({link_tuple[1]})")
      if len(parts) != 2:
        raise ValueError("ERROR: Invalid markdown, link section not closed")
      if parts[0] != "":
        new_nodes.append(TextNode(parts[0], TextType.TEXT))
      new_nodes.append(TextNode(link_tuple[0], TextType.LINK, link_tuple[1]))
      if parts[1] != "":
        for new_node in split_nodes_link([TextNode(parts[1], TextType.TEXT)]):
          new_nodes.append(new_node)
    else:
      new_nodes.append(node)
  return new_nodes

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  return nodes