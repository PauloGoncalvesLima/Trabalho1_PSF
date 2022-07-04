from pathlib import Path
import pandas as pd
from numpy import nan
import yfinance as yf
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

def historicalDay(coin,yesterdayB,todayB):
    df = yf.download(coin, start=str(yesterdayB), end=str(todayB)) 
    return df

#! ICB
#! DI
#! IGMI-C

indice_list = ['IFNC', 'BDRX', 'ICON', 'IEE', 'IFIX', 'IMAT', 'IDIV', 'INDX', 'IMOB', 'MLCX', 'SMLL', 'UTIL', 'IVBX']
base_link = 'http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?'

ativos_codes_dfs = []

for indice in indice_list:
    try:
        ativos_codes_dfs.append(pd.read_html(f"{base_link}Indice={indice}&idioma=pt-br")[0]['Código'])
        print(f'Download do indice: {indice}')
    except ValueError:
        print(f'Não foi possivel fazer o download do indice: {indice}')

base_path = Path(__file__).parent
ativos_codes_dfs.append(pd.read_csv(base_path.joinpath('AGFSDia_04-07-22.csv'), sep=';')['Codigo']) # IAGRO
ativos_codes_dfs.append(pd.read_csv(base_path.joinpath('IFILDia_04-07-22.csv'), sep=';')['Codigo']) # IFIX L

todos_cod_dos_ativos = {}

for indice in ativos_codes_dfs:
    for symbol in indice:
        symbol = str.strip(symbol)
        if symbol == 'Quantidade Teórica Total  Redutor':
            continue
        try:
            todos_cod_dos_ativos[symbol] += 1
        except KeyError:
            todos_cod_dos_ativos[symbol] = 1
total = 0

todayB = dt.date.today()
yesterdayB = todayB - dt.timedelta(days=11*365)
print(todayB,yesterdayB)

ativos_historical_data_dfs = []

outOpen, outHigh, outLow, outClose, outVolume = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
cols=[]

for cod in tqdm(todos_cod_dos_ativos):
    if todos_cod_dos_ativos[cod] >= 5:
        try:
            tmp_df = historicalDay(f'{cod}.SA', yesterdayB, todayB)

            dfOutOpen    = tmp_df['Open']
            dfOutClose   = tmp_df['Close']
            dfOutHigh    = tmp_df['High']
            dfOutLow     = tmp_df['Low']
            dfOutVolume  = tmp_df['Volume']

            outOpen   = pd.concat([outOpen, dfOutOpen], axis=1)
            outClose  = pd.concat([outClose, dfOutClose], axis=1)
            outHigh   = pd.concat([outHigh, dfOutHigh], axis=1)
            outLow    = pd.concat([outLow, dfOutLow], axis=1)
            outVolume = pd.concat([outVolume, dfOutVolume], axis=1)

            cols.append(cod)
        except:
            print(f'Error: {cod}')

outOpen.columns=cols
outClose.columns=cols
outHigh.columns=cols
outLow.columns=cols
outVolume.columns=cols


output=outVolume.copy()

print(output.shape)
import plotly.express as px

fig = px.imshow(output.isnull(), color_continuous_scale='aggrnyl')
fig.update_layout(coloraxis_showscale=False)
fig.show()
# plt.figure(figsize=(40,10))
# sns.heatmap(output.isnull(),  cbar=False, cmap = 'summer')


len(output.columns)


medias_dos_volumes_de_cada_ativo = {}

for cod, ativo_df in zip(todos_cod_dos_ativos, ativos_historical_data_dfs):
    medias_dos_volumes_de_cada_ativo[cod] = ativo_df['Volume'].mean(axis=0)
    
print(sorted(medias_dos_volumes_de_cada_ativo.items(), key= lambda x:x[1], reverse=True))

