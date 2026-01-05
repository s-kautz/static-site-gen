class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError
  
  def props_to_html(self):
    try:
      html_props = ""
      for key in self.props.keys():
        html_props += f' {key}="{self.props[key]}"'
      return html_props
    except:
      raise AttributeError(f"ERROR: No properties in {self.props}")
  
  def __repr__(self):
    return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super(LeafNode, self).__init__(tag=tag, value=value, children=None, props=props)
  
  def to_html(self):
    if self.value == None:
      raise ValueError("ERROR: LeafNode has no value")
    if self.tag == "a" and not "href" in self.props.keys():
      raise ValueError("ERROR: LeafNode link has no target")
    if self.props:
      return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super(ParentNode, self).__init__(tag=tag, value=None, children=children, props=props)
  
  def to_html(self):
    if not self.tag:
      raise ValueError("ParentNode has no tag")
    if not self.children:
      raise ValueError("ParentNode has no children")
    child_html = ""
    for child in self.children:
      child_html += child.to_html()
    if self.props:
      return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
    return f"<{self.tag}>{child_html}</{self.tag}>"