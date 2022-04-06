import time
import random
import MetaTrader5 as mt5
import pandas as pd

mt5.initialize()

ativo = 'WINJ22'

infoPosicoes = mt5.positions_get(symbol=ativo)
totalOrdens = mt5.positions_total()
tipoDeOrdem = [0,1]

#coleta dados do ativo
# df = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M15, 0, 5000)
# df = pd.DataFrame(df)
# df['time'] = pd.to_datetime(df['time'], unit='s')
# df = df.set_index('time') #tempo em index
# df['diff_hl'] = df['high'] - df['low']
# df['loss'] = df['diff_hl'].mean()

def venda():
    print("ORDEM DE VENDA ENVIADA")
    lot = float(1)
    symbol = ativo
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).last
    deviation = 5
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + stop_loss * point,
        "tp": price - take_profit * point,
        "deviation": deviation,
        "magic": 10032021,
        "comment": "Ordem de Venda Enviada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    resultado = mt5.order_send(request)
    return resultado

def compra():
    print("ORDEM DE COMPRA ENVIADA")
    lot = float(1)
    symbol = ativo
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).last
    deviation = 5
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - stop_loss * point,
        "tp": price + take_profit * point,
        "deviation": deviation,
        "magic": 10032021,
        "comment": "Ordem de Compra Enviada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    resultado = mt5.order_send(request)
    return resultado



mt5.shutdown()