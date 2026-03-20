"""
valuation.py
Calculos de multiplos de mercado e DCF simplificado.
"""

import pandas as pd
import numpy as np
from typing import Optional


def calcular_multiplos(df_fundamentals: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe DataFrame de get_fundamentals() e calcula/normaliza multiplos.
    Adiciona colunas de decisao relativa ao peer group.

    Returns:
        DataFrame enriquecido com multiplos e sinais de valuation.
    """
    df = df_fundamentals.copy()

    # Mediana do peer group para cada multiplo
    multiplos = ["trailingPE", "priceToBook", "enterpriseToEbitda"]
    for col in multiplos:
        if col in df.columns:
            mediana = df[col].median()
            df[f"{col}_vs_peer"] = df[col] / mediana

    # Sinal de valuation: barata (<0.85x peer), neutra, cara (>1.15x peer)
    def _sinal(row):
        cols_vs = [c for c in row.index if c.endswith("_vs_peer")]
        if not cols_vs:
            return "indefinido"
        media_rel = row[cols_vs].mean()
        if media_rel < 0.85:
            return "barata vs peers"
        elif media_rel > 1.15:
            return "cara vs peers"
        return "neutra vs peers"

    df["decisao_valuation"] = df.apply(_sinal, axis=1)
    return df


def dcf_simplificado(
    fcf_historico: pd.Series,
    taxa_crescimento: float = 0.05,
    wacc: float = 0.10,
    anos_projecao: int = 5,
    shares_outstanding: Optional[int] = None
) -> dict:
    """
    DCF simplificado a partir de FCF historico.

    Args:
        fcf_historico: Serie de FCF anuais (mais recente primeiro ou ultimo).
        taxa_crescimento: Crescimento anual estimado do FCF.
        wacc: Custo medio ponderado de capital (taxa de desconto).
        anos_projecao: Numero de anos a projetar.
        shares_outstanding: Acoes em circulacao para calcular preco justo/acao.

    Returns:
        Dict com FCF projetado, VP, valor intrinseco e preco justo/acao.
    """
    fcf_base = fcf_historico.dropna().iloc[-1]  # FCF mais recente

    # Projecao de FCF
    fcf_projetado = [
        fcf_base * ((1 + taxa_crescimento) ** t)
        for t in range(1, anos_projecao + 1)
    ]

    # Valor presente de cada FCF projetado
    vp_fcf = [
        fcf / ((1 + wacc) ** t)
        for t, fcf in enumerate(fcf_projetado, start=1)
    ]

    # Valor terminal (perpetuidade de Gordon)
    taxa_crescimento_terminal = min(taxa_crescimento * 0.5, 0.03)
    fcf_terminal = fcf_projetado[-1] * (1 + taxa_crescimento_terminal)
    vt = fcf_terminal / (wacc - taxa_crescimento_terminal)
    vp_terminal = vt / ((1 + wacc) ** anos_projecao)

    valor_intrinseco = sum(vp_fcf) + vp_terminal
    preco_justo = valor_intrinseco / shares_outstanding if shares_outstanding else None

    return {
        "fcf_base": fcf_base,
        "fcf_projetado": fcf_projetado,
        "vp_fcf": vp_fcf,
        "vp_terminal": vp_terminal,
        "valor_intrinseco": valor_intrinseco,
        "preco_justo_por_acao": preco_justo,
        "wacc": wacc,
        "taxa_crescimento": taxa_crescimento,
    }
