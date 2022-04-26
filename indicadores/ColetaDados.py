import pandas as pd
import MetaTrader5 as mt5
import datetime as dt

# define as variáveis de controle
frameTrintaMinutos = mt5.TIMEFRAME_M30
frameUmaHora = mt5.TIMEFRAME_H1
frameUmDia = mt5.TIMEFRAME_D1

# define a função de coleta dos dados
def getDados(timeFrame, ativo = "PETR4"):
    qtdCandles = 1000
    posInicial = 0
    if not mt5.initialize():
        print("Não tem MT5 funcionando")
        quit()

    mt5.symbol_select(ativo)
    rates = mt5.copy_rates_from_pos(ativo, timeFrame, posInicial, qtdCandles)
    ratesFrame = pd.DataFrame(rates)

    return ratesFrame

df = getDados(frameUmDia, "VALE3")

print(df)