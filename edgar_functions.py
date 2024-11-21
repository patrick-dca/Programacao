import os
import pandas as pd
import numpy as np  # make sure to add
import requests
from bs4 import BeautifulSoup
import logging  # make sure to add
import calendar  # make sure to add
import yfinance as yf
import matplotlib.pyplot as plt

headers = {"User-Agent": "patrickca@al.insper.edu.br"}    # change to your own headers file or add variable in code

pd.options.display.float_format = (
    lambda x: "{:,.0f}".format(x) if int(x) == x else "{:,.2f}".format(x)
)


pd.options.display.float_format = (
    lambda x: "{:,.0f}".format(x) if int(x) == x else "{:,.2f}".format(x)
)

statement_keys_map = {
    "balance_sheet": [
        "balance sheet",
        "balance sheets",
        "statement of financial position",
        "consolidated balance sheets",
        "consolidated balance sheet",
        "consolidated financial position",
        "consolidated balance sheets - southern",
        "consolidated statements of financial position",
        "consolidated statement of financial position",
        "consolidated statements of financial condition",
        "combined and consolidated balance sheet",
        "condensed consolidated balance sheets",
        "consolidated balance sheets, as of december 31",
        "dow consolidated balance sheets",
        "consolidated balance sheets (unaudited)",
    ],
    "income_statement": [
        "income statement",
        "income statements",
        "statement of earnings (loss)",
        "statements of consolidated income",
        "consolidated statements of operations",
        "consolidated statements of operations (unaudited)",
        "consolidated statement of operations",
        "consolidated statements of earnings",
        "consolidated statement of earnings",
        "consolidated statements of income",
        "consolidated statement of income",
        "consolidated income statements",
        "consolidated income statement",
        "condensed consolidated statements of earnings",
        "consolidated results of operations",
        "consolidated statements of income (loss)",
        "consolidated statements of income - southern",
        "consolidated statements of operations and comprehensive income",
        "consolidated statements of income and comprehensive income",
        "consolidated statements of comprehensive income",
    ],
    "cash_flow_statement": [
        "cash flows statement",
        "cash flows statements",
        "statement of cash flows",
        "statements of consolidated cash flows",
        "consolidated statements of cash flows",
        "consolidated statement of cash flows",
        "consolidated statement of cash flow",
        "consolidated cash flows statements",
        "consolidated cash flow statements",
        "condensed consolidated statements of cash flows",
        "consolidated statements of cash flows (unaudited)",
        "consolidated statements of cash flows - southern",
    ],
}


def cik_matching_ticker(ticker, headers=headers):
    ticker = ticker.upper().replace(".", "-")
    ticker_json = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=headers
    ).json()

    for company in ticker_json.values():
        if company["ticker"] == ticker:
            cik = str(company["cik_str"]).zfill(10)
            return cik
    raise ValueError(f"Ticker {ticker} not found in SEC database")


def get_submission_data_for_ticker(ticker, headers=headers, only_filings_df=False):
    """
    Get the data in json form for a given ticker. For example: 'cik', 'entityType', 'sic', 'sicDescription', 'insiderTransactionForOwnerExists', 'insiderTransactionForIssuerExists', 'name', 'tickers', 'exchanges', 'ein', 'description', 'website', 'investorWebsite', 'category', 'fiscalYearEnd', 'stateOfIncorporation', 'stateOfIncorporationDescription', 'addresses', 'phone', 'flags', 'formerNames', 'filings'

    Args:
        ticker (str): The ticker symbol of the company.

    Returns:
        json: The submissions for the company.
    """
    cik = cik_matching_ticker(ticker)
    headers = headers
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    company_json = requests.get(url, headers=headers).json()
    if only_filings_df:
        return pd.DataFrame(company_json["filings"]["recent"])
    else:
        return company_json


def get_filtered_filings(
    ticker, ten_k=True, just_accession_numbers=False, headers=headers
):
    company_filings_df = get_submission_data_for_ticker(
        ticker, only_filings_df=True, headers=headers
    )
    if ten_k:
        df = company_filings_df[company_filings_df["form"] == "10-K"]
    else:
        df = company_filings_df[company_filings_df["form"] == "10-Q"]
    
    if just_accession_numbers:
        df = df.set_index("reportDate")
        accession_df = df["accessionNumber"]
        return accession_df
    else:
        return df


def get_facts(ticker, headers=headers):
    cik = cik_matching_ticker(ticker)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    company_facts = requests.get(url, headers=headers).json()
    return company_facts


def facts_DF(ticker, headers=headers):
    facts = get_facts(ticker, headers)
    us_gaap_data = facts["facts"]["us-gaap"]
    df_data = []
    for fact, details in us_gaap_data.items():
        for unit in details["units"]:
            for item in details["units"][unit]:
                row = item.copy()
                row["fact"] = fact
                df_data.append(row)

    df = pd.DataFrame(df_data)
    df["end"] = pd.to_datetime(df["end"])
    df["start"] = pd.to_datetime(df["start"])
    df = df.drop_duplicates(subset=["fact", "end", "val"])
    df.set_index("end", inplace=True)
    labels_dict = {fact: details["label"] for fact, details in us_gaap_data.items()}
    return df, labels_dict


