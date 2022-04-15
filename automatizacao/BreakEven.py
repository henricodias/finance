import time
import random
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import talib
from datetime import datetime

#configura parâmetros da biblioteca pandas
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)
pd.set_option('mode.chained_assignment', None)

#inicializa o metatrader
mt5.initialize()

#define variáveis do ativo
ativo = 'WINJ22'
selecionado = mt5.symbol_select(ativo)
stopLoss = 100
takeProfit = 500
qtdContratos = float(1)

#define o horário das operações
def VerificaHorarioOperacoes():
    # print('retorna o horario')
    horarioInicioMercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d") + "-10:15:00")
    horarioMeioMercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d") + "-12:30:00")
    horarioTardeMercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d") + "-15:00:00")
    horarioFechamentoMercado = pd.Timestamp(datetime.today().strftime("%Y-%m-%d") + "-17:00:00")

    horaAgora = datetime.now()
    print(horaAgora)

    if (horaAgora >= horarioInicioMercado and horaAgora <= horarioMeioMercado) or (
            horaAgora >= horarioTardeMercado and horaAgora <= horarioFechamentoMercado):
        return True
    else:
        return False

#define a ordem de fechamento
def ordem_fechamento(ativo, quantidade, ticket, type_order, magic, deviation):
    if(type_order == 0):
        print("ORDEM DE VENDA - FECHAMENTO")
        request_fechamento = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
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
            "position": ticket,
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

#define a ordem de venda:
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

#define a ordem de compra:
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


