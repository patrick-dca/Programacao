# Importando as bibliotecas que serão utilizadas #
import pandas as pd
import matplotlib.pyplot as plt
import yahoofinancials as yf
import pandas_ta as ta
import numpy as np

# Escolher a ação e datas que serão utilizadas #
print('////////////////////////////////////////////////////////////////////////////')
x = print('Qual ação quer utilizar para testar no programa?')
y = print('OBS: para ações brasileiras - "ticker.SA" e para americanas apenas seu ticker. ')
t = input('ação escolhida --> ')
print('////////////////////////////////////////////////////////////////////////////')
w = print('Qual perí­odo quer analisar?')
z = print('OBS: colocar as datas no seguinte formato: aaaa-mm-dd')
inicio = input('data de iní­cio --> ')
fim = input('data final --> ')
print('////////////////////////////////////////////////////////////////////////////')

# Transformando os dados requeridos em um data Frame contendo as datas e os preços de fechamento ajustado #
ticker = yf.YahooFinancials(t) 

dados_originais = ticker.get_historical_price_data(inicio, fim, 'daily')
dados_originais = pd.DataFrame(dados_originais[t]['prices'])
dados_originais = dados_originais.drop(['close','date'],axis=1)
dados = dados_originais[['formatted_date','adjclose']]
dados.rename(columns={'formatted_date' : 'data', 'adjclose' : 'fechamento'}, inplace=True)
dados_originais.rename(columns={'high' : 'High', 'low' : 'Low', 'open' : 'Open', 'volume' : 'Volume', 'formatted_date' : 'Date', 'adjclose' : 'Close'}, inplace=True)

# CÃ¡lculo da média móvel exponencial p/ curto e longo prazo #
Periodo_curto = 50
Periodo_Longo = 200

print('////////////////////////////////////////////////////////////////////////////')
e = print('Qual estratégia quer usar? Média Móvel Simples (SMA) ou Média Móvel Exponencial (EMA) ? ')
f = input('Estratégia escolhida --> ')
print('////////////////////////////////////////////////////////////////////////////')


if f == 'SMA':
    dados['MMECP'] = round(pd.Series(dados.iloc[:, 1]).rolling(Periodo_curto).mean(), 4) # Média móvel simples de curto
    dados['MMELP'] = round(pd.Series(dados.iloc[:, 1]).rolling(Periodo_Longo).mean(), 4) # Média móvel simples de longo   
elif f == 'EMA':
    dados['MMECP'] = round(ta.ema(dados.iloc[:, 1], Periodo_curto), 4) # Média móvel exponencial de curto
    dados['MMELP'] = round(ta.ema(dados.iloc[:, 1], Periodo_Longo), 4) # Média móvel exponencial de longo

# Gráfico do fechamento ajustado no perí­odo #
figura1=plt.plot(dados['data'], dados['fechamento'], dados['data'], dados['MMECP'], dados['data'], dados['MMELP'])
plt.title('Gráfico do fechamento,da média móvel exponencial de curto e longo prazo de 2015 a 2022')
plt.xlabel('Data')
plt.ylabel('Preço em R$')
plt.legend(['Fechamento','MMECP','MMELP'])

# Cálculo para entender se a curva de curto prazo estão acima, abaixo ou cruzando a de longo prazo #
cross = pd.DataFrame()
cross['cross'] = dados['MMECP'] - dados['MMELP']
cross['data']=dados['data']
cross = cross[['data', 'cross']]
cross.dropna(axis=0,inplace=True)
cross.reset_index(inplace=True)
print('////////////////////////////////////////////////////////////////////////////')
print('Tabela de diferença entre MMECP e MMELP:')
print(cross)
print('////////////////////////////////////////////////////////////////////////////')

# Gráfico para enxergar os momentos que a curva de curto prazo estão acima, abaixo ou cruzando a de longo prazo #
zero = np.zeros(len(cross))

fig2, ax = plt.subplots(figsize=(8,8))

ax.plot(cross['data'],cross['cross'],color='black')
ax.plot(cross['data'],zero,color='black')

    # preencher area quando MMECP > MMELP com verde
ax.fill_between(
    cross['data'], cross['cross'], zero, where=(cross['cross'] > zero), 
    interpolate=True, color="green", alpha=0.25, 
    label="Golden Cross"
)

    # preencher area quando MMECP <= MMELP com vermelho
ax.fill_between(
    cross['data'], cross['cross'], zero, where=(cross['cross'] <= zero), 
    interpolate=True, color="red", alpha=0.25,
    label="Death Cross"
)

plt.title('Representação das áreas onde MMECP estãp acima da MMELP')
plt.ylabel('Diferença entre MMECP e MMELP')
plt.legend()

