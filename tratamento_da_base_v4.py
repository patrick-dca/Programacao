import pandas as pd
import numpy as np
import os
import datetime as dt
from datetime import datetime, date

# 0°: indicar qual o nome da carteira e o caminho para o arquivo

print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')
#   --> input do nome da carteira a ser analisada
print('Qual o nome da carteira analisada?')
print('Ex: Boletoflex2 --> escrever boletoflex_2')
nome_carteira = input('Nome da carteira: ')

#   --> input do caminho para a pasta onde está arquivo da base original, e também onde os arquivos serão criados
print('Qual o caminho para o arquivo da carteira analisada?')
print('OBS: colocar apenas o caminho por enquanto, não colocar o nome do arquivo')
caminho = input('Caminho para o arquivo: ')

#   --> input do nome do arquivo original da carteira analisada
print('Qual o nome do arquivo original da carteira analisada?')
nome_arquivo_original = input('Nome do arquivo original: ')

#   --> input do tipo de arquivo da carteira analisada
print('Qual o tipo do arquivo a ser lido')
print('Ex: se for Excel escrever excel, se for CSV, escrever csv e se for texto, escrever texto')
tipo_arquivo_original = input('Tipo do arquivo original: ')

print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')
# 1°: ler o arquivo em excel contendo os dados originais da base a ser analisada

#   --> condição para identificar qual método do pandas usar para ler o arquivo, de acordo com o valor na variável "tipo_arquivo_original"
if tipo_arquivo_original == 'csv':
    # se o arquivo for csv, juntar o nome do arquivo na variável "nome_arquivo_original" com '.csv'
    nome_arquivo_original = nome_arquivo_original + '.csv'    
    # caminho completo até a base original
    caminho_completo = os.path.join(caminho, nome_arquivo_original)
    # le o arquivo e cria um dataframe com o conteúdo do arquivo indicado
    arquivo = pd.read_csv(caminho_completo)
elif tipo_arquivo_original == 'texto':
    nome_arquivo_original = nome_arquivo_original + '.txt'    
    caminho_completo = os.path.join(caminho, nome_arquivo_original)
    arquivo = pd.read_csv(caminho_completo)
elif tipo_arquivo_original == 'excel':
    nome_arquivo_original = nome_arquivo_original + '.xlsx'    
    caminho_completo = os.path.join(caminho, nome_arquivo_original)
    arquivo = pd.read_excel(caminho_completo)

#   --> dataframe como forma de tabela para mostrar as colunas existentes no dataframe "arquivo"
colunas = pd.DataFrame(arquivo.columns).reset_index()
colunas.rename(columns={ 0 :'Colunas', 'index': 'Localização'},inplace=True)
#   --> printa os valores e o nome das colunas para auxiliar no processo de escolha das colunas necessárias
print(arquivo,colunas)
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')

# 2°: criação de um dataframe contendo apenas as colunas selecionadas necessárias para a análise da carteira

# 2.1°: processo de escolha das colunas que irão compor o dataframe reduzido

print('Quantas colunas quer selecionar para a criação de um novo dataframe?')
#   --> input do  número de colunas que irão para o novo dataframe
input_num_colunas = int(input('Número de colunas: '))
print('Agora, quais colunas quer selecionar para a criação de um novo dataframe?')
print('A seleção será por meio da localização na lista. A localização é o número a esquerda do nome da coluna')
#   --> lista vazia para armazenar a localização das colunas escolhidas
localizacoes = []
#   --> iteração pelo número de colunas escohidas para armazenar em uma lista as localizações das colunas
for i in range(input_num_colunas):
    # input da localização da coluna de acordo com a tabela de colunas
    input_localizacao_coluna = int(input('Localização da coluna na lista "colunas": '))
    # adiciona na lista "localizacoes" a localização de cada nome da coluna
    localizacoes.append(input_localizacao_coluna)
#   --> lista vazia para armazenar o nome das colunas escolhidas de acordo com as localizações indicadas
lista_colunas = []
#   --> iteração pelo número de colunas escohidas para armazenar em uma lista os nomes das colunas de acordo com suas localizações
for j in range(input_num_colunas):
    # adiciona na lista "lista_colunas" o nome das colunas, contidas no dataframe "colunas" de acordo com as localizações escolhidas
    lista_colunas.append(colunas['Colunas'][localizacoes[j]])
print(lista_colunas)
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')

