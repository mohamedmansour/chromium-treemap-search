import json


class Node(object):
  """ Simple Node class that has many children """
  def __init__(self, id='root', children=None):
    self.id = id
    self.children = []
    self.size = 0
    self.data = None
    if children is not None:
      for child in children:
          self.add_child(child)

  def add_child(self, node):
    assert isinstance(node, Node)
    self.children.append(node)

  def get_child_by_id(self, id):
    return next((node for node in self.children if id == node.id), None)

class Tree:
  def __init__(self, root):
    assert isinstance(root, Node)
    self.root = root

  def toJSON(self):
    """ Convert the tree to the json dump so the webview can read """
    cleaned_data_fnc = lambda o: { k: v for k, v in o.__dict__.items() if v }
    return json.dumps(self.root,
                      default=cleaned_data_fnc,
                      sort_keys=True, indent=2)

  def sort(self, node=None):
    """ Sort the children by largest size """
    node = node or self.root
    if not node.children:
      return
    for child in node.children:
      self.sort(child)
    node.children.sort(key=lambda node: node.size, reverse=True)

  def flatten(self, node=None):
    """ Flatten the tree if there is just one child """
    node = node or self.root
    if node.children:
      for child in node.children:
        self.flatten(child)
      if len(node.children) == 1:
        child = node.children[0]
        node.id += '/' + child.id
        node.children = child.children
