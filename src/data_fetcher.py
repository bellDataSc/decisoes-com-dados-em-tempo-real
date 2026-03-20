"""
data_fetcher.py
Funcoes de coleta de dados financeiros publicos.
Fontes: yfinance, Alpha Vantage (free tier).
"""

import yfinance as yf
import pandas as pd
from typing import List, Optional


def get_stock_info(ticker: str) -> dict:
    """Retorna informacoes fundamentalistas de um ticker via yfinance."""
    stock = yf.Ticker(ticker)
    return stock.info


def get_historical_prices(
    tickers: List[str],
    period: str = "2y",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Baixa precos historicos de fechamento ajustado para uma lista de tickers.

    Args:
        tickers: Lista de simbolos (ex: ['AAPL', 'MSFT'])
        period: Periodo (1mo, 3mo, 6mo, 1y, 2y, 5y)
        interval: Intervalo (1d, 1wk, 1mo)

    Returns:
        DataFrame com precos de fechamento ajustado.
    """
    data = yf.download(tickers, period=period, interval=interval, auto_adjust=True)
    if isinstance(data.columns, pd.MultiIndex):
        return data["Close"]
    return data[["Close"]].rename(columns={"Close": tickers[0]})


def get_fundamentals(tickers: List[str]) -> pd.DataFrame:
    """
    Coleta indicadores fundamentalistas para uma lista de tickers.

    Campos: marketCap, trailingPE, priceToBook, enterpriseToEbitda,
            forwardEps, dividendYield, sector.
    """
    records = []
    fields = [
        "shortName", "sector", "marketCap", "trailingPE",
        "priceToBook", "enterpriseToEbitda", "forwardEps",
        "dividendYield", "totalRevenue", "ebitda"
    ]
    for ticker in tickers:
        info = get_stock_info(ticker)
        row = {"ticker": ticker}
        for f in fields:
            row[f] = info.get(f, None)
        records.append(row)
    return pd.DataFrame(records).set_index("ticker")


def get_free_cash_flow(ticker: str) -> pd.Series:
    """
    Retorna serie historica de Free Cash Flow via yfinance.
    FCF = Operating Cash Flow - Capital Expenditures.
    """
    stock = yf.Ticker(ticker)
    cf = stock.cashflow
    if cf is None or cf.empty:
        raise ValueError(f"Sem dados de cash flow para {ticker}")
    ocf = cf.loc["Operating Cash Flow"] if "Operating Cash Flow" in cf.index else None
    capex = cf.loc["Capital Expenditure"] if "Capital Expenditure" in cf.index else None
    if ocf is None or capex is None:
        raise ValueError(f"Campos de FCF ausentes para {ticker}")
    return (ocf + capex).sort_index()  # capex ja vem negativo no yfinance
