import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import talib
import seaborn as sns
import statsmodels.api as sm

#configura parâmetros da biblioteca pandas
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)
pd.set_option('mode.chained_assignment', None)

#importa dados do ativo
ativo = 'PETR4'
mt5.initialize()
mt5.symbol_select(ativo)

df = mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_D1, 0, 5000)
df = pd.DataFrame(df)
df['time'] = pd.to_datetime(df['time'], unit='s')

#machine learning
#print(df)

df['close'].plot(label="PETR4", legend=True)
plt.show()
plt.clf()

#plota retorno em forma de histograma
df['close'].pct_change().plot.hist(bins=50)
plt.show()
plt.clf()

pacoteDeDias = 5
df['dias_no_futuro'] = df['close'].shift(pacoteDeDias)
df['dias_no_futuro_retorno'] = df['dias_no_futuro'].pct_change(pacoteDeDias)
df['dias_atuais_retorno'] = df['close'].pct_change(pacoteDeDias)
print(df.tail(10))

correlacao = df[['dias_atuais_retorno', 'dias_no_futuro_retorno']].corr()
print("Correção: " +str(correlacao))

plt.scatter(df['dias_atuais_retorno'],df['dias_no_futuro_retorno'])
plt.show()
plt.clf()