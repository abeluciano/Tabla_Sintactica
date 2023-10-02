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
        "lexeme": "$",
        "nroline": 0,
        "col": 0
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
    
    for item in stack:
      print(f"Symbol: {item.symbol}, Lexeme: {item.lexeme}, ID: {item.id}")
  
    if stack[-1].symbol == '$' and input[0]["symbol"] == '$':
      print("\nLa gramatica es correcta\n")
      break
    print(stack[-1].symbol, input[0]["symbol"])

    
    if stack[-1].symbol == input[0]["symbol"]:
      node_h = stack[-1].symbol
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
          #nodo hoja
          node_h = term
          input.pop(0)
          continue
        new_node = NodeStack(term, None)
        stack.append(new_node)
      
    elif production == ' ':
      print("Error sintactico en linea:", input[0]["nroline"])
  
    else:
      # Producción vacía, desapila
      node_h = stack.pop()
      continue