import time
import random
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import talib

#configura parâmetros da biblioteca pandas
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)
pd.set_option('mode.chained_assignment', None)

#define ativo
ativo = 'WINJ22'
mt5.initialize()
mt5.symbol_select(ativo)

stopLoss = 500
takeProfit = 500


def ordem_fechamento(ativo, quantidade, ticket, type_order, magic, deviation):
    if(type_order == 0):
        print("ORDEM DE VENDA - FECHAMENTO")
        request_fechamento = {
            "action": mt5.TRADE_ACTION_DEAL,
            "postion": ticket,
            "symbol": ativo,
            "volume": quantidade,
            "deviation": deviation,
            "magic": magic,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(ativo).ask,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }

        resultado = mt5.order_send(request_fechamento)
        print(resultado)
    else:
        print("ORDEM DE COMPRA - FECHAMENTO")
        request_fechamento = {
            "action": mt5.TRADE_ACTION_DEAL,
            "postion": ticket,
            "symbol": ativo,
            "volume": quantidade,
            "deviation": deviation,
            "magic": magic,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(ativo).bid,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN
        }
        resultado = mt5.order_send(request_fechamento)
        print(resultado)

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
        "sl": price + stopLoss * point,
        "tp": price - takeProfit * point,
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
        "sl": price - stopLoss * point,
        "tp": price + takeProfit * point,
        "deviation": deviation,
        "magic": 10032021,
        "comment": "Ordem de Compra Enviada",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }
    resultado = mt5.order_send(request)
    return resultado

#coleta dados do ativo
df = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 1, 5000)
df = pd.DataFrame(df)
df['time'] = pd.to_datetime(df['time'], unit='s')
df = df.set_index('time') #tempo em index

#criação das médias
df['ema9'] = talib.EMA(df['close'].values, timeperiod=9)
df['ema21'] = talib.EMA(df['close'].values, timeperiod=21)

while True:
    totalOrdens = mt5.positions_total()
    dr = pd.DataFrame()
    dr = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 1)
    dr = pd.DataFrame(dr)
    dr['time'] = pd.to_datetime(dr['time'], unit='s')
    dr = dr.set_index('time')  # tempo em index
    dr = dr.append(dr)
    df['ema9'] = talib.EMA(df['close'].values, timeperiod=9)
    df['ema21'] = talib.EMA(df['close'].values, timeperiod=21)
    df['signal'] = np.sign(df['ema9'] - df['ema21'])
    print(df)


    if(totalOrdens == 0):
        if(df['signal'].iloc[-1] == 1):
            print(compra())
            totalOrdens = mt5.positions_total()
        else:
            print(venda())
            totalOrdens = mt5.positions_total()
    elif(totalOrdens == 1):
        infoPosicoes = mt5.positions_get(symbol=ativo)
        dataPosicoes = pd.DataFrame(list(infoPosicoes), columns=infoPosicoes[0]._asdict().keys())

        if(dataPosicoes['type'][0] == 0 and df['signal'].iloc[-1] == -1):
            print(ordem_fechamento((str(dataPosicoes['symbol'][0]),
                                    float(dataPosicoes['volume'][0]),
                                    int(dataPosicoes['ticket'][0]),
                                    dataPosicoes['type'][0]),
                                   int(dataPosicoes['magic'][0]),
                                   0))
            print(venda())

        if (dataPosicoes['type'][0] == 1 and df['signal'].iloc[-1] == 1):
            print(ordem_fechamento((str(dataPosicoes['symbol'][0]),
                                    float(dataPosicoes['volume'][0]),
                                    int(dataPosicoes['ticket'][0]),
                                    dataPosicoes['type'][0]),
                                   int(dataPosicoes['magic'][0]),
                                   0))
            print(compra())

    time.sleep(60)