def annual_facts(ticker, headers=headers):
    accession_nums = get_filtered_filings(
        ticker, ten_k=True, just_accession_numbers=True
    )
    df, label_dict = facts_DF(ticker, headers)
    ten_k = df[df["accn"].isin(accession_nums)]
    ten_k = ten_k[ten_k.index.isin(accession_nums.index)]
    pivot = ten_k.pivot_table(values="val", columns="fact", index="end")
    pivot.rename(columns=label_dict, inplace=True)
    return pivot.T


def quarterly_facts(ticker, headers=headers):
    accession_nums = get_filtered_filings(
        ticker, ten_k=False, just_accession_numbers=True
    )
    df, label_dict = facts_DF(ticker, headers)
    ten_q = df[df["accn"].isin(accession_nums)]
    ten_q = ten_q[ten_q.index.isin(accession_nums.index)].reset_index(drop=False)
    ten_q = ten_q.drop_duplicates(subset=["fact", "end"], keep="last")
    pivot = ten_q.pivot_table(values="val", columns="fact", index="end")
    pivot.rename(columns=label_dict, inplace=True)
    return pivot.T


def save_dataframe_to_csv(dataframe, folder_name, ticker, statement_name, frequency):
    directory_path = os.path.join(folder_name, ticker)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"{statement_name}_{frequency}.csv")
    dataframe.to_csv(file_path)
    return None


def _get_file_name(report):
    html_file_name_tag = report.find("HtmlFileName")
    xml_file_name_tag = report.find("XmlFileName")

    if html_file_name_tag:
        return html_file_name_tag.text
    elif xml_file_name_tag:
        return xml_file_name_tag.text
    else:
        return ""


def _is_statement_file(short_name_tag, long_name_tag, file_name):
    return (
        short_name_tag is not None
        and long_name_tag is not None
        and file_name  # Check if file_name is not an empty string
        and "Statement" in long_name_tag.text
    )


def get_statement_file_names_in_filing_summary(
    ticker, accession_number, headers=headers
):
    try:
        session = requests.Session()
        cik = cik_matching_ticker(ticker)
        base_link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}"
        filing_summary_link = f"{base_link}/FilingSummary.xml"
        filing_summary_response = session.get(
            filing_summary_link, headers=headers
        ).content.decode("utf-8")

        filing_summary_soup = BeautifulSoup(filing_summary_response, "lxml-xml")
        statement_file_names_dict = {}

        for report in filing_summary_soup.find_all("Report"):
            file_name = _get_file_name(report)
            short_name, long_name = report.find("ShortName"), report.find("LongName")

            if _is_statement_file(short_name, long_name, file_name):
                statement_file_names_dict[short_name.text.lower()] = file_name

        return statement_file_names_dict

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {}


def get_statement_soup(
    ticker,
    accession_number,
    statement_name,
    headers,
    statement_keys_map,
):
    """
    the statement_name should be one of the following:
    'balance_sheet'
    'income_statement'
    'cash_flow_statement'
    """
    session = requests.Session()

    cik = cik_matching_ticker(ticker)
    base_link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}"

    statement_file_name_dict = get_statement_file_names_in_filing_summary(
        ticker, accession_number, headers
    )

    statement_link = None
    for possible_key in statement_keys_map.get(statement_name.lower(), []):
        file_name = statement_file_name_dict.get(possible_key.lower())
        if file_name:
            statement_link = f"{base_link}/{file_name}"
            break

    if not statement_link:
        raise ValueError(f"Could not find statement file name for {statement_name}")

    try:
        statement_response = session.get(statement_link, headers=headers)
        statement_response.raise_for_status()  # Check if the request was successful

        if statement_link.endswith(".xml"):
            return BeautifulSoup(
                statement_response.content, "lxml-xml", from_encoding="utf-8"
            )
        else:
            return BeautifulSoup(statement_response.content, "lxml")

    except requests.RequestException as e:
        raise ValueError(f"Error fetching the statement: {e}")
    
def extract_columns_values_and_dates_from_statement(soup):
    """
    Extracts columns, values, and dates from an HTML soup object representing a financial statement.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the HTML document.

    Returns:
        tuple: Tuple containing columns, values_set, and date_time_index.
    """
    columns = []
    values_set = []
    date_time_index = get_datetime_index_dates_from_statement(soup)

    for table in soup.find_all("table"):
        unit_multiplier = 1
        special_case = False

        # Check table headers for unit multipliers and special cases
        table_header = table.find("th")
        if table_header:
            header_text = table_header.get_text()
            # Determine unit multiplier based on header text
            if "in Thousands" in header_text:
                unit_multiplier = 1000
            elif "in Millions" in header_text:
                unit_multiplier = 1000000
            # Check for special case scenario
            if "unless otherwise specified" in header_text:
                special_case = True

        # Process each row of the table
        for row in table.select("tr"):
            onclick_elements = row.select("td.pl a, td.pl.custom a")
            if not onclick_elements:
                continue

            # Extract column title from 'onclick' attribute
            onclick_attr = onclick_elements[0]["onclick"]
            column_title = onclick_attr.split("defref_")[-1].split("',")[0]
            columns.append(column_title)

            # Initialize values array with NaNs
            values = [np.NaN] * len(date_time_index)

            # Process each cell in the row
            for i, cell in enumerate(row.select("td.text, td.nump, td.num")):
                if "text" in cell.get("class"):
                    continue

                # Clean and parse cell value
                value = keep_numbers_and_decimals_only_in_string(
                    cell.text.replace("$", "")
                    .replace(",", "")
                    .replace("(", "")
                    .replace(")", "")
                    .strip()
                )
                if value:
                    value = float(value)
                    # Adjust value based on special case and cell class
                    if special_case:
                        value /= 1000
                    else:
                        if "nump" in cell.get("class"):
                            values[i] = value * unit_multiplier
                        else:
                            values[i] = -value * unit_multiplier

            values_set.append(values)

    return columns, values_set, date_time_index


