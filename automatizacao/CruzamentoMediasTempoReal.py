import MetaTrader5 as mt5
from datetime import datetime
import talib
import time
import pandas as pd
import numpy as np


#configura parâmetros do Pandas
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)
pd.set_option('mode.chained_assignment', None)

#define ativo
ativo = 'WINJ22'
mt5.initialize()
mt5.symbol_select(ativo)

stopLoss = 500
takeProfit = 500
gatilho = 40
gap = 10


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


while True:
    totalOrdens = mt5.positions_total()
    df = pd.DataFrame()
    df = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 1, 50)
    df = pd.DataFrame(df)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.set_index('time')

    #Data Frame Auxiliar
    dr = pd.DataFrame()
    dr = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 1)
    dr = pd.DataFrame(dr)
    dr['time'] = pd.to_datetime(dr['time'], unit='s')
    dr = dr.set_index('time')
    df = df.append(dr)

    #Define os indicadores e condições
    df['ema9'] = talib.EMA(df['close'].values, timeperiod=9)
    df['ema21'] = talib.EMA(df['close'].values, timeperiod=21)
    df['signal'] = np.sign(df['ema9'] - df['ema21'])
    df['diff'] = df['ema9'] - df['ema21']

    #Imprime o que está acontecendo
    print('\n' + '=' * 50)
    print('NOVO SINAL | {}'.format(datetime.now()))
    print('=' * 50)
    print(df.iloc[-1].tail())

    #Condições de operações
    if(totalOrdens == 0):
        if(np.abs(df['diff'].iloc[-1]) < gatilho and np.abs(df['diff'].iloc[-1]) >= gap and df['close'].iloc[-1] > df['ema21'].iloc[-1]):
            if(df['signal'].iloc[-1] == 1):
                print(compra())
                print('ORDEM DE COMPRA ENVIADA')
                totalOrdens = mt5.positions_total()
            elif(np.abs(df['diff'].iloc[-1]) < 50 and np.abs(df['diff'].iloc[-1]) >= 10 and df['close'].iloc[-1] > df['ema21'].iloc[-1]):
                print(venda())
                print('ORDEM DE VENDA ENVIADA')
                totalOrdens = mt5.positions_total()
            else:
                print('NÃO FAZ NADA')
    elif(totalOrdens == 1):
        infoPosicoes = mt5.positions_get(symbol=ativo)
        dataPosicoes = pd.DataFrame(list(infoPosicoes), columns=infoPosicoes[0].as_adict().keys)

        if (dataPosicoes['type'][0] == 0 and df['signal'].iloc[-1] == -1):
            print(ordem_fechamento((str(dataPosicoes['symbol'][0]),
                                    float(dataPosicoes['volume'][0]),
                                    int(dataPosicoes['ticket'][0]),
                                    dataPosicoes['type'][0]),
                                   int(dataPosicoes['magic'][0]),
                                   0))
            print(venda())
            print('venda')

        if (dataPosicoes['type'][0] == 1 and df['signal'].iloc[-1] == 1):
            print(ordem_fechamento((str(dataPosicoes['symbol'][0]),
                                    float(dataPosicoes['volume'][0]),
                                    int(dataPosicoes['ticket'][0]),
                                    dataPosicoes['type'][0]),
                                    int(dataPosicoes['magic'][0]),
                                    0))
            print(compra())
            print('compra')


    time.sleep(1)