#   --> função que cria um dicionário para nomes fixos de colunas que são preenchidas de acordo com colunas do arquivo. É preenchido por nomes de colunas que possuam certas letras.
def criar_dic(lista_palavras, letras1,letras1_1,letras2,letras2_1,letras2_2,letras2_3,letras3,letras3_1,letras3_2,letras3_3,letras3_4,letras4,letras4_1,letras4_2,letras4_3,letras5,letras5_1,letras5_2,letras5_3,letras5_4,letras5_5,letras5_6,letras5_7,letras5_8,letras5_9,letras6,letras6_1,letras7,letras7_1,letras7_2,letras7_3,letras8,letras8_1,letras9,letras9_1,letras9_2,letras9_3):
    # dicionário vazio para o preenchimento
    dic = {"CPF": '', "data_atraso": '', "dias_atraso": '', "data_referencia":'', "valor_divida": '', "produto":'', "FPD":'', "data_nascimento":'', "tipo_pessoa":'',}
    # iteração pelo número de palavras na lista
    for palavra in lista_palavras:
        # se tiver as letras indicadas na variável "letras1" na palavra da lista de palavras é adicionada ao dicionário 
        if letras1 in palavra:
            dic["CPF"]=dic["CPF"]+palavra
        elif letras1_1 in palavra:
            dic["CPF"]=dic["CPF"]+palavra
        elif letras2 in palavra:
            dic["data_atraso"]=dic["data_atraso"] + palavra
        elif letras2_1 in palavra:
            dic["data_atraso"]=dic["data_atraso"] + palavra
        elif letras2_2 in palavra:
            dic["data_atraso"]=dic["data_atraso"] + palavra
        elif letras2_3 in palavra:
            dic["data_atraso"]=dic["data_atraso"] + palavra
        elif letras3 in palavra:
            dic["dias_atraso"]=dic["dias_atraso"] + palavra
        elif letras3_1 in palavra:
            dic["dias_atraso"]=dic["dias_atraso"] + palavra
        elif letras3_2 in palavra:
            dic["dias_atraso"]=dic["dias_atraso"] + palavra
        elif letras3_3 in palavra:
            dic["dias_atraso"]=dic["dias_atraso"] + palavra
        elif letras3_4 in palavra:
            dic["dias_atraso"]=dic["dias_atraso"] + palavra
        elif letras4 in palavra:
            dic["data_referencia"]=dic["data_referencia"]+ palavra
        elif letras4_1 in palavra:
            dic["data_referencia"]=dic["data_referencia"]+ palavra
        elif letras4_2 in palavra:
            dic["data_referencia"]=dic["data_referencia"]+ palavra
        elif letras4_3 in palavra:
            dic["data_referencia"]=dic["data_referencia"]+ palavra
        elif letras5 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_1 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_2 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_3 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_4 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_5 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_6 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_7 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_8 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras5_9 in palavra:
            dic["valor_divida"]=dic["valor_divida"] + palavra
        elif letras6 in palavra:
            dic["produto"]=dic["produto"] + palavra
        elif letras6_1 in palavra:
            dic["produto"]=dic["produto"] + palavra
        elif letras7 in palavra:
            dic["FPD"]=dic["FPD"] + palavra
        elif letras7_1 in palavra:
            dic["FPD"]=dic["FPD"] + palavra
        elif letras7_2 in palavra:
            dic["FPD"]=dic["FPD"] + palavra
        elif letras7_3 in palavra:
            dic["FPD"]=dic["FPD"] + palavra
        elif letras8 in palavra:
            dic["data_nascimento"]=dic["data_nascimento"] + palavra
        elif letras8_1 in palavra:
            dic["data_nascimento"]=dic["data_nascimento"] + palavra
        elif letras9 in palavra:
            dic["tipo_pessoa"]=dic["tipo_pessoa"] + palavra
        elif letras9_1 in palavra:
            dic["tipo_pessoa"]=dic["tipo_pessoa"] + palavra
        elif letras9_2 in palavra:
            dic["tipo_pessoa"]=dic["tipo_pessoa"] + palavra
        elif letras9_3 in palavra:
            dic["tipo_pessoa"]=dic["tipo_pessoa"] + palavra
        else:
            continue
    return dic

