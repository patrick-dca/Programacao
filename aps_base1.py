import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yfin
yfin.pdr_override()
from scipy import optimize as op


'''------------------------------------------ PRIMEIRA BASE DE DADOS -----------------------------------'''
#PASSOS INICIAIS ------------------------------------------------------------------------
#DADOS IMPORTANTES
rf = 0.0075
simulacoes = 100000

#BASE DE DADOS QUE SERÁ UTILIZADA
carteira = pd.read_excel("C:\\Users\\luuqu\\OneDrive\\Documentos\\FACULDADE\\4SEMESTRE\\Fin2\\BASE1.xlsx", 
                         sheet_name= "Retornos")

#MANIPULAÇÃO DA BASE DE DADOS
carteira.dropna()
carteira = carteira.drop('Attributes', axis = 1)
tickers = list(carteira.iloc[0,])
carteira.columns = [tickers]
carteira = carteira.drop(carteira.index[0:2], axis = 0)
carteira = carteira.reset_index()
num_acoes = len(tickers)
carteira = carteira.iloc[0:,1:]
carteira = carteira.replace("-",0)



#INICIANDO OS CÁLCULOS ------------------------------------------------------------------
med_df = carteira.mean()
cov_df = carteira.cov()

peso_acoes = []
retorno_simulacoes = []
desvio_simulacoes = []
sharpe_index = []

for carteiras in range(simulacoes):
    a = -1
    b = 1
    peso = (b-a)*np.random.random(num_acoes) + a
    retorno = np.dot(peso, med_df)
    desvio = np.sqrt(np.matmul(peso.T, np.matmul(peso, np.array(cov_df))))
    sharpe = (retorno-rf)/desvio
    
    peso_acoes.append(peso)
    retorno_simulacoes.append(retorno)
    desvio_simulacoes.append(desvio)
    sharpe_index.append(sharpe)

dic = {'Retorno' : retorno_simulacoes,
       'Desvio Padrão': desvio_simulacoes,
       'Sharpe': sharpe_index}
df_dic1 = pd.DataFrame(dic)

dic2 = {}
datafinal = pd.DataFrame()

for j in range(0, simulacoes):
    for i in range(0,len(tickers)-1):
        peso = peso_acoes[j][i]
        dic2["Peso " + tickers[i+1]] = [peso]
    df_dic2 = pd.DataFrame(dic2)
    
    datafinal = pd.concat([datafinal, df_dic2], axis = 0)
    
df_dic1.reset_index(drop = True, inplace=True)
datafinal.reset_index(drop = True, inplace=True)
carteiraf = pd.concat([df_dic1,datafinal], axis = 1)
#carteirf É O RESULTADO DE CADA SIMULAÇÃO DE CADA POSSÍVEL CARTEIRA QUE FOI CRIADA,
#COM OS DADOS DE PESO DE CADA ATIVO, BEM COMO RETORNO, DP E SHARPE DE CADA SIMULACAO

#PLOTANDO ESSE CONJUNTO DE SIMULACOES
carteiraf.plot.scatter(x ='Desvio Padrão', y ='Retorno', c ='Sharpe', figsize=(16,8), grid = True, cmap='RdYlGn', edgecolors= 'black',  xlim = (0, 0.45))

#INDICADORES E ANÁLISE DAS SIMULAÇÕES
maior_sharpe = carteiraf['Sharpe'].max()
carteira_maior_sharpe = carteiraf.loc[carteiraf['Sharpe'] == maior_sharpe]
print(f'O maior sharpe é {maior_sharpe}, da carteira {carteira_maior_sharpe.T}')


#CRIANDO FUNÇÃO PRA ACHAR A CARTEIRA OTIMA -------------------------------------------------
def otimizando(peso, med_df, cov_df, rf):
    retorno = np.dot(peso, med_df)
    desvio = np.sqrt(np.matmul(peso.T, np.matmul(peso,np.array(cov_df))))
    sharpe = -(retorno - rf)/desvio
    
    return sharpe

def soma_pesos(peso):
    soma = 1
    soma = soma - np.sum(peso)
    return soma

