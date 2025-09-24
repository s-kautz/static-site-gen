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