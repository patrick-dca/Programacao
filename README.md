# Pasta contendo arquivos próprios de programação:

Projetos de programação em Python e VBA Excel para a faculdade, trabalho, cursos extracurriculares ou apenas por passatempo.

# Descrição breve dos arquivos em Python:

1. Arquivos referentes a cálculo da Estrutura a Termo das Taxas de Juros (ETTJ), cálculo de taxas de juro (no caso spot e foward) e cálculo do preço de títulos de renda fixa:

   Programa em Python para um trabalho da faculdade no qual a partir de dados provenientes da B3, adquiridos através de webscreping, foi calculada as taxas de juros      descritas acima, e finalmente, foi calculado o valor de um título NTN-B trazendo os fluxos de caixa do mesmo a valor presente utilizando as taxas e os dias úteis      calculados. Valor esse que foi comparado ao seu preço de mercado, indicando se estava mais caro ou mais barato que deveria.
   
2. Arquivo de Markowitz:

   Programa em Python para um trabalho de faculdade no qual o usuário escolhe algumas ações para compor um portfolio e datas para o período de análise e com base          nessas informações calcula inicialmente: o retorno individual das ações e sua média, uma tabela de covariância entre as ações, e realiza n simulações para              identificar os pesos possíveis entre os ativos do portfólio. Assim, constrói uma tabela e um gráfico com os pesos simulados de cada ação e o retorno, desvio padrão    e sharpe ratio para cada distribuição de peso. A seguir é calculada e identificada a Carteira Ótima, ou seja, os pesos que resultam no maior retorno e sharpe com      menor desvio padrão. Então, é calculada a Carteira de Mínima Variância e a LAC. Tudo isso é plotado em um gráfico para melhor visualização.
   
3. Arquivo de Monte Carlo:

   Programa em Python feito nas férias no qual o usuário escolhe uma ação e um período para ser utilizado como histórico e com base nisso são calculadas as                estatísticas básicas da ação ao longo do período e são feitas n simulações de Monte Carlo para x dias na frente a fim de determinar o preço da ação escolhida no        futuro. Ainda, é plotado um gráfico com as n simulações mostrando as diferentes possibilidades para o preço daquela ação. Por fim, são calculados cenários otimistas    e pessimistas para o preço da ação.
   
4. Arquivo Tratamento da base V4:

   Consiste em um programa em Python feito durante meu estágio em uma fintech. Toda semana chegavam inúmeras bases de carteiras de dívidas de bancos e grandes            empresas, e essas bases possuiam dezenas de colunas de milhares de linhas, e eu era o responsável por fazer o tratamento dessa base (ordenar por dias de atraso,        retirar CPFs duplicados, somar as dívidas dos CPFs duplicados para não perder esses valores, calcular dias de atraso se precisasse, entre outros), calcular certas      métricas (valor de face da carteira, atraso médio, número de CPFs, percentis para valor de face e atraso, criar uma tabela com a composição de produtos da base,        calcular se o CPF deu inadimplência na primeira parcela, entre outros), separar apenas os dados de CPF, valor da dívida e dias de atraso em um CSV para enviar na      plataforma de análise, e por fim, separar outro CSV apenas com os CPFs escolhidos de forma aleatória para enviar a outra plataforma que checa o rating deles. E era    um trabalho que demandava muito do meu tempo, então, criei esse programa que faz tudo isso automaticamente.
   
5. Arquivo de Trend Following:

   Programa em Python feito para projeto de liga universitária no qual o usuário escolhe uma ação e um período para o backtest e utilizando esses dados um robô de        investimentos indica momentos de compra e de venda dessa ação seguindo a estratégia escolhida pelo usuário, Exponencial Moving Average (EMA) e Simple Moving Average    (SMA) e um Stop-Loss indicado. Assim, inúmeros calculos e tabelas são feitos a fim de facilitar a visualização do usuário bem como um backtesting extensivo da          performance do robô, mostrando melhores e piores trades, progressão de patrimônio, métricas de rentabilidade entre vários outros. Ainda, é feito uma otimização do      parâmetros das estratégias a fim de melhorar o modelo futuramente.
   

# Descrição breve dos arquivos em VBA Excel:

1. Arquivo referente a coleta de nomes de arquivos e atualização dos modelos financeiros:

   Programa em VBA Excel, criado durante estágio em fintech, que é utilizado em forma de botão. Primeiro, é fornecido o caminho da pasta no qual os arquivos desejados    estão e uma lista de arquivos que não devem ser coletados. Em seguida, no botão "Coleta do nome de arquivos", a pasta é percorrida e os nomes são coletados            (ignorandos os arquivos especificados), e então, um por um os nomes são colados na planilha em ordem alfabética. Assim, aciona-se o segundo botão "Atualizar Modelos    Financeiros". A partir dos nomes dos arquivos, o caminho da pasta dos mesmos e uma pasta de output, bem como valores a serem procurados e substituídos nos modelos,    o programa realiza uma série de tarefas. Primeiro copia todos os arquivos selecionados para a pasta de output, depois abre cada um e modifica os dados em algumas      coluna e atualiza alguns valores a partir do localizar e substituir, e finalmente, salva e fecha cada um.

2. Arquivo de Solver no VBA:

   Programa em VBA Excel, criado durante estágio em fintech, que gera tabelas contendo valores de precificações de carteiras de dívida e o percentual do valor original    que esse valor representa para valores diferentes de TIR. Portanto, o programa tem basicamente a função de um Solver que roda para inúmeras metas de uma vez só.


