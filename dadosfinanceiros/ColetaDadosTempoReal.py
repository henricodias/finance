import MetaTrader5 as mt5
import time

mt5.initialize()

ativo = 'WINJ22'

while(True):
    time.sleep(0.5)
    print(mt5.symbol_info_tick(ativo).last)


