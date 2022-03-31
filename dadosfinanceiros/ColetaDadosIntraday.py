import MetaTrader5 as mt5
import pandas as pd
import pytz
from datetime import datetime

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

timezone = pytz.timezone("ETC/UTC")

data_hoje = datetime.today().strftime('%Y-%m-%d')
data_hoje_pregao = data_hoje + "-10:00:00"

diff_inicio_pregao = datetime.today() - pd.Timestamp(data_hoje_pregao)
minutos = 5
quantidade_barras = int(diff_inicio_pregao.total_seconds() / (minutos * 60))

mt5.initialize()

ativo = "PETR4"

barras = mt5.copy_rates_from(ativo, mt5.TIMEFRAME_M5, datetime.today(), quantidade_barras)
barras_frame = pd.DataFrame(barras)
barras_frame['time'] = pd.to_datetime(barras_frame['time'], unit='s')
barras_hoje = barras_frame[barras_frame['time'] >= data_hoje_pregao].reset_index(drop=True)



print(barras_hoje)