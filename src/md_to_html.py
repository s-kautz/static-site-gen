import textnode, block_markdown, inline_markdown, htmlnode

def markdown_to_html_node(markdown):
  blocks = block_markdown.markdown_to_blocks(markdown)
  for block in blocks:
    block = block_markdown.block_to_block_type(block)