#   --> variáveis contendo um conjunto de letras para procurar os nomes correspondentes nas palavras da lista
letras1 = "cpf"
letras1_1 = "CPF"
letras2 = "ven"
letras2_1 = "vct"
letras2_2 = "VEN"
letras2_3 = "VCT"
letras3 = "dia"
letras3_1 = "DIA"
letras3_2 = "DATRA"
letras3_3 = "ATRA"
letras3_4 = "atra"
letras4 = "ref"
letras4_1 = "REF"
letras4_2 = "base"
letras4_3 = "BASE"
letras5 = "tot"
letras5_1 = "val"
letras5_2 = "vl"
letras5_3 = "sal"
letras5_4 = "sl"
letras5_5 = "TOT"
letras5_6 = "VAL"
letras5_7 = "VL"
letras5_8 = "SAL"
letras5_9 = "SL"
letras6 = "prod"
letras6_1 = "PROD"
letras7 = "fp"
letras7_1 = "FP"
letras7_2 = "pag"
letras7_3 = "PAG"
letras8 = "nasc"
letras8_1 = "NASC"
letras9 = "tipo"
letras9_1 = "tp"
letras9_2 = "TIPO"
letras9_3 = "TP"

#   --> uso da função criar_dic
dicionario = criar_dic(lista_colunas, letras1,letras1_1,letras2,letras2_1,letras2_2,letras2_3,letras3,letras3_1,letras3_2,letras3_3,letras3_4,letras4,letras4_1,letras4_2,letras4_3,letras5,letras5_1,letras5_2,letras5_3,letras5_4,letras5_5,letras5_6,letras5_7,letras5_8,letras5_9,letras6,letras6_1,letras7,letras7_1,letras7_2,letras7_3,letras8,letras8_1,letras9,letras9_1,letras9_2,letras9_3)
#print(dicionario)

# 2.2°: processo de preenchimento do dataframe
#   --> dataframe vazio para armazenar o conteúdo das colunas escolhidas
dataframe = pd.DataFrame()

#   --> se dicionario estiver vazio, pular, se cheio, preencher a coluna no dataframe criado
if dicionario.get("CPF"):
    dataframe['CPF'] = arquivo[dicionario['CPF']]

# função que formata a data, evitando confusões quanto a qual parte seria o mês e qual seria o dia
#   --> função que tem como input um dataframe e a coluna de data, e devolve a coluna formatada como: 'aaaa-mm-dd'
def formatar_data(df, coluna_data):
    # se a data estiver sendo separada por "/" ou por "-", separa cada parte e armazena em três colunas diferentes
    formatar = df[coluna_data].str.contains("/").any() and "/" or "-"
    df[['coluna1','coluna2','coluna3']] = df[coluna_data].str.split(formatar, expand=True)
    df[['coluna1','coluna2','coluna3']] = df[['coluna1','coluna2','coluna3']].astype(int)

    colunas = df.columns
    
    for col in range(1,len(colunas)):
        if (df[colunas[col]] >= 1).all() and (df[colunas[col]] <= 12).all():
            df.rename(columns={colunas[col]: 'mês'}, inplace=True)
        elif (df[colunas[col]] >= 1).all() and (df[colunas[col]] <= 31).all():
            df.rename(columns={colunas[col]: 'dia'}, inplace=True)
        elif (df[colunas[col]] >= 1990).all() and (df[colunas[col]] <= 2023).all():
            df.rename(columns={colunas[col]: 'ano'}, inplace=True) 

    df['data_completa'] = df.apply(lambda x: datetime(int(x['ano']), int(x['mês']), int(x['dia'])), axis=1) 
    
    df.drop([coluna_data,'mês','ano','dia'],axis = 1)
    
    df_data = pd.DataFrame()
    df_data[coluna_data] = df['data_completa']
    
    return df_data

if dicionario.get("data_atraso"):
    dataframe['data_atraso'] = arquivo[dicionario['data_atraso']]
#else:
 #       data_vencimento = pd.DataFrame()
  #      data_vencimento['data_atraso'] = formatar_data(arquivo,dicionario['data_atraso'])
   #     dataframe['data_atraso'] = data_vencimento['data_atraso']
if dicionario.get("data_referencia"):
    dataframe['data_referencia'] = arquivo[dicionario['data_referencia']]
    #try:
     #   data_referencia = pd.DataFrame()
     #  data_referencia['data_referencia'] = formatar_data(arquivo,dicionario['data_referencia'])    
    #except:
     #   dataframe['data_referencia'] = arquivo[dicionario['data_referencia']]
else:
    dataframe['data_referencia'] = date.today().strftime('%m-%d-%Y')
if dicionario.get("dias_atraso"):
    dataframe['dias_atraso'] = arquivo[dicionario['dias_atraso']]