def get_datetime_index_dates_from_statement(soup: BeautifulSoup) -> pd.DatetimeIndex:
    """
    Extracts datetime index dates from the HTML soup object of a financial statement.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the HTML document.

    Returns:
        pd.DatetimeIndex: A Pandas DatetimeIndex object containing the extracted dates.
    """
    table_headers = soup.find_all("th", {"class": "th"})
    dates = [str(th.div.string) for th in table_headers if th.div and th.div.string]
    dates = [standardize_date(date).replace(".", "") for date in dates]
    index_dates = pd.to_datetime(dates)
    return index_dates


def standardize_date(date: str) -> str:
    """
    Standardizes date strings by replacing abbreviations with full month names.

    Args:
        date (str): The date string to be standardized.

    Returns:
        str: The standardized date string.
    """
    for abbr, full in zip(calendar.month_abbr[1:], calendar.month_name[1:]):
        date = date.replace(abbr, full)
    return date


def keep_numbers_and_decimals_only_in_string(mixed_string: str):
    """
    Filters a string to keep only numbers and decimal points.

    Args:
        mixed_string (str): The string containing mixed characters.

    Returns:
        str: String containing only numbers and decimal points.
    """
    num = "1234567890."
    allowed = list(filter(lambda x: x in num, mixed_string))
    return "".join(allowed)


def create_dataframe_of_statement_values_columns_dates(
    values_set, columns, index_dates
) -> pd.DataFrame:
    """
    Creates a DataFrame from statement values, columns, and index dates.

    Args:
        values_set (list): List of values for each column.
        columns (list): List of column names.
        index_dates (pd.DatetimeIndex): DatetimeIndex for the DataFrame index.

    Returns:
        pd.DataFrame: DataFrame constructed from the given data.
    """
    transposed_values_set = list(zip(*values_set))
    df = pd.DataFrame(transposed_values_set, columns=columns, index=index_dates)
    return df


def process_one_statement(ticker, accession_number, statement_name):
    """
    Processes a single financial statement identified by ticker, accession number, and statement name.

    Args:
        ticker (str): The stock ticker.
        accession_number (str): The SEC accession number.
        statement_name (str): Name of the financial statement.

    Returns:
        pd.DataFrame or None: DataFrame of the processed statement or None if an error occurs.
    """
    try:
        # Fetch the statement HTML soup
        soup = get_statement_soup(
            ticker,
            accession_number,
            statement_name,
            headers=headers,
            statement_keys_map=statement_keys_map,
        )
    except Exception as e:
        logging.error(
            f"Failed to get statement soup for {ticker}: {e} for accession number: {accession_number}"
        )
        return None

    if soup:
        try:
            # Extract data and create DataFrame
            columns, values, dates = extract_columns_values_and_dates_from_statement(
                soup
            )
            df = create_dataframe_of_statement_values_columns_dates(
                values, columns, dates
            )

            if not df.empty:
                # Remove duplicate columns
                df = df.T.drop_duplicates()
            else:
                logging.warning(
                    f"Empty DataFrame for accession number: {accession_number}"
                )
                return None

            return df
        except Exception as e:
            logging.error(f"Error processing statement: {e}")
            return None
        
def get_label_dictionary(ticker, headers):
    facts = get_facts(ticker, headers)
    us_gaap_data = facts["facts"]["us-gaap"]
    labels_dict = {fact: details["label"] for fact, details in us_gaap_data.items()}
    return labels_dict


def rename_statement(statement, label_dictionary):
    # Extract the part after the first "_" and then map it using the label dictionary
    statement.index = statement.index.map(
        lambda x: label_dictionary.get(x.split("_", 1)[-1], x)
    )
    return statement

def process_all_statements_for_ticker(ticker, headers=headers):        

        # Obtem todos os accession numbers para o ticker
        accn_df = get_filtered_filings(ticker, ten_k=True, just_accession_numbers=False, headers=headers)
        accn_list = accn_df['accessionNumber'].tolist()  # Converte a coluna de accessionNumber para uma lista

        for i in range(len(accn_list)):
                accn_list[i] = accn_list[i].replace("-", "")    

        #print(accn_list)

        # Inicializa um dicionário para armazenar os demonstrativos financeiros
        all_statements = {}

        #label_dict = get_label_dictionary(ticker, headers)

        # Itera sobre cada accession number
        for j in range(len(accn_list)):
                acc_num = accn_list[j]  # Remove hífens do accession number
                
                # Inicializa um dicionário para armazenar cada demonstrativo do accession_number
                statements = {}

                # Tenta processar cada tipo de demonstrativo para o accession_number atual
                for statement_name in ["balance_sheet", "income_statement", "cash_flow_statement"]:
                        try:
                            df = process_one_statement(ticker, acc_num, statement_name)
                                #df = statement = rename_statement(df, label_dict)
                            if df is not None:
                                # Adiciona o dataframe ao dicionário, após formatar as colunas de data
                                statements[statement_name] = df #clean_statement(df)
                        except Exception as e:
                                logging.error(f"Erro ao processar {statement_name} para {ticker} em {acc_num}: {e}")

                # Adiciona os demonstrativos processados ao dicionário principal
                if statements:
                        all_statements[acc_num] = statements

        return all_statements

