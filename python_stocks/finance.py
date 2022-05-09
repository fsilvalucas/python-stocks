from typing import List, Dict, Union

import pandas as pd
import yfinance as yf
import numpy as np


def get_last_price(tickers: List) -> List[Dict[str, Union[str, float]]]:
    values = yf.download(tickers, period="1d")["Adj Close"]
    aux = []
    for i in values.columns:
        aux.append({'ticker': i,
                    'price': values[i].iloc[0]})

    return aux


def rentability(stocks):
    for i in range(len(stocks)):
        stocks[i] = stocks[i].as_dict
    df = pd.DataFrame(stocks)
    df['qtd'] = df.apply(lambda x: x.qtd if x.operation == 'C' else -x.qtd, axis=1)
    df = df[['ticker', 'date', 'operation', 'qtd', 'price']]
    pivoted_qtd = pd.pivot_table(df, index=['date'], values='qtd', columns=df['ticker'], aggfunc=np.sum).fillna(0)
    pivoted_price = pd.pivot_table(df, index=['date'], values='price', columns=df['ticker'], aggfunc=np.mean).fillna(0)
    prices = yf.download(tickers=(pivoted_price.columns + '.SA').to_list(), start=pivoted_price.index[0], rounding=True)['Adj Close']
    prices.columns = prices.columns.str.rstrip('.SA')
    pivoted_qtd.index = pivoted_qtd.index.astype('datetime64[ns]')
    pivoted_price.index = pivoted_price.index.astype('datetime64[ns]')
    trades = pivoted_qtd.reindex(index=prices.index).fillna(0)
    aportes = (trades * pivoted_price).sum(axis=1)
    posicao = trades.cumsum()
    carteira = posicao * prices
    carteira['saldo'] = carteira.sum(axis=1)
    for i, data in enumerate(aportes.index):
        if i == 0:
            carteira.at[data, 'vl_cota'] = 1
            carteira.at[data, 'qtd_cotas'] = carteira.loc[data]['saldo'].copy()
        else:
            if aportes[data] != 0:
                carteira.at[data, 'qtd_cotas'] = carteira.iloc[i - 1]['qtd_cotas'] + (
                            aportes[data] / carteira.iloc[i - 1]['vl_cota'])
                carteira.at[data, 'vl_cota'] = carteira.iloc[i]['saldo'] / carteira.at[data, 'qtd_cotas']
                carteira.at[data, 'retorno'] = (carteira.iloc[i]['vl_cota'] / carteira.iloc[i - 1]['vl_cota']) - 1
            else:
                carteira.at[data, 'qtd_cotas'] = carteira.iloc[i - 1]['qtd_cotas']
                carteira.at[data, 'vl_cota'] = carteira.iloc[i]['saldo'] / carteira.at[data, 'qtd_cotas']
                carteira.at[data, 'retorno'] = (carteira.iloc[i]['vl_cota'] / carteira.iloc[i - 1]['vl_cota']) - 1

    return (carteira.vl_cota / carteira.vl_cota.shift(1)).fillna(1).reset_index().rename(columns={'vl_cota':'rentability'}).to_dict('records')
