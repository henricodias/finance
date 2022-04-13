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
