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

#inicializar o metatrader
mt5.initialize()

#define variáveis do ativo
ativo = 'WINJ22'
selecionado = mt5.symbol_select(ativo)
stopLoss = 100
takeProfit = 500
qtdContratos = float(1)
