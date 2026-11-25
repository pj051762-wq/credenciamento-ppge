from dataclasses import dataclass
from typing import List

PONTUACAO_MINIMA = 1.25
PERCENTIL_MINIMO = 0.25
MAX_ARTIGOS = 4
JANELA_BASE_ANOS = 4

@dataclass
class Artigo:
    titulo: str
    percentil: float

@dataclass
class Resultado:
    pontuacao: float
    credenciado: bool
    artigos_validos: List[Artigo]
    artigos_descartados: List[Artigo]
    janela_anos: float
    detalhes: str

def calcular_janela_anos(parentalidade: bool = False, pcd: bool = False, meses_licenca_medica: float = 0.0) -> float:
    janela = JANELA_BASE_ANOS
    if parentalidade:
        janela = JANELA_BASE_ANOS * 1.5
    if pcd:
        janela = max(janela, JANELA_BASE_ANOS * 1.25)
    if meses_licenca_medica > 0:
        janela += meses_licenca_medica / 12.0
    return janela

def avaliar(artigos: List[Artigo], janela_anos: float) -> Resultado:
    indicados = artigos[:MAX_ARTIGOS]
    validos = [a for a in indicados if a.percentil >= PERCENTIL_MINIMO]
    descartados = [a for a in indicados if a.percentil < PERCENTIL_MINIMO]
    pontuacao = sum(a.percentil for a in validos)
    credenciado = pontuacao >= PONTUACAO_MINIMA
    
    detalhes = f"Janela de análise: {janela_anos:.2f} ano(s). Artigos válidos: {len(validos)} | descartados: {len(descartados)}. Pontuação = {pontuacao:.2f} (mínimo {PONTUACAO_MINIMA})."
    
    return Resultado(pontuacao, credenciado, validos, descartados, janela_anos, detalhes)