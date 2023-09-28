import pandas as pd


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
        "lexeme": "4",
        "nroline": 2,
        "col": 2
    },
    {
        "symbol": "*",
        "lexeme": "*",
        "nroline": 2,
        "col": 4
    },
    {
        "symbol": "int",
        "lexeme": "5",
        "nroline": 2,
        "col": 6
    },
    {
        "symbol": "$",
        "lexeme": "$",
        "nroline": 0,
        "col": 0
    },
]

while len(stack) > 0: 
  for item in stack:
    print(f"Symbol: {item.symbol}, Lexeme: {item.lexeme}, ID: {item.id}")

  if stack[-1].symbol == '$' and input[0]["symbol"] == '$':
    print("\nLa gramatica es correcta")
    break

  production = tabla.at[stack[-1].symbol, input[0]["symbol"]]

  if production != 'e':
    production_terms = production.split()
    node_p = stack.pop()
    for term in reversed(production_terms):
      if term == input[0]["symbol"]:
        #nodo hoja
        node_h = term
        input.pop(0)
        continue
      new_node = NodeStack(term, None)
      stack.append(new_node)
  elif production == ' ':
    print("La gramatica es incorrecta")
  else:
    # Producción vacía, desapila
    node_h = stack.pop()
    continue

# crear los hijo X y T de E
#node_X_tree = NodeTree(node_X.id, node_X.symbol, node_X.lexeme)
#node_T_tree = NodeTree(node_T.id, node_T.symbol, node_T.lexeme)
#node_father = buscar_node(node_p.id)
#node_father.children.append(node_X_tree)
#node_father.children.append(node_T_tree)
#node_X_tree.father = node_father
#node_T_tree.father = node_father
