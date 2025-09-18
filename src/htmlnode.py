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
      raise ValueError(f"ERROR: No properties in {self.props}")
  
  def __repr__(self):
    return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'