# Função para extrair cada tipo de statement em um DataFrame separado com data como coluna e remoção de duplicatas
def create_financial_statement_data_frame(all_statements, statement):

    key_list = list(all_statements.keys())

    # Iniciar o DataFrame acumulado como vazio
    df_acumulado = pd.DataFrame()

    for chave in key_list:
        # Extrair o DataFrame correspondente para a chave atual, mantendo apenas as duas primeiras colunas e removendo duplicatas
        df_atual = all_statements[chave][statement].reset_index().iloc[:, :2].drop_duplicates(subset='index', keep='first')
        
        # Configurar o índice para a coluna 'index' para possibilitar a junção
        df_atual.set_index('index', inplace=True)
        
        if df_acumulado.empty:
            # Se for o primeiro DataFrame, inicialize df_acumulado com ele
            df_acumulado = df_atual
        else:
            # Fazer uma junção externa com o DataFrame acumulado
            df_acumulado = pd.concat([df_acumulado, df_atual], axis=1, join='outer')

    # Resetar o índice para ter a coluna 'index' como coluna regular novamente
    df_acumulado.reset_index(inplace=True)

    # Transformando as colunas de datas a partir da segunda coluna
    # Obtenha todas as colunas exceto a primeira
    colunas_datas = df_acumulado.columns[1:]

    # Renomeie as colunas usando strftime
    novos_nomes = ['index'] + [pd.to_datetime(coluna).strftime('%Y-%m-%d') for coluna in colunas_datas]

    # Aplicando os novos nomes ao DataFrame
    df_acumulado.columns = novos_nomes
    # Exibir o DataFrame final com todos os dados juntos
    #print("DataFrame final com todas as junções:")
    return df_acumulado

# Função para coletar todas as demonstrações financeiras
def get_all_financials(symbol, api_key):
    """
    Coleta todas as demonstrações financeiras de uma ação usando a Alpha Vantage.
    
    Args:
        symbol (str): Código da ação (ticker), por exemplo, 'PLD' para Prologis.
    
    Returns:
        dict: Dicionário com DataFrames de Income Statement, Balance Sheet e Cash Flow.
    """
    # Tipos de relatórios financeiros
    report_types = {
        'INCOME_STATEMENT': 'Demonstração de Resultados',
        'BALANCE_SHEET': 'Balanço Patrimonial',
        'CASH_FLOW': 'Fluxo de Caixa'
    }
    
    # Dicionário para armazenar os DataFrames
    financial_data = {}
    
    # Loop para coletar cada tipo de demonstração
    for report_type, report_name in report_types.items():
        url = f'https://www.alphavantage.co/query?function={report_type}&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        
        # Verifica se a resposta contém dados válidos e armazena no dicionário
        if 'annualReports' in data:
            reports = data['annualReports']
            df = pd.DataFrame(reports)
            financial_data[report_name] = df
        else:
            print(f"Erro: Dados para {report_name} não disponíveis.")
    
    return financial_data

def get_ticker_price(ticker, date):
    """
    Coleta o Market Cap e o Ticker Price para uma data específica.

    Args:
    ticker (str): Símbolo da ação.
    date (str): Data para coletar os dados financeiros (formato 'YYYY-MM-DD').

    Returns:
    dict: Contém o Market Cap e o Ticker Price na data especificada.
    """
    # Define o intervalo para buscar os dados (um dia antes e um dia depois, para garantir o dado exato se estiver disponível)
    start_date = (pd.to_datetime(date) - pd.Timedelta(days=2)).strftime('%Y-%m-%d')
    end_date = (pd.to_datetime(date) + pd.Timedelta(days=2)).strftime('%Y-%m-%d')
    
    # Baixa os dados de preços históricos para o intervalo
    stock = yf.Ticker(ticker)
    historical_data = stock.history(start=start_date, end=end_date)
    
    # Primeiro, tenta encontrar dados exatamente na data desejada
    if date in historical_data.index:
        nearest_date = date
    # Se não houver dados na data exata, tenta a última data disponível antes dela
    elif not historical_data.empty:
        nearest_date = historical_data.index[-1]
    else:
        return {"error": f"Dados não encontrados para {ticker} na data {date} ou antes dela."}
    
    # Pega o preço de fechamento e calcula o Market Cap
    closing_price = historical_data.loc[nearest_date, 'Close']
    
    return closing_price

def get_overview_data(symbol, api_key):
    """
    Coleta dados gerais da empresa, como MarketCap e Shares Outstanding.
    """
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    shares_outstanding = safe_float(data.get('SharesOutstanding'))
    return shares_outstanding

