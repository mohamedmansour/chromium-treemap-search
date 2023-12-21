import argparse
import os
import subprocess
import sys

from tree_utils import Node, Tree


def main():
  parser = argparse.ArgumentParser(description='Generate a treemap of the chromium source code')
  parser.add_argument('query', nargs='+', help='The query to generate the treemap for')
  parser.add_argument('--filter', nargs='+', help='Filter the results by the given patterns', default=['*.cc', '*.h'])
  parser.add_argument('--output', '-o', help='The output file to write to')
  parser.add_argument('--src', help='The source directory', default='~/chromium/src')

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()

  grep_query = '-e ' + ' -e '.join(f'"{item}"' for item in args.query)
  grep_filter = '-name ' + ' -o -name '.join(f'"{item}"' for item in args.filter)
  cwd = os.path.expanduser(args.src)

  print(f'Searching for: {grep_query}')
  print(f'Filtering for: {grep_filter}')
  print(f'CWD: {cwd}')

  command = f'find . -type f -not -path "./out/*" -not -path "./.git/*" {grep_filter} | xargs grep -l {grep_query} | sort | uniq'
  process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=cwd)
  output, error = process.communicate()
  
  if error:
    sys.exit(f"Error: {error}")

  lines = output.decode().split('\n')
  print(f'Found {len(lines)} files')

  # Build the tree.
  treemap = Node()
  treemap.size = 0

  # Add each file to the tree.
  for line in lines:
      path = line.strip()
      paths = path.split('/')
      current_node = treemap

      # Add each path to the tree.
      for path in paths[:-1]:
        child = current_node.get_child_by_id(path)
        
        # Create a new node if it doesn't exist.
        if not child:
          child = Node(path)
          child.size = 0
          current_node.add_child(child)
        else:
          child.size += 1
        current_node = child

      # Add the leaf node.
      leaf_node = Node(paths[-1])
      leaf_node.size = 1
      current_node.add_child(leaf_node)

  # Sort a flatten the tree, remove root since it's not needed.
  root = treemap.children[0]
  root.id = ', '.join(args.query)
  tree = Tree(root)
  tree.sort()
  tree.flatten()

  # Write the tree to a file.
  with open('data.json', 'w') as file:
    file.write(tree.toJSON())

if __name__ == '__main__':
  main()
