import MetaTrader5 as mt5

mt5.initialize()

simbolos = mt5.symbols_get()

contador = 0

for simbolo in simbolos:
    contador += 1
    print("{}. {}".format(contador, simbolo.name))
    if contador == 5: break


petr_simbolos = mt5.symbols_get("*PETR*")
print(len(petr_simbolos))

for simbolos in petr_simbolos:
    print(simbolos.name)


print("Simbolos", len(simbolos))

mt5.shutdown()