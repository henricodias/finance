import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import talib
import seaborn as sns
import statsmodels.api as sm
from sklearn.neural_network import MLPClassifier
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import adam_v2, rmsprop_v2
import random

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
df = df.set_index('time') #tempo em index

df['return'] = np.log(df['close'] / df['close'].shift(1))
df.dropna(inplace=True)

colunas = []
lags = 5

for lag in range(1, lags + 1):
    coluna = f'lag_{lag}'
    df[coluna] = df['return'].shift(lag)
    colunas.append(coluna)
df.dropna(inplace=True)

variaveisUteis = ['close', 'return'] + colunas
dfNovo = df[variaveisUteis]
dfNovo['direction'] = np.where(dfNovo['return'] > 0, 1, 0)
otimizador = adam_v2.Adam(learning_rate=0.0001)

def set_seeds(seed = 100):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

set_seeds()

modelo = Sequential()
modelo.add(Dense(64,
                 activation='relu',
                 input_shape=(lags, )))

modelo.add(Dense(64,
                 activation='relu'))

modelo.add(Dense(1,
                 'sigmoid'))

modelo.compile(optimizer=otimizador,
               loss='binary_crossentropy',
               metrics=['accuracy'])

cutoff = '2020-09-01'

dadosDeTreinamento = dfNovo[dfNovo.index < cutoff].copy()
media = dadosDeTreinamento.mean()
desvio = dadosDeTreinamento.std()

dadosDeTreinamentoNormalizado = (dadosDeTreinamento - media) / desvio


#dados de teste
dadosDeTeste = dfNovo[dfNovo.index >= cutoff].copy()
dadosDeTesteNormalizado = (dadosDeTeste - media) / desvio

#treinamento do modelo

modelo.fit(dadosDeTreinamento[colunas],
           dadosDeTreinamento['direction'],
           epochs=50,
           verbose=True,
           validation_split=0.2,
           shuffle=False)

resultado = pd.DataFrame(modelo.history.history)
resultado[['accuracy', 'val_accuracy']].plot(figsize=(10,6), style='--')
#plt.show()

modelo.evaluate(dadosDeTreinamentoNormalizado[colunas], dadosDeTreinamento['direction'])


predicao = np.where(modelo.predict(dadosDeTreinamentoNormalizado[colunas]) > 0.5, 1, 0)
dadosDeTreinamento['prediction'] = np.where(predicao > 0, 1, -1)
dadosDeTreinamento['strategy'] = (dadosDeTreinamento['prediction'] * dadosDeTreinamento['return'])
dadosDeTreinamento[['return', 'strategy']].sum().apply(np.exp)
dadosDeTreinamento[['return', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10,6))


modelo.evaluate(dadosDeTesteNormalizado[colunas], dadosDeTeste['direction'])
predicao1 = np.where(modelo.predict(dadosDeTesteNormalizado[colunas]) > 0.5, 1, 0)
dadosDeTeste['prediction'] = np.where(predicao1 > 0, 1, -1)
dadosDeTeste['strategy'] = (dadosDeTeste['prediction'] * dadosDeTeste['return'])
dadosDeTeste[['return', 'strategy']].sum().apply(np.exp)
dadosDeTeste[['return', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10,6))
plt.show()

#print(dadosDeTreinamento)

#print(dfNovo)