# Regra de decisão #
d = dados.set_index('data', inplace = False)
preco = []
compra_ou_venda = []
data = []
for i in range(len(cross)-1):
        if cross['cross'][i]<0 and cross['cross'][i+1]>0:
            compra_ou_venda.append('comprar')
            data.append(cross['data'][i])
            preco.append(d.loc[dados['data'][i],'fechamento'])
        elif cross['cross'][i]>0 and cross['cross'][i+1]<0:
            compra_ou_venda.append('vender')
            data.append(cross['data'][i])
            preco.append(d.loc[dados['data'][i],'fechamento'])
decisao=pd.DataFrame(compra_ou_venda, columns=['decisão '])
decisao['data'] = data
decisao['valor de compra/venda'] = preco
print('////////////////////////////////////////////////////////////////////////////')
print('Tabela com as regras de decisão com base na estratégia escolhida:')
print(decisao)
print('////////////////////////////////////////////////////////////////////////////')

#BACKTEST
d = dados.set_index('data', inplace = False)
preco = []
compra_ou_venda = []
data = []
rentabilidade = []

position = 0

a = print('Quanto deseja que seja o Stop Loss do robô ?')
stop = float(input('Stop Loss --> '))


for i in range(1,len(cross)):
        
        if cross['cross'][i-1]<0 and cross['cross'][i]>0:
            compra_ou_venda.append('comprar')
            data.append(cross['data'][i])
            if position !=0:
                rentabilidade.append((preco[-1]/d.loc[dados['data'][i],'fechamento'])-1)
            preco.append(d.loc[dados['data'][i],'fechamento'])
            position = 1    
            
        elif cross['cross'][i-1]>0 and cross['cross'][i]<0:
            compra_ou_venda.append('vender')
            data.append(cross['data'][i])
            if position !=0:
                rentabilidade.append((d.loc[dados['data'][i],'fechamento']/preco[-1])-1)
            preco.append(d.loc[dados['data'][i],'fechamento'])
            position = -1
            
        elif position == 1 and d.loc[dados['data'][i],'fechamento'] < d.loc[dados['data'][i-1],'fechamento']*(1-stop):
            compra_ou_venda.append('STOP')
            data.append(cross['data'][i]) 
            rentabilidade.append((d.loc[dados['data'][i],'fechamento']/preco[-1])-1)
            if position !=0:
                rentabilidade.append((d.loc[dados['data'][i],'fechamento']/preco[-1])-1)         
            preco.append(d.loc[dados['data'][i],'fechamento'])
            position = 0

        elif position == -1 and d.loc[dados['data'][i],'fechamento'] > d.loc[dados['data'][i-1],'fechamento'] *(1+stop):
            compra_ou_venda.append('STOP')
            data.append(cross['data'][i])
            rentabilidade.append((d.loc[dados['data'][i],'fechamento']/preco[-1])-1)
            if position !=0:
                rentabilidade.append((preco[-1]/d.loc[dados['data'][i],'fechamento'])-1) 
            preco.append(d.loc[dados['data'][i],'fechamento'])
            position = 0
            
decisao=pd.DataFrame(compra_ou_venda, columns=['decisão'])
decisao['data'] = data
decisao['valor de compra/venda'] = preco

print('////////////////////////////////////////////////////////////////////////////')
print('Tabela de decisão porém com stop-loss:')
print(decisao)
print('////////////////////////////////////////////////////////////////////////////')

rentabilidade=pd.DataFrame(rentabilidade, columns=['rentabilidade'])
print('Rentabilidade dos trades:')
print(rentabilidade)
print('////////////////////////////////////////////////////////////////////////////')


# Cálculo do retorno para o robô e para uma estratégia puramente de buy and hold
retorno_buy_and_hold = pd.DataFrame()
retorno_buy_and_hold['data'] = dados['data']

retorno_robo = pd.DataFrame()

def retornos(fechamento):
    retornos=[0]
    for i in range(1,len(fechamento)):
        retornos.append(fechamento[i]/fechamento[i-1] -1)
    return np.array(retornos)

retorno_buy_and_hold['retornos diários'] = retornos(dados['fechamento'])
retorno_robo['retornos por operação'] = rentabilidade['rentabilidade']

def retornos_acumulados(retornos_por_periodo):
    capital = 1
    retornos = []
    for r in retornos_por_periodo:
        capital += capital*r
        retornos.append(capital-1)
    return retornos

retorno_buy_and_hold['retornos acumulados'] = retornos_acumulados(retorno_buy_and_hold['retornos diários'])
tam_buy_and_hold=len(retorno_buy_and_hold)

retorno_robo['retornos acumulados'] = retornos_acumulados(retorno_robo['retornos por operação'])
tam_robo=len(retorno_robo)

