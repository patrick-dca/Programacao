# -*- coding: utf-8 -*-
"""
Aula: Finanças Corporativas III
Autora: Mariana Orsini Machado de Sousa
Data: Out/Nov de 2021

pacotes:
# C:/Users/maria/AppData/Local/Programs/Python/Python39/python.exe -m pip install <...>
!pip install investpy - acessa os dados da investing.com
!pip install pandas
!pip install matplotlib
!pip install seaborn
!pip install -U pybovespa

"""

#pacotes 

import matplotlib.pyplot as plt
import investpy as inv #acessa dados do investing.com
#import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib
#import plotly.graph_objects as go
matplotlib.rcParams['figure.figsize'] = (16,8)
#import pandas_datareader.data as web
#import yfinance as yf


#### Exercício Python com dados do Investing.com
#lista as variáveis
bondsBR = inv.get_bonds_list('brazil')
print(bondsBR)

bonds_overview = inv.get_bonds_overview('brazil')
print(bonds_overview)

plt.plot(bondsBR, bonds_overview['last_close'])
plt.show()

#bondsMX = inv.get_bonds_list('mexico')
#print(bondsMX)


##Plotando o Yield de fechamento histórico para o vencimento de 1 ano:
    
data_inicio = '01/01/2015'
data_fim = '24/05/2022'

um_ano = inv.get_bond_historical_data('Brazil 1Y', from_date= data_inicio, to_date = data_fim)
print(um_ano)

um_ano['Close'].plot()
plt.show()

#Construindo uma curva de juros para varios vencimentos

data_inicio = '01/01/2010'
data_fim = '24/05/2022'
bonds = pd.DataFrame()

for prazo in bondsBR:
  bonds[prazo] =  inv.get_bond_historical_data(prazo, from_date= data_inicio, to_date = data_fim)['Close']

print(bonds)

bonds.index = pd.to_datetime(bonds.index) #transforma o índice do dataframe em date-time p facilitar a busca

## Curva de Hoje
plt.figure(figsize=(12,5))
plt.xlabel('Interest Rate')
ax1 = plt.plot(bondsBR, bonds.loc['2021-11-22'].values, label='2021-11-22')
plt.legend(loc='upper left', frameon=False)
plt.title("Taxa de Juros por Vencimento")

plt.show()

# Curvas com diversos vencimentos para avaliar a evolução ao longo do tempo (tanto inclinação como deslocamento)
plt.figure(figsize=(12,5))
plt.xlabel('Interest Rate')
ax1 = plt.plot(bondsBR, bonds.loc['2022-05-23'].values, label='2022-05-23')
ax2 = plt.plot(bondsBR, bonds.loc['2021-05-22'].values, label='2021-05-22')
ax3 = plt.plot(bondsBR, bonds.loc['2020-05-22'].values, label='2020-05-22')
ax3 = plt.plot(bondsBR, bonds.loc['2019-05-22'].values, label='2019-05-22')
plt.legend(loc='upper left', frameon=False)
plt.title("Taxa de Juros por Vencimento")

plt.show()

### shift na taxa para o cálculo da taxa à termo

bonds_today = bonds.loc['2022-05-23']
bonds_today = pd.DataFrame(bonds_today)
#adding maturity days to dataFrame
bonds_today["days"] = [90,180,270,360,720,980,1800,2880,3600]
bonds_today.head() 
bonds_today = bonds_today.rename(columns={bonds_today.columns[0]: "rates" })

bonds_today["Rate_Shift"] = bonds_today["rates"].shift(1, fill_value=0)
bonds_today["Day_Shift"] = bonds_today["days"].shift(1, fill_value=0)
bonds_today["delta_days"] = bonds_today["days"] - bonds_today["Day_Shift"] 

## Calculando a taxa à termo

bonds_today["part1"] =(1+bonds_today["rates"])**(bonds_today["days"]/bonds_today["delta_days"])
bonds_today["part2"] =(1+bonds_today["Rate_Shift"])**(bonds_today["Day_Shift"]/bonds_today["delta_days"])

bonds_today["Forward_Rate"] = (bonds_today["part1"]/bonds_today["part2"]) - 1

## Gráfico taxa à termo
plt.figure(figsize=(12,5))
plt.xlabel('%')
ax3 = plt.plot(bondsBR, bonds_today["Forward_Rate"], label='Forward Rate')
ax4 = plt.plot(bondsBR, bonds_today["rates"], label='Spot Rate')
plt.legend(loc='upper left', frameon=False)
plt.title("Spot vs Forward Rate")

plt.show()

