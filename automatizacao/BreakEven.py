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
def venda(quantidade):
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
def compra(quantidade):
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

#coleta o valor disponível para operar:
def ColetaValorDisponivel():
    #print('retorna a margem')
    accountInfo = mt5.account_info()
    accountInfoDict = mt5.account_info()._asdict()
    df = pd.DataFrame(list(accountInfoDict.items()), columns=['property', 'value'])
    balance = df['value'][10]

    return balance

while True:
    if (VerificaHorarioOperacoes() and ColetaValorDisponivel() > 400):
        totalOrdens = mt5.positions_total()
        df = pd.DataFrame()
        df = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 1, 50) #verificar
        df = pd.DataFrame(df)
        df['time'] = pd.to_datetime(df['time'], units='s')
        df = df.set_index('time')

        #Data Frame auxiliar:
        df = pd.DataFrame()
        df = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 1)
        dr = pd.DataFrame(dr)
        dr['time'] = pd.to_datetime(dr['time'], unit='s')
        dr = dr.set_index('time')
        df = df.append(dr)

        #bandas de bollinger
        df['banda_alta'] = getBandas(df, 20, qtdDesvios)['upper']
        df['banda_baixa'] = getBandas(df, 20, qtdDesvios)['lower']
        df['media'] = getBandas(df, 20, qtdDesvios)['middle']
        df['diff_upper_low'] = df['banda_alta'] - df['banda_baixa']

        df['kama'] - talib.KAMA(df['close'].values, timeperiod=9)

        #imprime o que está acontecendo:
        print('\n' + '=' * 50)
        print('NOVO SINAL | {}'.format(datetime.now()))
        print('=' * 50)
        print(df.iloc[-1].tail())

        precoAtual = df['close'].iloc[-1]
        valorIndicador = df['kama'].iloc[-1]
        difMediaPrecoAtual = np.abs(valorIndicador - precoAtual)
        # bandaInferior = df['banda_baixa'].iloc[-1]
        # bandaSuperior = df['banda_alta'].iloc[-1]
        # diferencaBandas = df['diff_upper_low'].iloc[-1]

        breakEven = False
        breakEvenPontos = 50

        #abertura de posição
        if (totalOrdens == 0):
            breakEven = False
            if (precoAtual >= valorIndicador and difMediaPrecoAtual <= 50):
                print(compra(qtdContratos))
            elif (precoAtual <= valorIndicador and difMediaPrecoAtual <= 50):
                print(venda(qtdContratos))
        elif (totalOrdens == 1):
            infoPosicoes = mt5.positions_get(symbol=ativo)
            dataPosicoes = pd.Dataframe(list(infoPosicoes), columns=infoPosicoes[0]._asdict().keys())

            #diferença do preço de operação para o preço atual
            difAtualOperacao = np.abs(dataPosicoes['price_open'][0] - precoAtual)
            precoOperacao = dataPosicoes['price_open'][0]

            if (difAtualOperacao >= 100):
                breakEven = True

            if (breakEven):
                if (dataPosicoes['type'][0] == 0 and (precoAtual <= precoOperacao + breakEvenPontos or precoAtual <= valorIndicador)):
                    print(ordem_fechamento(str(dataPosicoes['symbol'][0]),
                                           float(dataPosicoes['volume'][0]),
                                           int(dataPosicoes['ticket'][0]),
                                           dataPosicoes['type'][0],
                                           int(dataPosicoes['magic'][0]),
                                           0))
                    totalOrdens = 0
                    breakEven = False
                if(dataPosicoes['type'][0] == 1 and (precoAtual >= precoOperacao - breakEvenPontos or precoAtual >= valorIndicador)):
                    print(ordem_fechamento(str(dataPosicoes['symbol'][0]),
                                           float(dataPosicoes['volume'][0]),
                                           int(dataPosicoes['ticket'][0]),
                                           dataPosicoes['type'][0],
                                           int(dataPosicoes['magic'][0]),
                                           0))
                    totalOrdens = 0
                    breakEven = False
            else:
                if (dataPosicoes['type'][0] == 0 and (precoAtual <= valorIndicador and valorIndicador >= precoOperacao)):
                    print(ordem_fechamento(str(dataPosicoes['symbol'][0]),
                                           float(dataPosicoes['volume'][0]),
                                           int(dataPosicoes['ticket'][0]),
                                           dataPosicoes['type'][0],
                                           int(dataPosicoes['magic'][0]),
                                           0))
                    totalOrdens = 0
                if (dataPosicoes['type'][0] == 1 and (precoAtual >= valorIndicador and valorIndicador <= precoOperacao)):
                    print(ordem_fechamento(str(dataPosicoes['symbol'][0]),
                                           float(dataPosicoes['volume'][0]),
                                           int(dataPosicoes['ticket'][0]),
                                           dataPosicoes['type'][0],
                                           int(dataPosicoes['magic'][0]),
                                           0))
                    totalOrdens = 0
        else:
            print("NOTHING")
        time.sleep(1)
    mt5.shutdown()