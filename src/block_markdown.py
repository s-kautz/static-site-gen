import re
from blocknode import BlockType

def markdown_to_blocks(markdown):
  block_delimiter = r"(\n\s*\n)"
  blocks = re.split(pattern=block_delimiter, string=markdown)
  blocks[:] = [block.strip() for block in blocks if not block.strip() == ""]

  return blocks

def block_to_block_type(mdblock):
  heading_pattern = r"#{1,6} [\s\S]*"
  code_pattern = r"```\n[\s\S]*```"
  quote_pattern = r">[\s\S]*"
  ul_line_pattern = r"- [\s\S]*"

  if re.match(heading_pattern, mdblock):
    return BlockType.HEADING
  if re.match(code_pattern, mdblock):
    return BlockType.CODE
  if re.match(quote_pattern, mdblock):
    return BlockType.QUOTE
  lines = mdblock.split("\n")
  is_list = True
  for line in lines:
    if not re.match(ul_line_pattern, line):
      is_list = False
  if is_list:
    return BlockType.UL
  is_list = True
  for i in range(1, len(lines)+1):
    ol_line_pattern = fr"{i}\. [\s\S]*"
    if not re.match(ol_line_pattern, line):
      is_list = False
  if is_list:
    return BlockType.OL
  return BlockType.PARAGRAPH