#ACHANDO A CARTEIRA ÓTIMA
restricao = {'type': 'eq', 'fun': soma_pesos}
start = np.random.random(num_acoes)
result = op.minimize(otimizando, start, args = (med_df, cov_df, rf), constraints = restricao)
pesos = result.x
carteiraOtima = pd.DataFrame({'Ativos': tickers, 'Pesos': pesos})
carteiraOtima.set_index(['Ativos'], inplace = True)

#DETALHES DA CARTEIRA OTIMA
retorno_otimo = np.dot(pesos, med_df)
desvio_otimo = np.sqrt(np.matmul(pesos.T, np.matmul(pesos, np.array(cov_df))))
sharpe_otimo = (retorno_otimo - rf) / desvio_otimo
cOtima_details = pd.DataFrame([retorno_otimo, desvio_otimo, sharpe_otimo],
                              ['E[r]', 'Risco','Sharpe'], ['Carteira de ativos de risco ótima'])


#CRIANDO A LAC
fim = max(carteiraf['Desvio Padrão'])
x = np.linspace(0, fim, simulacoes)
lac = sharpe_otimo*x + rf
plt.scatter(x = carteiraf['Desvio Padrão'], y = carteiraf['Retorno'], c = carteiraf['Sharpe'],
            s=20, cmap='RdYlGn', edgecolors='black' )
plt.scatter(x = desvio_otimo, y = retorno_otimo, s = 50, edgecolors = 'black',
            label='Carteira Ótima Otimização')
plt.plot(x, lac, label = 'LAC')
plt.ylim((-0.05,0.05))
plt.xlim((0,0.2))
plt.yticks(carteira_maior_sharpe['Retorno'])
plt.xticks(carteira_maior_sharpe['Desvio Padrão'])
plt.grid()
plt.legend()


#CRIANDO OS PERFIS DE CADA INVESTIDOR E SUAS CARTEIRAS -------------------------------------------------
#CRIANDO FUNÇÕES QUE SERÃO UTILIZADAS
def retU_investidor(A, U):
    sigma = np.linspace(0,max(carteiraf['Desvio Padrão']), simulacoes)
    retorno = 0.5*A*sigma**2 + U
    return retorno

def CPO(A):
    y = (retorno_otimo - rf) / (A*desvio_otimo**2)
    retorno_c = y*retorno_otimo + (1-y)*rf
    desvio_c = ((y**2)*desvio_otimo**2)**(1/2)
    return retorno_c, desvio_c

def Uinvestidor(A, retorno_c, desvio_c):
    utilidade_c = retorno_c - 0.5*A*desvio_c**2
    return utilidade_c

figure, axis = plt.subplots(2, 2) 
U = 0.05
axis[0,0].plot(x, retU_investidor(5,U), label = 'Utilidade Aversão ao Risco')
axis[0,0].plot(x, retU_investidor(1,U), label = 'Utilidade Amante ao Risco')
axis[0,0].plot(x, retU_investidor(2,U), label = 'Utilidade Neutro ao Risco')
axis[0,0].plot(x, lac, label='LAC')
axis[0,0].legend()

#CARTEIRAS ÓTIMAS --------------
#AVESSO AO RISCO
retorno_c, desvio_c = CPO(5)
utilidade_c = Uinvestidor(5, retorno_c, desvio_c)
axis[0,1].plot(x, lac, label='LAC')
axis[0,1].scatter(x = desvio_c, y = retorno_c, s = 50, edgecolors = 'black',
                  label= 'Aversão ao Risco')
axis[0,1].grid()
axis[0,1].legend()

#AMANTE AO RISCO
retorno_c, desvio_c = CPO(1)
utilidade_c = Uinvestidor(1, retorno_c, desvio_c)
axis[1,0].plot(x,lac, label='LAC')
axis[1,0].scatter(x = desvio_c, y = retorno_c, s=50, edgecolors = 'black',
                  label= 'Amante ao Risco')
axis[1,0].grid()
axis[1,0].legend()

#NEUTRO AO RISCO
retorno_c, desvio_c = CPO(2)
utilidade_c = Uinvestidor(2, retorno_c, desvio_c)
axis[1,1].plot(x, lac, label = 'LAC')
axis[1,1].scatter(x = desvio_c, y = retorno_c, s = 50, edgecolors = 'black',
                  label = 'Neutro ao Risco')
axis[1,1].grid()
axis[1,1].legend()