def get_dividends_data(symbol, api_key):
    """
    Coleta dados de dividendos e organiza por ano para somar os dividendos anuais.
    """
    url = f'https://www.alphavantage.co/query?function=DIVIDENDS&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    dividends_by_year = {}

    if 'data' in data:
        for record in data['data']:
            date = record['ex_dividend_date']
            year = date[:4]  # Extrai o ano
            dividend = safe_float(record.get('amount'))

            if year in dividends_by_year:
                dividends_by_year[year].append(dividend)
            else:
                dividends_by_year[year] = [dividend]
    
    # Processa os dividendos anuais
    annual_dividends = {}
    for year, dividends in dividends_by_year.items():
        if len(dividends) < 4:
            estimated_annual_dividend = sum(dividends) * (4 / len(dividends))
        else:
            estimated_annual_dividend = sum(dividends)
        annual_dividends[year] = estimated_annual_dividend
    
    return annual_dividends

def safe_float(value):
    """Converte o valor para float, substituindo valores nulos ou inválidos por 0."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def calculate_reit_metrics_API(symbol, api_key):
    """
    Calcula métricas financeiras úteis para análise de REITs usando dados das demonstrações financeiras.
    Args:
        symbol (str): Código da ação (ticker), por exemplo, 'PLD' para Prologis.
    Returns:
        DataFrame: DataFrame com métricas e múltiplos úteis para análise de REITs.
    """
    # Coleta as demonstrações financeiras
    financials = get_all_financials(symbol, api_key)
    if not financials:
        print("Erro ao obter as demonstrações financeiras.")
        return None
    
    # Coleta dados gerais e de dividendos
    shares_outstanding = get_overview_data(symbol, api_key)
    dividends_data = get_dividends_data(symbol, api_key)

    # Extrair cada uma das demonstrações
    income_df = financials.get('Demonstração de Resultados')
    balance_df = financials.get('Balanço Patrimonial')
    cash_flow_df = financials.get('Fluxo de Caixa')
    
    # DataFrame final para armazenar métricas
    metrics_df = pd.DataFrame()
    
    # Loop por períodos para calcular as métricas (assume-se que os períodos estão alinhados)
    for idx in range(len(income_df)):
        fiscal_date = income_df.iloc[idx]['fiscalDateEnding']
        period = income_df.iloc[idx]['fiscalDateEnding'][:4]  # Ano do período fiscal
        
        share_price = get_ticker_price(symbol, fiscal_date)
        market_cap = share_price * shares_outstanding

        # Dividendos anuais a partir dos dados coletados
        dividends = dividends_data.get(str(period), 0)
        
        # Pega os dados financeiros específicos usando safe_float
        revenue = safe_float(income_df.iloc[idx].get('totalRevenue'))
        net_income = safe_float(income_df.iloc[idx].get('netIncome'))
        gross_income = safe_float(income_df.iloc[idx].get('grossProfit')) 
        total_assets = safe_float(balance_df.iloc[idx].get('totalAssets'))
        total_liabilities = safe_float(balance_df.iloc[idx].get('totalLiabilities'))
        total_debt = safe_float(balance_df.iloc[idx].get('shortLongTermDebtTotal'))
        total_debt_expense = safe_float(income_df.iloc[idx].get('interestAndDebtExpense'))
        ebitda = safe_float(income_df.iloc[idx].get('ebitda'))
        capex = safe_float(cash_flow_df.iloc[idx].get('capitalExpenditures'))
        
        # Coleta dividendos pagos e fluxos operacionais do cash flow statement
        #dividends_paid = safe_float(cash_flow_df.iloc[idx].get('dividendPayout'))
        operating_cash_flow = safe_float(cash_flow_df.iloc[idx].get('operatingCashflow'))
        
        # Calcula o NOI com aproximações; substituir conforme disponível
        rental_income = revenue  # Placeholder para receita de aluguel
        ancillary_income = 0     # Placeholder para receitas adicionais
        direct_operating_expenses = revenue * 0.2  # Aproximação de despesas operacionais diretas (20% da receita)
        noi = rental_income + ancillary_income - direct_operating_expenses
        
        # Cálculos de métricas de REIT
        ffo = net_income + safe_float(income_df.iloc[idx].get('depreciationAndAmortization')) - total_debt_expense # Aproximação de FFO
        ffo_ps = ffo/shares_outstanding
        p_ffo = share_price / ffo_ps
        ffo_yield = ffo / noi
        affo = ffo - capex  # Aproximação de AFFO
        dividend_yield = (dividends / share_price) if share_price else 0
        debt_to_ebitda = (total_debt / ebitda) if ebitda else None
        payout_ratio = (dividends / ffo_ps) if ffo_ps else None
        debt_coverage = (noi / total_debt_expense) if total_debt_expense else None

        gross_margin = gross_income/revenue
        net_margin = net_income/revenue
        
        # NAV e Cap Rate
        nav = (total_assets - total_liabilities) / shares_outstanding if shares_outstanding else None
        cap_rate = noi / total_assets if total_assets else None
        
        # Adiciona os dados ao DataFrame final
        metrics_df = metrics_df.append({
            'REIT': symbol,
            'Data Fiscal': fiscal_date, 
            'Período': period,
            'Preço do REIT': share_price,
            'Market Cap': market_cap,
            'Shares Outstanding': shares_outstanding,
            'Receita Total': revenue,
            'Fluxo de Caixa Operacional': operating_cash_flow,
            'Margem Bruta': gross_margin,
            'Lucro Líquido': net_income,
            'Margem Líquida': net_margin,
            'FFO': ffo,
            'AFFO': affo,
            'Price to FFO': p_ffo,
            'FFO Yield': ffo_yield,
            'CAPEX': capex,
            'NAV': nav,
            'NOI': noi,
            'Cap Rate': cap_rate,
            'Dividendos Anuais (Por Ação)': dividends,
            'Dividend Yield': dividend_yield,
            'Payout Ratio': payout_ratio,
            'Dívida Total': total_debt,
            'Debt-to-EBITDA': debt_to_ebitda,
            'Cobertura de Juros': debt_coverage
        }, ignore_index=True)
    
    return metrics_df

#///////////////////////////////////////////////////////

def calculate_reit_metrics_EDGAR(symbol, headers, file_path):
    """
    Calcula métricas financeiras úteis para análise de REITs usando dados das demonstrações financeiras.
    Args:
        symbol (str): Código da ação (ticker), por exemplo, 'PLD' para Prologis.
    Returns:
        DataFrame: DataFrame com métricas e múltiplos úteis para análise de REITs.
    """
    # Coleta as demonstrações financeiras
    all_statements = process_all_statements_for_ticker(symbol, headers=headers)
    
    # Extrair cada uma das demonstrações
    balance_df = create_financial_statement_data_frame(all_statements,'balance_sheet').set_index('index')
    income_df = create_financial_statement_data_frame(all_statements,'income_statement').set_index('index')
    cash_flow_df = create_financial_statement_data_frame(all_statements,'cash_flow_statement').set_index('index')

    base_reits = pd.read_excel(file_path)
    sector = base_reits.loc[base_reits['Ticker'] == symbol, 'Sector'].values[0]

    # DataFrame final para armazenar métricas
    metrics_df = pd.DataFrame()

    df_columns = income_df.columns

    ticker = []
    reit_sector = []
    fiscal_statement_date = []
    metrics_period = []
            
    # Coleta dados gerais e de dividendos
    shares_outstanding = []#get_overview_data(symbol, api_key)
    dividends_data = []#get_dividends_data(symbol, api_key)

    share_price = []
    market_cap = []

    # Dividendos anuais a partir dos dados coletados
    dividends = []
            
    # Pega os dados financeiros específicos usando safe_float
    revenue = []
    net_income = []
    gross_income = []
    total_assets = []
    total_liabilities = []
    total_debt = []
    total_debt_expense = []
    depr_amort = []
    taxes = []
    ebitda = []
    capex = []
            
    # Coleta dividendos pagos e fluxos operacionais do cash flow statement
    operating_cash_flow = []
            
    # Calcula o NOI com aproximações; substituir conforme disponível
    rental_income = []  # Placeholder para receita de aluguel
    ancillary_income = []     # Placeholder para receitas adicionais
    direct_operating_expenses = []
    noi = []
            
    # Cálculos de métricas de REIT
    ffo = []
    ffo_ps = []
    p_ffo = []
    ffo_yield = []
    affo = []
    dividend_yield = []
    debt_to_ebitda = []
    payout_ratio = []
    debt_coverage = []

    gross_margin = []
    net_margin = []
            
    # NAV e Cap Rate
    nav = []
    nav_ps = []
    cap_rate = []
    
    # Loop por períodos para calcular as métricas (assume-se que os períodos estão alinhados)
    for i in range(len(df_columns)):

        fiscal_date = df_columns[i]
        period = fiscal_date[:4]  # Ano do período fiscal
        
        ticker.append(symbol)
        reit_sector.append(sector)
        fiscal_statement_date.append(fiscal_date)
        metrics_period.append(period)

        # Coleta dados gerais e de dividendos
        shares_period = income_df.loc['us-gaap_WeightedAverageNumberOfSharesOutstandingBasic'][fiscal_date]#get_overview_data(symbol, api_key)
        shares_outstanding.append(shares_period)
        dividends_period = -1 * cash_flow_df.loc['us-gaap_PaymentsOfDividends'][fiscal_date]
        dividends_data.append(dividends_period) #get_dividends_data(symbol, api_key)

        share_price_period = get_ticker_price(symbol, fiscal_date)
        share_price.append(share_price_period)
        market_cap.append(share_price_period * shares_period)

        # Dividendos anuais a partir dos dados coletados
        dividends.append(dividends_period / shares_period)
        
        # Pega os dados financeiros específicos usando safe_float
        revenue.append(safe_float(income_df.loc['us-gaap_Revenues'][fiscal_date]))
        net_income.append(safe_float(income_df.loc['us-gaap_NetIncomeLoss'][fiscal_date]))
        gross_income.append(safe_float(income_df.loc['us-gaap_OperatingIncomeLoss'][fiscal_date]))
        total_assets.append(safe_float(balance_df.loc['us-gaap_Assets'][fiscal_date]))
        total_liabilities.append(safe_float(balance_df.loc['us-gaap_Liabilities'][fiscal_date]))
        total_debt.append(safe_float(balance_df.loc['us-gaap_LongTermDebt'][fiscal_date]))
        total_debt_expense.append(safe_float(-1 * income_df.loc['us-gaap_InterestExpense'][fiscal_date]))
        depr_amort.append(safe_float(income_df.loc['us-gaap_DepreciationAndAmortization'][fiscal_date]))
        taxes.append(safe_float(-1 * income_df.loc['us-gaap_IncomeTaxExpenseBenefit'][fiscal_date]))        
        ebitda.append(safe_float( net_income[i] + depr_amort[i] + taxes[i] + total_debt_expense[i]))
        capex.append(safe_float(-1 * cash_flow_df.loc['us-gaap_PaymentsToAcquireRealEstate'][fiscal_date]))
        
        # Coleta dividendos pagos e fluxos operacionais do cash flow statement
        #dividends_paid = safe_float(cash_flow_df.iloc[idx].get('dividendPayout'))
        operating_cash_flow.append(safe_float(cash_flow_df.loc['us-gaap_NetCashProvidedByUsedInOperatingActivities'][fiscal_date]))
        
        # Calcula o NOI com aproximações; substituir conforme disponível
        rental_income.append(safe_float(income_df.loc['pld_RentalRevenue'][fiscal_date]))  # Placeholder para receita de aluguel
        ancillary_income.append(safe_float(income_df.loc['pld_OtherRealEstateRevenue1'][fiscal_date]))     # Placeholder para receitas adicionais
        direct_operating_expenses.append(safe_float(income_df.loc['us-gaap_DirectCostsOfLeasedAndRentedPropertyOrEquipment'][fiscal_date])) # Aproximação de despesas operacionais diretas (20% da receita)
        noi.append(rental_income[i] + ancillary_income[i] - direct_operating_expenses[i])
        
        # Cálculos de métricas de REIT
        ffo.append(net_income[i] + depr_amort[i] - total_debt_expense[i]) # Aproximação de FFO
        ffo_ps.append(ffo[i]/shares_outstanding[i])
        p_ffo.append(share_price[i] / ffo_ps[i])
        ffo_yield.append(ffo[i] / noi[i])
        affo.append(ffo[i] - capex[i])  # Aproximação de AFFO
        dividend_yield.append((dividends_period / share_price[i]) if share_price[i] else 0)
        debt_to_ebitda.append((total_debt[i] / ebitda[i]) if ebitda[i] else None)
        payout_ratio.append((dividends[i] / ffo_ps[i]) if ffo_ps[i] else None)
        debt_coverage.append((noi[i] / total_debt_expense[i]) if total_debt_expense[i] else None)

        gross_margin.append(gross_income[i]/revenue[i])
        net_margin.append(net_income[i]/revenue[i])
        
        # NAV e Cap Rate
        nav.append((total_assets[i] - total_liabilities[i]))
        nav_ps.append((total_assets[i] - total_liabilities[i]) / shares_outstanding[i] if shares_outstanding[i] else None)
        cap_rate.append(noi[i] / total_assets[i] if total_assets[i] else None)
        
    # Cria o DataFrame diretamente a partir das listas
    metrics_df = pd.DataFrame({
        'REIT': ticker,
        'Setor': reit_sector,
        'Data Fiscal': fiscal_statement_date, 
        'Período': metrics_period,
        'Preço do REIT': share_price,
        'Market Cap': market_cap,
        'Shares Outstanding': shares_outstanding,
        'Receita Total': revenue,
        'Fluxo de Caixa Operacional': operating_cash_flow,
        'Margem Bruta': gross_margin,
        'Lucro Líquido': net_income,
        'Margem Líquida': net_margin,
        'FFO': ffo,
        'AFFO': affo,
        'Price to FFO': p_ffo,
        'FFO Yield': ffo_yield,
        'CAPEX': capex,
        'NAV': nav,
        'NAV (Por Ação)': nav_ps,
        'NOI': noi,
        'Cap Rate': cap_rate,
        'Dividendos Anuais (Por Ação)': dividends,
        'Dividend Yield': dividend_yield,
        'Payout Ratio': payout_ratio,
        'Dívida Total': total_debt,
        'Debt-to-EBITDA': debt_to_ebitda,
        'Cobertura de Juros': debt_coverage
    })

    # Exibe o DataFrame resultante
    return metrics_df#, balance_df, income_df, cash_flow_df

def metric_growth(df):
    """
    Calcula o crescimento percentual de uma coluna específica em comparação ao ano anterior.

    Args:
    df (DataFrame): DataFrame com os dados financeiros.
    coluna (str): Nome da coluna para calcular o crescimento percentual.

    Returns:
    DataFrame: DataFrame original com uma nova coluna para o crescimento percentual.
    """
    # Inicializa o dataframe
    df_cresc = df[['REIT','Setor', 'Data Fiscal', 'Período']]

    # Seleciona apenas as colunas numéricas para cálculo de crescimento
    colunas_calculo = [col for col in df.columns if col not in ['REIT', 'Data Fiscal', 'Período']]

    # Calcula o crescimento percentual para cada coluna numérica
    for coluna in colunas_calculo:
        crescimento_percentual = []
        for i in range(len(df) - 1):
            valor_atual = df.loc[i, coluna]
            valor_anterior = df.loc[i + 1, coluna]

            # Verifica se o valor anterior não é zero para evitar divisão por zero
            if valor_anterior != 0:
                try:
                    crescimento = ((valor_atual - valor_anterior) / valor_anterior) * 100
                    crescimento_percentual.append(crescimento)
                except:
                    crescimento_percentual.append(None)
            else:
                crescimento_percentual.append(None)
        
        # Adiciona o valor None para a última linha (sem crescimento percentual para o último ano)
        crescimento_percentual.append(None)
        
        # Adiciona a coluna de crescimento ao DataFrame de crescimento
        # Adiciona a coluna de crescimento ao DataFrame de crescimento
        df_cresc = df_cresc.copy()
        df_cresc['Crescimento (%) ' + coluna] = crescimento_percentual

    return df_cresc

def generate_graphs(reit_df_metrics):
    """
    Gera gráficos de barras e linhas para análise de métricas financeiras de REITs,
    exibindo os dados do menor para o maior ano.
    
    Args:
    reit_df (DataFrame): DataFrame com dados financeiros de REITs.
    """
    # Ordena o DataFrame pelo período (ano) de forma crescente
    reit_df = reit_df_metrics.sort_values(by='Período', ascending=True).reset_index(drop=True)
    
    # Configurações gerais dos gráficos usando o estilo ggplot
    plt.style.use('ggplot')
    
    # Converte a coluna 'Período' em string para melhor apresentação nos gráficos
    reit_df['Período'] = reit_df['Período'].astype(str)

    # Gráfico 1: Receita Total, Lucro Líquido e Fluxo de Caixa Operacional com Margem Bruta e Margem Líquida no eixo secundário
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    # Ajusta o espaçamento entre barras e as posições
    bar_width = 0.25
    x = range(len(reit_df['Período']))
    
    # Gráficos de barras
    ax1.bar([i - bar_width for i in x], reit_df['Receita Total'], color='skyblue', width=bar_width, label='Receita Total')
    ax1.bar(x, reit_df['Lucro Líquido'], color='orange', width=bar_width, label='Lucro Líquido')
    ax1.bar([i + bar_width for i in x], reit_df['Fluxo de Caixa Operacional'], color='green', width=bar_width, label='Fluxo de Caixa Operacional')

    # Gráficos de linhas para margens
    ax2.plot(reit_df['Período'], reit_df['Margem Bruta'], color='blue', marker='o', label='Margem Bruta')
    ax2.plot(reit_df['Período'], reit_df['Margem Líquida'], color='red', marker='o', label='Margem Líquida')

    # Legendas e labels
    ax1.set_xlabel('Período')
    ax1.set_ylabel('Valores Financeiros')
    ax2.set_ylabel('Margens (%)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(reit_df['Período'])
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.set_title("Receita, Lucro, Fluxo de Caixa e Margens (%)")

    # Exibir gráfico
    plt.show()

    # Gráfico 2: Linha para Preço do REIT com eixo secundário para Price to FFO
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(reit_df['Período'], reit_df['Preço do REIT'], color='purple', marker='o', linestyle='-', label='Preço do REIT')
    ax2.plot(reit_df['Período'], reit_df['Price to FFO'], color='grey', marker='s', linestyle='--', label='Price to FFO')

    # Labels e título
    ax1.set_xlabel('Período')
    ax1.set_ylabel('Preço do REIT')
    ax2.set_ylabel('Price to FFO')
    ax1.set_title("Evolução do Preço do REIT e Price to FFO")
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.show()

    # Gráfico 3: Barras para Dividendos Anuais com Linha de Dividend Yield no eixo secundário
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # Gráficos de barras para Dividendos Anuais
    ax1.bar(reit_df['Período'], reit_df['Dividendos Anuais (Por Ação)'], color='lightcoral', label='Dividendos Anuais (Por Ação)')

    # Linha para Dividend Yield
    ax2.plot(reit_df['Período'], reit_df['Dividend Yield'], color='darkred', marker='o', label='Dividend Yield')

    # Legendas e labels
    ax1.set_xlabel('Período')
    ax1.set_ylabel('Dividendos Anuais (Por Ação)')
    ax2.set_ylabel('Dividend Yield (%)')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.set_title("Dividendos Anuais (Por Ação) e Dividend Yield (%)")

    plt.show()

    # Gráfico 4: FFO em forma de barra com FFO Yield no eixo secundário
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # Barras para FFO
    ax1.bar(reit_df['Período'], reit_df['FFO'], color='lightblue', label='FFO')

    # Linha com pontos para FFO Yield
    ax2.plot(reit_df['Período'], reit_df['FFO Yield'], color='darkblue', marker='o', linestyle='-', label='FFO Yield')

    # Legendas e labels
    ax1.set_xlabel('Período')
    ax1.set_ylabel('FFO')
    ax2.set_ylabel('FFO Yield (%)')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.set_title("FFO e FFO Yield (%)")

    plt.show()

    # Gráfico 5: Dívida Total em forma de barra com Debt-to-EBITDA no eixo secundário
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # Barras para Dívida Total
    ax1.bar(reit_df['Período'], reit_df['Dívida Total'], color='lightgreen', label='Dívida Total')

    # Linha para Debt-to-EBITDA
    ax2.plot(reit_df['Período'], reit_df['Debt-to-EBITDA'], color='darkgreen', marker='o', label='Debt-to-EBITDA')

    # Legendas e labels
    ax1.set_xlabel('Período')
    ax1.set_ylabel('Dívida Total')
    ax2.set_ylabel('Debt-to-EBITDA')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.set_title("Dívida Total e Debt-to-EBITDA")

    plt.show()