print('////////////////////////////////////////////////////////////////////////////')
print('Retornos diários e acumulados da estratégia BUY AND HOLD:')
print(retorno_buy_and_hold)
print('////////////////////////////////////////////////////////////////////////////')
print('Retornos diários e acumulados da estratégia do ROBÔ:')
print(retorno_robo)
print('////////////////////////////////////////////////////////////////////////////')
print('O retorno acumulado da estratégia BUY AND HOLD foi de: ', round(retorno_buy_and_hold['retornos acumulados'][tam_buy_and_hold-1]*100,2),'%')
print('Já o retorno acumulado da estratégia do robô de: ', round(retorno_robo['retornos acumulados'][tam_robo-1]*100,2),'%')
print('////////////////////////////////////////////////////////////////////////////')

# Gráfico dos retornos das duas estratégias
fig3_4, (ax3, ax4) = plt.subplots(2)
fig3_4.suptitle('Retornos acumulados do BUY AND HOLD e do ROBÔ ao longo do perí­odo analisado')
ax3.plot(retorno_buy_and_hold['retornos acumulados'])
ax3.legend(['BUY AND HOLD'],loc="upper left")
ax4.plot(retorno_robo['retornos acumulados'], color='red')
ax4.legend(['ROBÔ'],loc="upper left")

# Backtest
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

dados_backtest = pd.DataFrame()

Open = dados_originais.iloc[:, 2]
High = dados_originais.iloc[:, 0]
Low = dados_originais.iloc[:, 1]
Close = dados_originais.iloc[:, 4]
Volume = dados_originais.iloc[:, 3]

dados_backtest['Open'] = Open
dados_backtest['High'] = High
dados_backtest['Low'] = Low
dados_backtest['Close'] = Close
dados_backtest['Volume'] = Volume

def SMA(valores, n):
    """
    Retorna a média móvel simples dos 'valores'
    com cada passo levando em conta os n valores anteriores.
    """
    #
    return pd.Series(valores).rolling(n).mean()

def EMA(valores, n):
    """
    Retorna a média móvel exponencial dos 'valores'
    com cada passo levando em conta os n valores anteriores.
    """
    EMA = ta.ema(dados_backtest["Close"], n)
    return EMA


class SMACross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = Periodo_curto
    n2 = Periodo_Longo
    
    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

class EMACross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = Periodo_curto
    n2 = Periodo_Longo
    
    def init(self):
        # Precompute the two moving averages
        self.ema1 = self.I(EMA, self.data.Close, self.n1)
        self.ema2 = self.I(EMA, self.data.Close, self.n2)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.ema1, self.ema2):
            self.position.close()
            self.buy()

        # Else, if ema1 crosses below ema2, close any existing
        # long trades, and sell the asset
        elif crossover(self.ema2, self.ema1):
            self.position.close()
            self.sell()

if f == 'SMA':
    bt = Backtest(dados_backtest, SMACross, cash=100, commission=.002)
    estatisticas = bt.run()
    print('////////////////////////////////////////////////////////////////////////////')
    print('Backtesting da estratégia escolhida:')
    print(estatisticas)
    print('////////////////////////////////////////////////////////////////////////////')
    bt.plot(filename = r'C:\Users\patri\OneDrive - Insper - Institudo de Ensino e Pesquisa\INSPER\ENTIDADES' ,plot_equity=True, plot_return=False, plot_pl=True, plot_volume=True, plot_drawdown=True,show_legend=True,open_browser=True)
elif f == 'EMA':
    bt = Backtest(dados_backtest, EMACross, cash=100, commission=.002)
    estatisticas = bt.run()
    print('////////////////////////////////////////////////////////////////////////////')
    print('Backtesting da estratégia escolhida:')
    print(estatisticas)
    print('////////////////////////////////////////////////////////////////////////////')
    bt.plot(filename = r'C:\Users\patri\OneDrive - Insper - Institudo de Ensino e Pesquisa\INSPER\ENTIDADES' ,plot_equity=True, plot_return=False, plot_pl=True, plot_volume=True, plot_drawdown=True,show_legend=True,open_browser=True)    

otimizar = bt.optimize(n1=range(5, 70, 5),
                    n2=range(100, 300, 5),
                    maximize='Equity Final [$]',
                    constraint=lambda param: param.n1 < param.n2)

otimo = otimizar._strategy
print('////////////////////////////////////////////////////////////////////////////')
print('Valores para os parâmetros de dias para as médias móveis de curto e longo prazo que maximizam os lucros:')
print(otimo)
print('////////////////////////////////////////////////////////////////////////////')
print('Backtesting da estratégia escolhida para os parâmetros otimizados:')
print(otimizar)
print('////////////////////////////////////////////////////////////////////////////')



# Curva de patrimônio
patrimonio = estatisticas['_equity_curve']
plt.plot(patrimonio['Equity'])

# Tabela de trades
trades = estatisticas['_trades'] 
print('////////////////////////////////////////////////////////////////////////////')
print('Tabela de trades:')
print(trades)
print('////////////////////////////////////////////////////////////////////////////')