else:
    # para o caso da base não conter os dias de atraso explicitado, terá que ser feito o cálculo por aqui, através das seguintes linhas:
    # calcula os dias de atraso e insere no dataframe em uma nova coluna chamada "dias_atraso"
    dataframe['dias_atraso'] = (pd.to_datetime(dataframe['data_referencia']) - pd.to_datetime(dataframe['data_atraso'])).dt.days
if dicionario.get("valor_divida"):
    dataframe['valor_divida'] = arquivo[dicionario['valor_divida']]
if dicionario.get("produto"):
    dataframe['produto'] = arquivo[dicionario['produto']]
if dicionario.get("data_nascimento"):
    dataframe['data_nascimento'] = arquivo[dicionario['data_nascimento']]
if dicionario.get("FPD"):
    dataframe['FPD'] = arquivo[dicionario['FPD']]
if dicionario.get("tipo_pessoa"):
    dataframe['tipo_pessoa'] = arquivo[dicionario['tipo_pessoa']]
print(dataframe)
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')

#   --> arruma todos os dados do dataframe criado de modo decrescente quanto aos dias de atraso
dataframe = dataframe.sort_values('dias_atraso', ascending = False)

# 3°: cria um segundo dataframe, para a realização dos cálculos com cpfs únicos

#   --> primeiro é feito a exclusão da coluna de valores dos títulos
dataframe_editado = dataframe.drop('valor_divida', axis = 1)
#   --> só então é feita a exclusão de cpfs duplicados, mantendo apenas os primeiros, ou seja, com maiores dias de atraso
dataframe_editado = dataframe_editado.drop_duplicates(subset ='CPF', keep ='first').reset_index(drop = True)

#   --> função que conta a quantidade contratos que são do tipo pessoa física ou pessoa jurídica
def contagem_tipo_pessoa(df):
    if 'tipo_pessoa' in df.columns:
        num_f = len(df[df['tipo_pessoa'] == 'F'])
        num_j = len(df[df['tipo_pessoa'] == 'J'])
        return num_f, num_j
    else:
        return len(df), 0  
#   --> uso da função contagem_tipo_pessoa
conta_tipo_pessoa = contagem_tipo_pessoa(dataframe)

#   --> função de filtro do dataframe por tipo de pessoa, pega apenas linhas no qual a pessoa seja física, não jurídica
def filtro_df(df):
    if 'tipo_pessoa' in df.columns:
        return df[df['tipo_pessoa'] == 'F']
    else:
        return df
#   --> uso da função filtro_df
dataframe_editado = filtro_df(dataframe_editado)

# 4°: é feito o cálculo do valor devido total por cpf, utilizando uma função que funciona como um "somases" do excel

#   --> função do somases, onde temos como input o dataframe original, o dataframe editado e as colunas em comum, e ele retorna um dataframe com a soma da dívida por cpf
def somases(df1, coluna1, df2, coluna2):
    # Agrupa df1 pela coluna1 and soma os valores
    df1_agrupado = df1.groupby(coluna1).sum()
    # Faz um left join do df1 agrupado com o df2 pela coluna2
    resultado = df1_agrupado.merge(df2, left_index=True, right_on=coluna2, how='left' )
    return resultado
#   --> uso da função somases
somase = somases(dataframe, 'CPF', dataframe_editado, 'CPF')
#   --> feito o cálculo, é obtida apenas a coluna referente ao valor devido total por cpf e insere em uma nova coluna no dataframe editado com nome de "valor devido total"
dataframe_editado['valor_divida_por_cpf'] = somase['valor_divida']
print(dataframe_editado)
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')

# 4.1°: é feito um check para saber quantos cpfs repetidos haviam na base original

n_cpfs_original = len(dataframe)
n_cpfs_unico = len(dataframe_editado)
diferenca = str(n_cpfs_original - n_cpfs_unico)
print('Existem ' + diferenca + ' cpfs repetidos')
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')

# 5°: começam os cálculos para uma tabela descritiva dos dados do dataframe editado

# 5.1°: função para o cálculo da FPD da base, caso hajam os dados
print('Existem dados acerca de FPD na base analisada? ')
print('Se sim, escrever "sim" e se não, escrever "não"')
existencia_fpd = input('Resposta: ')
if existencia_fpd == 'sim':
    print('Escolha a condição para o cálculo da FPD')
    print('Ex: se for fornecida uma coluna "FPD", escolher valor = 1, se for fornecida uma coluna "Quantidade de parcelas pagas", escolher valor=0')
    condicao = int(input('Condição da FPD: '))
