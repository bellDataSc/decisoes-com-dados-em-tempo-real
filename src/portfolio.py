"""
portfolio.py
Metricas de risco-retorno e otimizacao de portfolio (Markowitz).
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Tuple


def calcular_retorno_risco(
    precos: pd.DataFrame,
    periodos_por_ano: int = 252
) -> Tuple[pd.Series, pd.DataFrame]:
    """
    Calcula retornos anualizados e matriz de covariancia anualizada.

    Args:
        precos: DataFrame de precos de fechamento (cada coluna = 1 ativo).
        periodos_por_ano: 252 para diario, 52 para semanal, 12 para mensal.

    Returns:
        Tuple (retornos_anualizados, cov_anualizada)
    """
    retornos_diarios = precos.pct_change().dropna()
    retornos_anualizados = retornos_diarios.mean() * periodos_por_ano
    cov_anualizada = retornos_diarios.cov() * periodos_por_ano
    return retornos_anualizados, cov_anualizada


def sharpe_ratio(
    pesos: np.ndarray,
    retornos: pd.Series,
    cov: pd.DataFrame,
    risk_free: float = 0.05
) -> float:
    """Calcula o Sharpe Ratio negativo (para minimizacao)."""
    ret_portfolio = np.dot(pesos, retornos)
    vol_portfolio = np.sqrt(np.dot(pesos.T, np.dot(cov.values, pesos)))
    return -(ret_portfolio - risk_free) / vol_portfolio


def otimizar_portfolio(
    precos: pd.DataFrame,
    risk_free: float = 0.05,
    periodos_por_ano: int = 252
) -> dict:
    """
    Encontra a alocacao que maximiza o Sharpe Ratio.

    Args:
        precos: DataFrame de precos de fechamento.
        risk_free: Taxa livre de risco (anual).
        periodos_por_ano: 252 para dados diarios.

    Returns:
        Dict com pesos otimos, retorno, volatilidade e Sharpe.
    """
    n = len(precos.columns)
    retornos, cov = calcular_retorno_risco(precos, periodos_por_ano)

    # Restricoes: soma dos pesos = 1
    constraints = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n))
    pesos_iniciais = np.array([1 / n] * n)

    resultado = minimize(
        sharpe_ratio,
        pesos_iniciais,
        args=(retornos, cov, risk_free),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )

    pesos_otimos = resultado.x
    ret_otimo = np.dot(pesos_otimos, retornos)
    vol_otima = np.sqrt(np.dot(pesos_otimos.T, np.dot(cov.values, pesos_otimos)))
    sharpe_otimo = (ret_otimo - risk_free) / vol_otima

    return {
        "tickers": list(precos.columns),
        "pesos": dict(zip(precos.columns, pesos_otimos.round(4))),
        "retorno_anualizado": round(ret_otimo, 4),
        "volatilidade_anualizada": round(vol_otima, 4),
        "sharpe_ratio": round(sharpe_otimo, 4),
        "risk_free": risk_free,
    }


def simular_fronteira_eficiente(
    precos: pd.DataFrame,
    n_portfolios: int = 3000,
    risk_free: float = 0.05,
    periodos_por_ano: int = 252
) -> pd.DataFrame:
    """
    Simula portfolios aleatorios para plotar a fronteira eficiente.

    Returns:
        DataFrame com colunas: retorno, volatilidade, sharpe, pesos por ativo.
    """
    n = len(precos.columns)
    retornos, cov = calcular_retorno_risco(precos, periodos_por_ano)
    resultados = []

    for _ in range(n_portfolios):
        pesos = np.random.dirichlet(np.ones(n))
        ret = np.dot(pesos, retornos)
        vol = np.sqrt(np.dot(pesos.T, np.dot(cov.values, pesos)))
        sharpe = (ret - risk_free) / vol
        row = {"retorno": ret, "volatilidade": vol, "sharpe": sharpe}
        for ticker, peso in zip(precos.columns, pesos):
            row[ticker] = peso
        resultados.append(row)

    return pd.DataFrame(resultados)
