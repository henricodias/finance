import MetaTrader5 as mt5

mt5.initialize()

simbolos = mt5.symbols_total()

if simbolos > 0:
    print("Total de símbolos encontrados: ", simbolos)
else:
    print("Nenhum símbolo encontrado.")

mt5.shutdown()