else:
    condicao = []
    
#   --> função de fpd, onde temos como input a lista dos dados de fpd e a condição, e se der erro (caso de não existir coluna de FPD),o valor é colocado como 0
def fpd(lista, condicao):

    # admite valores que respeitem a condição como 1 e os soma, em seguida divide a soma pelo tamanho da lista
    resultado = (sum(1 for item in lista if condicao(item)))/len(lista)

    return resultado
#   --> uso da função fpd para a coluna de fpd da base editada e como condição os valores que sejam iguais a 1
#   --> OBS: as vezes acontece do FPD na base ser para valores iguais a 0, então deve-se trocar ali a condição
try:
    FPD = fpd(dataframe_editado['FPD'], lambda x: x == condicao)
except:
    FPD = 0.00
    
#   --> função de analise de idade para cpfs com idade acima de 60 anos, retona a média e a mediana das idades acima de 60 anos
def analise_acima_60_anos(df):
    
    data_nascimento = pd.DataFrame()
    data_nascimento['data_nascimento'] = pd.to_datetime(df['data_nascimento'])
    hoje = datetime.now().date()
    data_nascimento['idade'] = ((hoje - data_nascimento['data_nascimento'].dt.date).dt.days)/365
    media_acima_60 = round(data_nascimento[data_nascimento['idade'] >= 60]['idade'].mean(),0)
    mediana_acima_60 = round(data_nascimento[data_nascimento['idade'] >= 60]['idade'].median(),0)    
    
    return media_acima_60,mediana_acima_60
#   --> uso da função analise_acima_60_anos para o dataframe editado
try:
    analise_idosos = analise_acima_60_anos(dataframe_editado)
except:
    analise_idosos = [0,0]
    
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')

# 5.2°: função para o cálculo da tabela descritiva da base
#   --> função para a tabela, onde temos como input a lista dos dados de fpd e a condição conta_tipo_pessoa
def analise_descritiva(df):
    tabela = pd.DataFrame()
    resultado = pd.DataFrame({"Número de cpfs únicos": dataframe_editado.count(),
                           "Número de cpfs totais na base": dataframe.count(),
                           "Número total de contratos do tipo pessoa física na base": conta_tipo_pessoa[0],
                           "Número total de contratos do tipo pessoa jurídica na base": conta_tipo_pessoa[1],
                           "Valor de Face": "R${:,.2f}".format(dataframe_editado['valor_divida_por_cpf'].sum()),
                           "Valor de Face - 10 percentil": "R${:,.2f}".format(dataframe_editado['valor_divida_por_cpf'].quantile(0.10)),
                           "Valor de Face - 90 percentil": "R${:,.2f}".format(dataframe_editado['valor_divida_por_cpf'].quantile(0.90)),
                           "Ticket Médio": "R${:,.2f}".format(dataframe_editado['valor_divida_por_cpf'].mean()),
                           "Atraso Médio (dias)": "{:.2f}".format(dataframe_editado['dias_atraso'].mean()),
                           "Atraso Médio (meses)": "{:.2f}".format((dataframe_editado['dias_atraso'].mean())/30),
                           "Atraso Médio (meses) - 10 percentil": "{:.2f}".format((dataframe_editado['dias_atraso'].quantile(0.10))/30),
                           "Atraso Médio (meses) - 90 percentil": "{:.2f}".format((dataframe_editado['dias_atraso'].quantile(0.90))/30),
                           "Atraso Médio (anos)": "{:.2f}".format((dataframe_editado['dias_atraso'].mean())/365),
                           "FPD": "{:.2%}".format(FPD),
                           "Média de idade acima de 60 anos": analise_idosos[0],
                           "Mediana de idade acima de 60 anos": analise_idosos[1]})
    resultado = resultado.reset_index(drop = True).iloc[0]
    tabela['Valores'] = resultado    
    return tabela
#   --> uso da função analise_descritiva para o dataframe editado
tabela_descritiva = analise_descritiva(dataframe_editado)
print(tabela_descritiva)
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')

# 5.3°: função para o cálculo da tabela de produtos da base
#   --> função para a tabela, faz o input de um dataframe e retorna uma tabela com os produtos, a soma por produto e a porcentagem do total por produto
def tabela_produto(df):

    soma_por_produto = df.groupby(['produto'])['valor_divida_por_cpf'].sum()
    soma_total_por_produto = soma_por_produto.sum()
    prct_total_por_produto = soma_por_produto.apply(lambda x: (x / soma_total_por_produto) * 100)
    
    tabela = pd.DataFrame({'Produto': soma_por_produto.index,
                           'Soma por porduto': soma_por_produto.values,
                           'Porcentagem do total': prct_total_por_produto.values})
        
    return tabela
