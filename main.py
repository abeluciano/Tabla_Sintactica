import pandas as pd
import sys

class NodeStack:

  def __init__(self, symbol, lexeme):
    global count
    self.symbol = symbol
    self.lexeme = lexeme
    self.id = count + 1
    count += 1


class NodeTree:

  def __init__(self, id, symbol, lexeme):
    self.id = id
    self.symbol = symbol
    self.lexeme = lexeme
    self.children = []
    self.father = None


def buscar_node(root_node, target_id):
  stack = [root_node]
  while stack:
    current_node = stack.pop()
    if current_node.id == target_id:
      return current_node
    stack.extend(current_node.children)
  return None


tabla = pd.read_csv("tabla.csv", index_col=0)
count = 0
stack = []

# Inicializa la pila
symbol_E = NodeStack('E', None)
symbol_dollar = NodeStack('$', None)
stack.append(symbol_dollar)
stack.append(symbol_E)

# Inicializa el árbol
root = NodeTree(symbol_E.id, symbol_E.symbol, symbol_E.lexeme)

input = [

    {
        "symbol": "int",
        "lexeme": "*",
        "nroline": 2,
        "col": 4
    },
  
    {
        "symbol": "+",
        "lexeme": "$",
        "nroline": 0,
        "col": 0
    },
  
    {
        "symbol": "int",
        "lexeme": "$",
        "nroline": 0,
        "col": 0
    },
    {
        "symbol": "$",
        "lexeme": "$",
        "nroline": 0,
        "col": 0
    },
]

if (
  stack[-1].symbol not in tabla.index or
  input[0]["symbol"] not in tabla.columns
):
  print("\nLa gramatica es incorrecta")
else:
  while len(stack) > 0:
    
    if stack[-1].symbol == '$' and input[0]["symbol"] == '$':
      print("\nLa gramatica es correcta\n")
      break

    if stack[-1].symbol == input[0]["symbol"]:
      input.pop(0)
      stack.pop()

    elif stack[-1].symbol not in tabla.index:
      print("Error sintactico en linea:", input[0]["nroline"])
      break

    production = tabla.at[stack[-1].symbol, input[0]["symbol"]]

    if production != 'e':
      production_terms = production.split()
      node_p = stack.pop()
      for term in reversed(production_terms):
        if term == input[0]["symbol"]:
          new_node = NodeStack(term, None)
          node_h = NodeTree(new_node.id,new_node.symbol, new_node.lexeme)
          node_father = buscar_node(root, node_p.id)
          node_father.children.append(node_h)
          node_h.father = node_father
          input.pop(0)
          continue
        new_node = NodeStack(term, None)
        new_node_tree = NodeTree(new_node.id, new_node.symbol, new_node.lexeme)
        node_father = buscar_node(root, node_p.id)
        node_father.children.append(new_node_tree)
        new_node_tree.father = node_father
        stack.append(new_node)

    elif production == ' ':
      print("Error sintactico en linea:", input[0]["nroline"])

    elif production == 'e':
      node_p = stack.pop()
      new_node = NodeStack("e", "e")
      node_h = NodeTree(new_node.id,new_node.symbol, new_node.lexeme)
      node_father = buscar_node(root, node_p.id)
      node_father.children.append(node_h)
      node_h.father = node_father
      continue

def printto_file(node, filename):
  with open(filename, "w") as file:
    sys.stdout = file  
    if node is not None:
      printfrom_tree(node)
    sys.stdout = sys.__stdout__  

def printfrom_tree(node):
  if node is None:
    return
  if node.father is not None:
    production = f"{node.father.symbol}_{node.father.id} -> {node.symbol}_{node.id}"
    print(production)
  for child in node.children:
    printfrom_tree(child)
output_filename = "graphviz.txt"
printto_file(root, output_filename)

