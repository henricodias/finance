import yfinance as yf
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go


acao = yf.Ticker("ITUB4.SA")
data = acao.history(period='1y')
df = data[['Close']]


#calculo da média móvel
mediaMovel = df.rolling(window=20).mean()

#cálculo do desvio padrão
desvioPadrao = df.rolling(window=20).std()

#cáclculo das bandas
bandaSuperior = mediaMovel + 2 * desvioPadrao
bandaInferior = mediaMovel - 2 * desvioPadrao

#altera o nome das colunas de banda sup e banda inf
bandaSuperior = bandaSuperior.rename(columns={'Close': 'superior'})
bandaInferior = bandaInferior.rename(columns={'Close': 'inferior'})

#união das colunas
bandasDeBollinger = df.join(bandaSuperior).join(bandaInferior)

bandasDeBollinger.dropna(inplace=True)

#cálculo dos pontos de compra e venda
compra = bandasDeBollinger[bandasDeBollinger['Close'] <= bandasDeBollinger['inferior']]
venda = bandasDeBollinger[bandasDeBollinger['Close'] >= bandasDeBollinger['superior']]


pio.templates.default = "plotly_dark"
fig = go.Figure()
fig.add_trace(go.Scatter(x=bandaInferior.index,
                         y=bandaInferior['inferior'],
                         name='Banda Inferior',
                         ))

fig.add_trace(go.Scatter(x=bandaSuperior.index,
                         y=bandaSuperior['superior'],
                         name='Banda Superior',
                         fill='tonexty',
                         ))

fig.add_trace(go.Scatter(x=df.index,
                         y=df['Close'],
                         name='Preço de Fechamento',
                         ))

fig.add_trace(go.Scatter(x=mediaMovel.index,
                         y=mediaMovel['Close'],
                         name='Média Móvel',
                         ))

fig.add_trace(go.Scatter(x=compra.index,
                         y=compra['Close'],
                         name='Compra',
                         mode='markers',
                         marker=dict(
                             color='#00CC96',
                             size=8,
                            )
                         ))

fig.add_trace(go.Scatter(x=venda.index,
                         y=venda['Close'],
                         name='Venda',
                         mode='markers',
                         marker=dict(
                             color='#EF553B',
                             size=8,
                            )
                         ))

fig.show()
#print(bandasDeBollinger)