#   --> uso da função tabela_produto para o dataframe editado
try:
    produto = tabela_produto(dataframe_editado)
except:
    produto = pd.DataFrame()
    
# 6°: cria um dataframe com as três colunas necessárias para o upload na AWS

def trocar_ponto_decimal(input_lista):
    output_lista = []
    for valor in input_lista:
        output_lista.append(str(valor).replace(".", ","))
    return output_lista

input_lista = dataframe_editado['valor_divida_por_cpf'].to_list()
troca_ponto_decimal = trocar_ponto_decimal(input_lista)
dataframe_editado['valor_divida_por_cpf_formatado'] = troca_ponto_decimal

dataframe_csv = dataframe_editado[['CPF','valor_divida_por_cpf','dias_atraso']]

# 7°: seleção aleatória de cpfs para o Score do SPC

#   --> função de escolha aleatória de cpfs, onde emos como input o dataframe, o nome da coluna e o número de amostras requeridas 
def cpfs_aleatorios(df, coluna, n):
    # obtém os cpfs únicos
    cpfs_unicos = df[coluna].unique()
    # organiza tais cpfs de forma aleatória
    np.random.shuffle(cpfs_unicos)
    # e devolve um dataframe contendo os n cpfs
    return pd.DataFrame({coluna: cpfs_unicos[:n]})
#   --> uso da função cpfs_aleatorios para o dataframe editado
escolha_aleatoria = cpfs_aleatorios(dataframe_editado,'CPF', 100)

# 8°: criação de um arquivo de excel, no qual certas partes do processo são colocados em uma aba individual

#   --> designa um caminho no qual o arquivo deverá ser criado, e já escolhe o nome para o arquivo ( por exemplo: nome_arquivo.xlsx)
nome_arquivo_criado = nome_carteira + '.xlsx'
caminho_arquivo_criado_completo = os.path.join(caminho, nome_arquivo_criado)
#   --> Cria um objeto ExcelWriter no caminho designado
writer = pd.ExcelWriter(caminho_arquivo_criado_completo, engine='openpyxl')
#   --> Cria abas no arquivo criado para a base original, base editada, tabela descritiva, colunas para AWS e a escolha aleatória de cpfs
arquivo.to_excel(writer, sheet_name='base original', index=False)
dataframe_editado.to_excel(writer, sheet_name='base editada', index=False)
tabela_descritiva.to_excel(writer, sheet_name='tabela descritiva da base', index=True)
dataframe_csv.to_excel(writer, sheet_name= nome_carteira , index=False)
escolha_aleatoria.to_excel(writer, sheet_name='escolha aleatória de cpfs', index=False)
produto.to_excel(writer, sheet_name='produto', index=False)
#   --> salva o arquivo de excel
writer.save()
#   --> fecha o arquivo de excel, para que seja possível alterá-lo
writer.close()

# 9°: finalmente, são criados os arquivos em csv para o envio na AWS e no SPC

#   --> designa um caminho no qual o arquivo em csv para a AWS deverá ser criado, e já escolhe o nome para o arquivo ( por exemplo: nome_cartiera.csv)
nome_arquivo_AWS = nome_carteira + '.csv'
caminho_arquivo_AWS_completo = os.path.join(caminho, nome_arquivo_AWS)
dataframe_csv.to_csv(caminho_arquivo_AWS_completo, index = False)
#   --> designa um caminho no qual o arquivo em csv para o SPC deverá ser criado, e já escolhe o nome para o arquivo ( por exemplo: cpfs_aleatorios_nome_carteira.csv)
nome_arquivo_SPC = 'cpfs_aleatorios_' + nome_carteira + '.csv'
caminho_arquivo_SPC_completo = os.path.join(caminho, nome_arquivo_SPC)
escolha_aleatoria.to_csv(caminho_arquivo_SPC_completo, index = False)


print('Download do arquivo "' + nome_arquivo_criado + '" concluído.')
print('Download do arquivo "' + nome_arquivo_AWS + '" concluído.')
print('Download do arquivo "' + nome_arquivo_SPC + '" concluído.')
print('Tudo pronto!')
print('////////////////////////////////////////////////////////////////////////////////////////////////////////////')
